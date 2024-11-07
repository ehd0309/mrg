from typing import List
from langchain_core.documents import Document


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def format_docs_with_meta(docs: List[Document]):
    formatted_docs = []
    for doc in docs:
        formatted_doc = {
            "doc_content": doc.page_content,
            "filename": doc.metadata['filename']
        }
        formatted_docs.append(formatted_doc)
    return formatted_docs
