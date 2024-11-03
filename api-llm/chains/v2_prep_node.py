from chains.graph_state import AdvancedDocumentPreprocessorState
from components import OCRResolver, VectorDatabase, TransformersDenseEmbeddings, Prompt, LLM, convert_di_documents, \
    extract_keywords
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker


def ocr_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    index_name = state['index_name']
    ocr_resolver = OCRResolver()
    result_md_paths = ocr_resolver.gen_md_from_pdf_v2(index_name=index_name)
    return AdvancedDocumentPreprocessorState(
        ocr_result_paths=result_md_paths,
        step='IN-PROGRESS',
        ocr_resolver=ocr_resolver)


def get_markdown_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    index_name = state['index_name']
    ocr_resolver = state['ocr_resolver']
    md_files = ocr_resolver.get_md_result_files(index_name=index_name)
    return AdvancedDocumentPreprocessorState(markdown_paths=md_files)


def text_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    md_files = state['markdown_paths']
    documents = []
    for md_file in md_files:
        loader = UnstructuredMarkdownLoader(
            md_file,
            mode="single",  # elements
            strategy="fast"
        )
        doc = loader.load()
        documents.extend(doc)
    for doc in documents:
        filename = doc.metadata['source'].split("\\")[-1]
        doc.metadata['filename'] = filename
        doc.metadata['additional_content'] = ''
        doc.metadata['category'] = 'Plain'
        del doc.metadata['source']
    return AdvancedDocumentPreprocessorState(text_contents=documents)


def table_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    md_files = state['markdown_paths']
    documents = []
    for md_file in md_files:
        loader = UnstructuredMarkdownLoader(
            md_file,
            mode="elements",  # elements
            strategy="fast"
        )
        doc = loader.load()
        documents.extend(doc)
    table_contents = []
    for doc in documents:
        if doc.metadata['category'] == 'Table':
            table_contents.append(doc)
    return AdvancedDocumentPreprocessorState(table_contents=table_contents)


def table_summary_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    table_contents = state['table_contents']
    result_table_contents = []
    chain = (
            {'table': RunnablePassthrough()}
            | Prompt.table_summary()
            | LLM().load_local(temp=0.5)
            | StrOutputParser()
    )
    for index, document in enumerate(table_contents):
        metadata = {}
        table_summary = chain.invoke(document.metadata['text_as_html'])
        page_content = table_summary
        metadata['additional_content'] = document.metadata['text_as_html']
        metadata['filename'] = document.metadata['filename']
        metadata['category'] = document.metadata['category']
        document = Document(
            page_content=page_content,
            metadata=metadata
        )
        result_table_contents.append(document)
    return AdvancedDocumentPreprocessorState(table_contents=result_table_contents)


def merge_documents_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    """Merge all documents"""
    table_contents = state['table_contents']
    text_contents = state['text_contents']
    documents = table_contents + text_contents
    return AdvancedDocumentPreprocessorState(documents=documents)


def de_identify_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    documents = state['documents']
    di_documents = convert_di_documents(documents)
    return AdvancedDocumentPreprocessorState(documents=di_documents)


def semantic_text_splitter_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    text_contents = state['text_contents']
    spliter = SemanticChunker(TransformersDenseEmbeddings(), min_chunk_size=50)
    result = spliter.split_documents(text_contents)
    return AdvancedDocumentPreprocessorState(text_contents=result)


def gen_keywords_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    documents = state['documents']
    keywords = extract_keywords(documents)
    return AdvancedDocumentPreprocessorState(keywords=keywords)


def embedding_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    return AdvancedDocumentPreprocessorState()
