from typing import List, Tuple

import numpy as np
from FlagEmbedding import BGEM3FlagModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

bge_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True, device=0)
bge_reranker_tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-v2-m3', device=0)
bge_reranker_model = AutoModelForSequenceClassification.from_pretrained('BAAI/bge-reranker-v2-m3')


def gen_dense_embedding(sentence):
    return bge_model.encode(
        sentence,
        batch_size=2,
        max_length=2048,
        return_dense=True,
        return_sparse=False,
    )['dense_vecs']


def gen_sparse_embedding(sentence):
    return bge_model.encode(
        sentence,
        batch_size=2,
        max_length=2048,
        return_dense=False,
        return_sparse=True,
    )['lexical_weights']


def cal_text_pairs_rank(p: List[Tuple[str, str]]) -> List[float]:
    def exp_norm(x):
        b = x.max()
        y = np.exp(x - b)
        return y / y.sum()

    bge_reranker_model.eval()
    with torch.no_grad():
        inputs = bge_reranker_tokenizer(p, return_tensors='pt', padding=True, truncation=True)
        scores = bge_reranker_model(**inputs, return_dict=True).logits.view(-1, ).float()
        scores = exp_norm(scores.numpy())
    print(np.round(scores * 100, 2))
    return scores


if __name__ == '__main__':
    print(torch.cuda.is_available())
    # dense_res = gen_dense_embedding(['hello-world'])
    # sparse_res = gen_sparse_embedding(['hello-world'])
    # print(dense_res)
    # print(sparse_res)
    pairs = [
        ('김갑환은 무슨 기술을 사용하나요?', '김갑환은 봉황각을 사용합니다,'),
        ('김갑환은 무슨 기술을 사용하나요?', '최번개가 알고보면 한국팀의 에이스입니다.'),
        ('김갑환은 무슨 기술을 사용하나요?', '김갑환은 앞차기가 핵심이며 종종 뒤돌려차기도 활용합니다'),
    ]
    res = cal_text_pairs_rank(pairs)
    print(res)
