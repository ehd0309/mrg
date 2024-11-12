from typing import List
from langchain_core.documents import Document


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def format_docs_with_meta(docs: List[Document]):
    formatted_docs = []
    for doc in docs:
        formatted_doc = {
            "doc_content": doc.page_content,
            "파일_이름": doc.metadata['filename'].split("_")[0],
            "파일이_작성된_날짜": doc.metadata['filename'].split("_")[1],
            "추가_정보": doc.metadata['additional_content']
        }
        formatted_docs.append(formatted_doc)
    return formatted_docs
