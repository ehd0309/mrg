import os
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

import fitz
import pymupdf4llm

from surya.schema import OCRResult

INPUT_PATH = Path(__file__).parent.parent.resolve() / 'assets/inputs'
OUTPUT_PATH = Path(__file__).parent.parent.resolve() / 'assets/outputs'
FONT_PATH = Path(__file__).parent.parent.resolve() / 'public/batang_m.ttf'
EXTENSIONS = ['.pdf', '.jpg', '.png']


def load_input_images(index):
    from surya.input.load import load_from_folder
    print(INPUT_PATH, index)
    igs, texts, _ = load_from_folder(INPUT_PATH / index)
    return igs, texts


def get_output_path():
    return OUTPUT_PATH


def get_input_path():
    return INPUT_PATH


def gen_text_pdf_from_pred(name: str, prediction: OCRResult, index: str):
    output_pdf = fitz.open()
    page = output_pdf.new_page(width=int(prediction.image_bbox[2]), height=int(prediction.image_bbox[3]))
    page.insert_font(fontfile=FONT_PATH, fontname="F1")
    for textLine in prediction.text_lines:
        if textLine.text.strip() != '':
            x0, y0 = textLine.bbox[0], textLine.bbox[1]
            x1, y1 = textLine.bbox[2], textLine.bbox[3]
            page.insert_text((x0, (y0 + y1) / 2), textLine.text, fontsize=11, fontname="F1", color=(0, 0, 0))
    res_file_path = OUTPUT_PATH / index / '{}.pdf'.format(name)
    os.makedirs(res_file_path.parent, exist_ok=True)
    output_pdf.save(res_file_path)
    output_pdf.close()
    return str(res_file_path)


def gen_md_from_text_pdf(file_path: str):
    md_text = pymupdf4llm.to_markdown(file_path, margins=(0, 0, 0, 0))
    result_path = file_path.split(".pdf")[0] + ".md"
    os.makedirs(Path(result_path).parent, exist_ok=True)
    Path(result_path).write_bytes(md_text.encode())
    return result_path


if __name__ == '__main__':
    print(get_output_path())
    # images, names = load_input_images('연세')
    # print(images)
    # print(names)
