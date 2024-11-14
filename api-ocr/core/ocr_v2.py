from marker.models import load_all_models
from utils.index import load_input_images, get_input_path, get_output_path
from marker.pdf.images import render_image
from marker.output import get_subfolder_path

import warnings
from marker.schema.page import Page

import pypdfium2 as pdfium  # Needs to be at the top to avoid warnings
from PIL import Image
import fitz
import json

from marker.utils import flush_cuda_memory
from marker.tables.table import format_tables
from marker.debug.data import dump_bbox_debug_data, draw_page_debug_images
from marker.layout.layout import annotate_block_types
from marker.layout.order import surya_order, sort_blocks_in_reading_order
from marker.ocr.lang import replace_langs_with_codes, validate_langs
from marker.ocr.detection import surya_detection
from marker.ocr.recognition import run_ocr
from marker.pdf.extract_text import get_text_blocks
from marker.cleaners.headers import filter_header_footer, filter_common_titles
from marker.equations.equations import replace_equations
from marker.pdf.utils import find_filetype
from marker.cleaners.code import identify_code_blocks, indent_blocks
from marker.cleaners.bullets import replace_bullets
from marker.cleaners.headings import split_heading_blocks, infer_heading_levels
from marker.cleaners.fontstyle import find_bold_italic
from marker.postprocessors.markdown import merge_spans, merge_lines, get_full_text
from marker.cleaners.text import cleanup_text
from marker.images.extract import extract_images
from marker.images.save import images_to_dict
from marker.cleaners.toc import compute_toc

from typing import List, Dict, Tuple, Optional
from marker.settings import settings

warnings.filterwarnings("ignore", category=UserWarning)  # Filter torch pytree user warnings

import os

os.environ[
    "PYTORCH_ENABLE_MPS_FALLBACK"] = "1"  # For some reason, transformers decided to use .isin for a simple op, which is not supported on MPS


def get_batch_size():
    if settings.LAYOUT_BATCH_SIZE is not None:
        return settings.LAYOUT_BATCH_SIZE
    elif settings.TORCH_DEVICE_MODEL == "cuda":
        return 6
    return 6


def surya_layout(images: list, pages: List[Page], layout_model, batch_multiplier=1):
    from surya.layout import batch_layout_detection
    text_detection_results = [p.text_lines for p in pages]

    processor = layout_model.processor
    layout_results = batch_layout_detection(images, layout_model, processor, detection_results=text_detection_results,
                                            batch_size=int(get_batch_size() * batch_multiplier))
    for layout_result in layout_results:
        for bbox in layout_result.bboxes:
            if bbox.label == 'Table':
                if bbox.bbox[2] - bbox.bbox[0] < 280:
                    bbox.label = 'Text'
    for page, layout_result in zip(pages, layout_results):
        page.layout = layout_result


def convert_single_pdf(
        fname: str,
        model_lst: List,
        max_pages: int = None,
        start_page: int = None,
        metadata: Optional[Dict] = None,
        langs: Optional[List[str]] = None,
        batch_multiplier: int = 1,
        ocr_all_pages: bool = False
) -> List[Tuple[str, Dict[str, Image.Image], Dict]]:
    ocr_all_pages = ocr_all_pages or settings.OCR_ALL_PAGES

    if metadata:
        langs = metadata.get("languages", langs)

    langs = replace_langs_with_codes(langs)
    validate_langs(langs)

    # Find the filetype
    filetype = find_filetype(fname)

    # Setup output metadata
    out_meta = {
        "languages": langs,
        "filetype": filetype,
    }

    if filetype == "other":  # We can't process this file
        return []

    # Get initial text blocks from the pdf
    doc = pdfium.PdfDocument(fname)
    pages, toc = get_text_blocks(
        doc,
        fname,
        max_pages=max_pages,
        start_page=start_page
    )
    out_meta.update({
        "pdf_toc": toc,
        "pages": len(pages),
    })

    # Trim pages from doc to align with start page
    if start_page:
        for page_idx in range(start_page):
            doc.del_page(0)

    max_len = min(len(pages), len(doc))
    lowres_images = [render_image(doc[pnum], dpi=settings.SURYA_DETECTOR_DPI) for pnum in range(max_len)]

    # Unpack models from list
    texify_model, layout_model, order_model, detection_model, ocr_model, table_rec_model = model_lst

    # Identify text lines, layout, reading order
    surya_detection(lowres_images, pages, detection_model, batch_multiplier=batch_multiplier)

    # OCR pages as needed
    pages, ocr_stats = run_ocr(doc, pages, langs, ocr_model, batch_multiplier=batch_multiplier,
                               ocr_all_pages=ocr_all_pages)

    out_meta["ocr_stats"] = ocr_stats
    if len([b for p in pages for b in p.blocks]) == 0:
        print(f"Could not extract any text blocks for {fname}")
        return []

    surya_layout(lowres_images, pages, layout_model, batch_multiplier=batch_multiplier)

    # Find headers and footers
    bad_span_ids = filter_header_footer(pages)
    out_meta["block_stats"] = {"header_footer": len(bad_span_ids)}

    # Add block types from layout
    annotate_block_types(pages)

    # Sort from reading order
    # surya_order(lowres_images, pages, order_model, batch_multiplier=batch_multiplier)
    # sort_blocks_in_reading_order(pages)

    # Dump debug data if flags are set
    draw_page_debug_images(fname, pages)
    dump_bbox_debug_data(fname, pages)

    # Fix code blocks
    code_block_count = identify_code_blocks(pages)
    out_meta["block_stats"]["code"] = code_block_count
    indent_blocks(pages)

    # Fix table blocks
    table_count = format_tables(pages, doc, fname, detection_model, table_rec_model, ocr_model)
    out_meta["block_stats"]["table"] = table_count

    # Replace equations
    filtered, eq_stats = replace_equations(doc, pages, texify_model, batch_multiplier=batch_multiplier)
    flush_cuda_memory()
    out_meta["block_stats"]["equations"] = eq_stats

    # Extract images and figures
    if settings.EXTRACT_IMAGES:
        extract_images(doc, pages)

    # Split out headers
    split_heading_blocks(pages)
    infer_heading_levels(pages)
    find_bold_italic(pages)

    # Compute table of contents
    out_meta["computed_toc"] = compute_toc(pages)

    # Process each page independently
    page_outputs = []
    for i, page in enumerate(pages):
        page_meta = out_meta.copy()
        page_meta['page_number'] = i + 1  # 페이지 번호 추가

        # Copy to avoid changing original data
        merged_lines = merge_spans([page])
        text_blocks = merge_lines(merged_lines)
        text_blocks = filter_common_titles(text_blocks)
        full_text = get_full_text(text_blocks)

        # Cleanup text
        full_text = cleanup_text(full_text)
        full_text = replace_bullets(full_text)

        # Extract images for each page
        doc_images = images_to_dict([page])

        page_outputs.append((full_text, doc_images, page_meta))

    return page_outputs


def det_rec_all(file_path, model_list):
    return convert_single_pdf(file_path, model_list, langs=["ko", "en"],
                              batch_multiplier=4,
                              ocr_all_pages=True)


def pdf_to_md(index_name, publish_callback, id):
    from marker.output import save_markdown
    _, names = load_input_images(index_name)
    fnames = list(set(names))
    result_mds = []
    # if len(names) != 1:
    #     for idx, name in enumerate(names):
    #         if idx == 0:
    #             continue
    #         page_filename = f"{name}_page_{idx}.md"
    #
    #         md_path = get_subfolder_path(str(get_output_path() / index_name), page_filename)
    #         result_mds.append(str(md_path))
    #     return result_mds
    pdf_cnt = get_pdf_page_count(get_input_path().resolve() / index_name / (fnames[0] + ".pdf"))
    publish_callback(json.dumps({"pageNum": pdf_cnt, 'processedPageCount': 0, 'status': 'pending', 'id': id}))
    model_list = load_all_models()
    for fname in fnames:
        file_path = get_input_path().resolve() / index_name / (fname + ".pdf")

        page_outputs = det_rec_all(file_path, model_list)
        for page_number, (full_text, images, out_meta) in enumerate(page_outputs, start=1):
            page_filename = f"{fname}_page_{page_number}.md"  # 각 페이지의 파일명 지정
            result_path = save_markdown(str(get_output_path() / index_name), page_filename, full_text, images, out_meta)
            print(f"Saved markdown for page {page_number} to {result_path}")
            result_mds.append(result_path)
            publish_callback(json.dumps({"pageNum": pdf_cnt, 'processedPageCount': page_number, 'id': id}))
    del model_list
    return result_mds


def get_pdf_page_count(file_path):
    with fitz.open(file_path) as pdf:
        return pdf.page_count


if __name__ == "__main__":
    res = pdf_to_md('yunv2')
    print(res)
