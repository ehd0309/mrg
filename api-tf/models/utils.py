from typing import List
from keybert import KeyBERT
from kiwipiepy import Kiwi
from konlpy.tag import Okt
import re
from gliner import GLiNER

okt = Okt()

from transformers import BertModel
import gc
import torch


def load_kr_ner():
    ner_model = GLiNER.from_pretrained("taeminlee/gliner_ko")
    return ner_model


def inference_kr_name(text, model):
    person_labels = ["PERSON"]
    entities = model.predict_entities(text, person_labels)
    return entities


def pseudonymizate_kr_names(sentences: List[str]):
    model = load_kr_ner()
    results = []
    for sentence in sentences:
        noun_sentence = noun_text(sentence)
        result = inference_kr_name(noun_sentence, model)
        results.append(result)
    for idx, result in enumerate(results):
        for r in result:
            if r['score'] < 0.75:
                continue
            if r['label'] != 'PERSON':
                continue
            sentences[idx] = sentences[idx].replace(r['text'], r['text'][0] + "○" * (len(r['text']) - 1))
    del results
    del model
    gc.collect()
    return sentences


def noun_extractor(text):
    results = []
    kiwi = Kiwi()
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('N'):
            results.append(token)
    return results


def noun_text(text):
    nouns = noun_extractor(text)
    return ' '.join(nouns)


def split_into_sentences(text):
    kiwi = Kiwi()
    str_list = kiwi.split_into_sents(text)
    keyword_list = []
    for id_num in range(1, len(str_list) + 1):
        str_list[id_num - 1] = str_list[id_num - 1].text
        keyword_list.append(noun_text(str_list[id_num - 1]))
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
    sens = ['박동석이 춤을 춘다. 박동석이 미쳐 날뛴다. 김갑환은 발차기를 한다 민선호/민선기/민소현', 'hello world 방사선치료를 받아보자']
    print(noun_extractor(sens[0]))
    print(noun_extractor(sens[1]))
    res = pseudonymizate_kr_names(sens)
    print(res)
