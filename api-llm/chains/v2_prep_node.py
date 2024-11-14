from chains.graph_state import AdvancedDocumentPreprocessorState
from components import OCRResolver, VectorDatabase, TransformersDenseEmbeddings, TransformersSparseEmbeddings, Prompt, \
    LLM, convert_di_documents, extract_keywords
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker

from utils.logger import log_execution_time


@log_execution_time('RUN_OCR')
def ocr_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    index_name = state['index_name']
    ocr_resolver = OCRResolver()
    # result_md_paths = ocr_resolver.gen_md_from_pdf_v2(index_name=index_name)
    return AdvancedDocumentPreprocessorState(
        step='IN-PROGRESS',
        ocr_result_paths=[],
        ocr_resolver=ocr_resolver)


@log_execution_time('GENERATE_MARKDOWN')
def get_markdown_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    index_name = state['index_name']
    ocr_resolver = state['ocr_resolver']
    md_files = ocr_resolver.get_md_result_files(index_name=index_name)
    documents = []
    for md_file in md_files:
        loader = UnstructuredMarkdownLoader(
            md_file,
            mode="elements",  # elements
            strategy="fast"
        )
        doc = loader.load()
        documents.append([d for d in doc])
    return AdvancedDocumentPreprocessorState(
        markdown_paths=md_files,
        raw_documents=documents,
    )


@log_execution_time('DE-IDENTIFY')
def de_identify_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    documents = state['raw_documents']
    di_documents = []
    for document in documents:
        di_results = convert_di_documents(document)
        di_documents.append(di_results)
    return AdvancedDocumentPreprocessorState(raw_documents=documents)


@log_execution_time('EXTRACT_PLAIN_TEXT')
def text_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    raw_documents = state['raw_documents']
    text_contents = []
    for docs in raw_documents:
        prev_content = ''
        for doc in docs:
            if doc.metadata['category'] == 'Table':
                continue
            if len(doc.page_content) < 150:
                prev_content += doc.page_content + "\n"
                continue
            prev_content += doc.page_content + "\n"
            document = Document(
                page_content=prev_content,
                metadata={
                    'category': "Plain",
                    'filename': doc.metadata['filename'].replace(".md", ""),
                    'last_modified': doc.metadata['last_modified'],
                    'additional_content': ''
                }
            )
            text_contents.append(document)
            prev_content = ''
    return AdvancedDocumentPreprocessorState(documents=text_contents)


@log_execution_time('EXTRACT_IMAGE')
def image_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    index_name = state['index_name']
    return AdvancedDocumentPreprocessorState(index_name=index_name)


@log_execution_time('IMAGE_SAVED(DONE)')
def save_image_node(state: AdvancedDocumentPreprocessorState):
    index_name = state['index_name']
    return AdvancedDocumentPreprocessorState(index_name=index_name)


@log_execution_time('EXTRACT_TABLE')
def table_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    raw_documents = state['raw_documents']
    table_contents = []
    for docs in raw_documents:
        for doc in docs:
            if doc.metadata['category'] == 'Table':
                document = Document(
                    page_content=doc.page_content,
                    metadata={
                        'category': "Table",
                        'filename': doc.metadata['filename'].replace(".md", ""),
                        'last_modified': doc.metadata['last_modified'],
                        'additional_content': doc.metadata['text_as_html']
                    }
                )
                table_contents.append(document)
    return AdvancedDocumentPreprocessorState(table_contents=table_contents)


@log_execution_time('TABLE_SUMMARIZATION')
def table_summary_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    table_contents = state['table_contents']
    summarized_table_contents = []
    chain = (
            {'table': RunnablePassthrough()}
            | Prompt.table_summary()
            | LLM().load_local(temp=0.5)
            | StrOutputParser()
    )
    for index, document in enumerate(table_contents):
        metadata = {}
        table_summary = chain.invoke(document.metadata['additional_content'])
        page_content = table_summary
        metadata['additional_content'] = document.metadata['additional_content']
        metadata['filename'] = document.metadata['filename']
        metadata['category'] = document.metadata['category']
        metadata['last_modified'] = document.metadata['last_modified']
        document = Document(
            page_content=page_content,
            metadata=metadata
        )
        summarized_table_contents.append(document)
    return AdvancedDocumentPreprocessorState(documents=summarized_table_contents)


@log_execution_time('SEMANTIC_CHUNKING')
def semantic_text_splitter_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    documents = state['documents']
    spliter = SemanticChunker(TransformersDenseEmbeddings(),
                              breakpoint_threshold_type="gradient",
                              breakpoint_threshold_amount=90
                              )
    result = spliter.split_documents(documents)
    filtered_blank_documents = []
    for document in result:
        if len(document.page_content.strip()) != 0:
            filtered_blank_documents.append(document)
    return AdvancedDocumentPreprocessorState(documents=filtered_blank_documents)


@log_execution_time('EXTRACT_KEYWORDS')
def gen_keywords_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    documents = state['documents']
    keywords = extract_keywords(documents)
    return AdvancedDocumentPreprocessorState(keywords=keywords)


@log_execution_time('EMBEDDING')
def embedding_node(state: AdvancedDocumentPreprocessorState) -> AdvancedDocumentPreprocessorState:
    documents = state['documents']
    index_name = state['index_name']
    keywords = state['keywords']
    vector_store = VectorDatabase()
    vector_store.generate_collection_idx(index_name)
    vector_store.hybrid_embedding(
        collection_name=index_name,
        docs=documents,
        keywords=keywords,
        dense_embedding=TransformersDenseEmbeddings(),
        sparse_embedding=TransformersSparseEmbeddings()
    )
    return AdvancedDocumentPreprocessorState(step='DONE')
