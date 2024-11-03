from chains.graph_state import BaseDocumentPreProcessorState
from components import OCRResolver, VectorDatabase, TransformersDenseEmbeddings
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter


def ocr_node(state: BaseDocumentPreProcessorState) -> BaseDocumentPreProcessorState:
    index_name = state['index_name']
    ocr_resolver = OCRResolver()
    result_md_paths = ocr_resolver.gen_md_from_pdf_v1(index_name=index_name)
    return BaseDocumentPreProcessorState(
        ocr_result_paths=result_md_paths,
        step='IN-PROGRESS',
        ocr_resolver=ocr_resolver)


def pdf_to_docs_node(state: BaseDocumentPreProcessorState) -> BaseDocumentPreProcessorState:
    index_name = state['index_name']
    ocr_resolver = state['ocr_resolver']
    md_files = ocr_resolver.get_md_result_files(index_name=index_name)
    documents = []
    for md_file in md_files:
        loader = UnstructuredMarkdownLoader(
            md_file,
            mode="single",  # elements
            # strategy="fast"
        )
        doc = loader.load()
        documents.extend(doc)
    return BaseDocumentPreProcessorState(documents=documents)


def docs_split_node(state: BaseDocumentPreProcessorState) -> BaseDocumentPreProcessorState:
    documents = state['documents']
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=12)
    texts = text_splitter.split_documents(documents)
    return BaseDocumentPreProcessorState(documents=texts)


def ingest_node(state: BaseDocumentPreProcessorState) -> BaseDocumentPreProcessorState:
    index_name = state['index_name']
    documents = state['documents']
    vector_db = VectorDatabase().load(
        collection_name=index_name,
        embeddings=TransformersDenseEmbeddings(),
    )
    from uuid import uuid4
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_db.add_documents(documents=documents, ids=uuids)
    return BaseDocumentPreProcessorState(step="DONE")
