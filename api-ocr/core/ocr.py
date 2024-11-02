from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor

from utils import load_input_images, gen_text_pdf_from_pred, gen_md_from_text_pdf

import gc

langs = ["ko"]


# run only once
def pdf_to_md(index):
    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()

    images, names = load_input_images(index)
    result_pdfs = []
    for i in range(len(names)):
        name = names[i] + "_" + str(i + 1)
        image = images[i]
        predictions = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)
        for pred in predictions:
            res_path = gen_text_pdf_from_pred(name=name, prediction=pred, index=index)
            result_pdfs.append(res_path)
        del predictions
        del image
    result_mds = []
    for pdf in result_pdfs:
        md = gen_md_from_text_pdf(pdf)
        result_mds.append(md)
        del md
    del det_processor
    del det_model
    del rec_model
    del rec_processor
    del images
    del names
    gc.collect()
    return result_mds


if __name__ == '__main__':
    pdf_to_md('연세')
