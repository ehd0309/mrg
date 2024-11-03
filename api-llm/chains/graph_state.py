from typing import Any, List, TypedDict

from langchain_core.documents import Document

from components import OCRResolver


class AdvancedDocumentPreprocessorState(TypedDict):
    index_name: str
    markdown_paths: list[str]
    ocr_resolver: OCRResolver
    ocr_result_paths: list[str]
    documents: List[Document]
    text_contents: List[Document]
    table_contents: List[Document]
    keywords: list[list[str]]
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
