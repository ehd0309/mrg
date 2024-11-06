from typing import List

import requests
from langchain_core.documents import Document

from utils import EnvFinder


def convert_di_documents(docs: List[Document]) -> List[Document]:
    page_contents = [doc.page_content for doc in docs]
    api_path = EnvFinder().get_transformers_url() + '/api/token/persons'
    response = requests.post(
        api_path,
        json={"sentences": page_contents}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed: {response.status_code}, {response.text}")
    persons = response.json()['persons']
    di_docs = []
    for idx, person in enumerate(persons):
        for r in person:
            if r['score'] >= 0.75 and r['label'] == 'PERSON':
                page_contents[idx] = page_contents[idx].replace(r['text'], r['text'][0] + "○" * (len(r['text']) - 1))
                if docs[idx].metadata['category'] == 'Table':
                    docs[idx].metadata['text_as_html'] = (
                        docs[idx].metadata['text_as_html'].replace(r['text'], r['text'][0] + "○" * (len(r['text']) - 1))
                    )
                docs[idx].page_content = page_contents[idx]
        di_docs.append(docs[idx])
    return di_docs


def extract_keywords(docs: List[Document]) -> List[str]:
    page_contents = [doc.page_content for doc in docs]
    api_path = EnvFinder().get_transformers_url() + '/api/token/keywords'
    response = requests.post(
        api_path,
        json={"sentences": page_contents}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed: {response.status_code}, {response.text}")
    extracted_keywords = response.json()
    return extracted_keywords['sentences']
