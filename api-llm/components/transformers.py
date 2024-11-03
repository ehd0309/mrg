from typing import List

import requests
from langchain_core.documents import Document

from utils import EnvFinder


def convert_di_documents(docs: List[Document]) -> List[Document]:
    page_contents = [doc.page_content for doc in docs]
    api_path = EnvFinder().get_transformers_url() + '/api/token/de-identify'
    response = requests.post(
        api_path,
        json={"sentence": page_contents}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed: {response.status_code}, {response.text}")
    di_page_contents = response.json()
    di_docs = [
        Document(page_content=di_content, metadata=doc.metadata)
        for doc, di_content in zip(docs, di_page_contents)
    ]
    return di_docs


def extract_keywords(docs: List[Document]) -> List[str]:
    page_contents = [doc.page_content for doc in docs]
    api_path = EnvFinder().get_transformers_url() + '/api/token/keywords'
    response = requests.post(
        api_path,
        json={"sentence": page_contents}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed: {response.status_code}, {response.text}")
    extracted_keywords = response.json()
    return extracted_keywords
