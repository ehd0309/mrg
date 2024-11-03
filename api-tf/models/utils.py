from typing import List
from keybert import KeyBERT
from kiwipiepy import Kiwi

from transformers import AutoTokenizer, AutoModelForTokenClassification, BertModel, pipeline
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


def noun_extractor(text):
    results = []
    kiwi = Kiwi()
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
            results.append(token)
    return results


def preprocess(text):
    nouns = noun_extractor(text)
    return ' '.join(nouns)


def split_into_sentences(text):
    kiwi = Kiwi()
    str_list = kiwi.split_into_sents(text)
    keyword_list = []
    for id_num in range(1, len(str_list) + 1):
        str_list[id_num - 1] = str_list[id_num - 1].text
        keyword_list.append(preprocess(str_list[id_num - 1]))
    return str_list, keyword_list


def get_keywords(kw_model, texts):
    sentences, pre_sentences = split_into_sentences(texts)
    result = []
    for id_num in range(1, len(sentences) + 1):
        keywords = kw_model.extract_keywords(pre_sentences[id_num - 1], keyphrase_ngram_range=(1, 1),
                                             stop_words='english',
                                             use_mmr=True,
                                             top_n=14)
        keywords = [item[0] for item in keywords]
        result.extend(keywords)
    return result


def generate_keywords(sentences: List[str]):
    model = BertModel.from_pretrained('monologg/kobert')
    model.to(torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
    kw_model = KeyBERT(model)
    keywords = []
    for sentence in sentences:
        keyword_list = get_keywords(kw_model, sentence)
        keywords.append(keyword_list)
    del model
    del kw_model
    return keywords


if __name__ == "__main__":
    res = generate_keywords(['안녕하세요 hello 저의 이름은 박동석이라고 합니다'])
    print(res)
