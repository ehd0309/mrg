from typing import List

import requests
from langchain.embeddings.base import Embeddings

from utils import EnvFinder


class TransformersDenseEmbeddings(Embeddings):
    def __init__(self, endpoint: str = EnvFinder().get_transformers_url()):
        self.endpoint = endpoint

    def embed_documents(self, sentences: list) -> List[List[float]]:
        path = self.endpoint + "/api/embed/dense"
        response = requests.post(
            path,
            json={"sentence": sentences}
        )
        if response.status_code != 200:
            raise ValueError(f"Request failed: {response.status_code}, {response.text}")
        result = response.json()
        return result["embeddings"]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


class TransformersSparseEmbeddings(Embeddings):
    def __init__(self, endpoint: str = EnvFinder().get_transformers_url()):
        self.endpoint = endpoint

    def embed_documents(self, sentences: list) -> List[List[float]]:
        path = self.endpoint + "/api/embed/sparse"
        response = requests.post(
            path,
            json={"sentence": sentences}
        )
        if response.status_code != 200:
            raise ValueError(f"Request failed: {response.status_code}, {response.text}")
        result = response.json()
        return result["embeddings"]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


if __name__ == "__main__":
    emb = TransformersDenseEmbeddings()
    res = emb.embed_query('hello world')
    print(res)
