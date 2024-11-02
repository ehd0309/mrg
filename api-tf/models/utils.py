from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import gc


def load_kr_ner():
    tokenizer = AutoTokenizer.from_pretrained("yeajinmin/NER-NewsBI-150142-e3b4")
    model = AutoModelForTokenClassification.from_pretrained("yeajinmin/NER-NewsBI-150142-e3b4")
    ner = pipeline("ner", model=model, tokenizer=tokenizer, device=0)
    return ner


def inference_kr_name(text):
    ner_pipe = load_kr_ner()
    results = ner_pipe(text)
    del ner_pipe
    gc.collect()
    return results
