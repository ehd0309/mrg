from typing import List

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import gc
import torch


def load_kr_ner():
    tokenizer = AutoTokenizer.from_pretrained("yeajinmin/NER-NewsBI-150142-e3b4")
    model = AutoModelForTokenClassification.from_pretrained("yeajinmin/NER-NewsBI-150142-e3b4")
    ner = pipeline("ner", model=model, tokenizer=tokenizer,
                   device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
    return ner


def inference_kr_name(text):
    ner_pipe = load_kr_ner()
    results = ner_pipe(text)
    del ner_pipe
    gc.collect()
    return results


def deidentify_kr_names(sentences: List[str]):
    results = inference_kr_name(sentences)
    deidentify_sentences = sentences.copy()
    del sentences
    print(results)
    for idx, result in enumerate(results):
        for r in result:
            if r['score'] < 0.5:
                continue
            if r['entity'] != 'I-PS_NAME':
                continue
            start_idx = r['start']
            end_idx = r['end']
            deidentify_sentences[idx] = (
                    deidentify_sentences[idx][:start_idx] +
                    "○" +
                    deidentify_sentences[idx][end_idx:]
            )
    del results
    gc.collect()
    return deidentify_sentences


if __name__ == "__main__":
    res = inference_kr_name(['김옥수/김옥수/최규한'])
    print(res[0])
