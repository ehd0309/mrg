from marker.convert import convert_single_pdf
from marker.models import load_all_models

def det_rec_all(file_path, model_list):
    return convert_single_pdf(file_path, model_list, langs=["ko", "en"],
                              batch_multiplier=4,
                              ocr_all_pages=True)


def pdf_to_md(index_name):
    from marker.output import save_markdown
    model_list = load_all_models()
    _, names = load_input_images(index_name)
    fnames = list(set(names))
    result_mds = []
    for fname in fnames:
        file_path = get_input_path().resolve() / index_name / (fname + ".pdf")
        full_text, images, out_meta = det_rec_all(file_path, model_list)
        result_path = save_markdown(str(get_output_path()), fname + '.md', full_text, images, out_meta)
        print(f"Saved markdown to the {result_path} folder")
        result_mds.append(result_path)
        del result_path
        del full_text
        del images
        del out_meta
    del model_list
    return result_mds


if __name__ == "__main__":
    from utils import load_input_images, get_output_path, get_input_path

    res = pdf_to_md('yunv2')
    print(res)
