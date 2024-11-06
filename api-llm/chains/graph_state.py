from typing import Any, List, TypedDict, Annotated

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from components import OCRResolver
import operator


class AdvancedDocumentPreprocessorState(TypedDict):
    index_name: str
    markdown_paths: list[str]
    ocr_resolver: OCRResolver
    ocr_result_paths: list[str]
    raw_documents: List[List[Document]]
    documents: Annotated[List[Document], operator.add]
    text_contents: List[Document]
    table_contents: List[Document]
    keywords: list[str]
    step: str


class BaseDocumentPreProcessorState(TypedDict):
    """
    State for OCR document preprocessor Graph

    Attributes:
        index_name: 시작(pdf 폴더 경로)
        ocr_result_paths: OCR 결과 파일 경로 목록
        documents: 추출된 문서
        step: 단계 설명
    """
    index_name: str
    ocr_resolver: OCRResolver
    ocr_result_paths: list[str]
    documents: List[Document]
    step: str


class AdvancedRAGGraphState(TypedDict):
    index_name: str
    question: str
    answer: str
    contexts: List[Document]
    step: str
    chain: Any
    callback: Any
    retriever: BaseRetriever
    temperature: float
    max_tokens: int


class BaseRAGGraphState(TypedDict):
    """
    State for Basic RAG Graph
    """
    index_name: str
    question: str
    answer: str
    contexts: List[Document]
    step: str
    chain: Any
    callback: Any
