from typing import List
from keybert import KeyBERT
from kiwipiepy import Kiwi
from konlpy.tag import Okt
import re
from gliner import GLiNER

okt = Okt()

from transformers import AutoTokenizer, AutoModelForTokenClassification, BertModel, pipeline
import gc
import torch


def load_kr_ner():
    model = GLiNER.from_pretrained("taeminlee/gliner_ko")
    return model


def inference_kr_name(text, model):
    person_labels = ["PERSON"]
    entities = model.predict_entities(text, person_labels)
    return entities


def pseudonymizate_kr_names(sentences: List[str]):
    model = load_kr_ner()
    results = []
    for sentence in sentences:
        result = inference_kr_name(sentence, model)
        results.append(result)
    deidentify_sentences = sentences.copy()
    del sentences
    for idx, result in enumerate(results):
        for r in result:
            if r['score'] < 0.7:
                continue
            if r['entity'] != 'PERSON':
                continue
            start_idx = r['start']
            end_idx = r['end']
            deidentify_sentences[idx] = (
                    deidentify_sentences[idx][:start_idx] +
                    "○" +
                    deidentify_sentences[idx][end_idx:]
            )
    del results
    del model
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


def generate_morphs(sentences: List[str]):
    keywords = []
    for sentence in sentences:
        result = []
        for word in sentence.split():
            if re.match("^[가-힣]+$", word):
                result.extend(okt.morphs(word))
            else:
                result.append(word)
        keywords.append(" ".join(result))
    return keywords


if __name__ == "__main__":
    text = "너랑 나랑은 지금 안되어요 KtgArgs Transf he 24.155 나를 죽이면 어떻게 될까요 안녕하세요? 형태소 분석기 테스트베드입니다. best matching 4-h1ao abc-he kill "
    print(" ".join(okt.morphs(text)))
    result = generate_morphs([text])
    print(result)