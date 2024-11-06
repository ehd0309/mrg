from chains.graph_state import AdvancedRAGGraphState
from components import TransformersDenseEmbeddings, Prompt, LLM, TransformersSparseEmbeddings
from components.vdb import VectorDatabase
from utils import format_docs_with_meta
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter


def question_node(state: AdvancedRAGGraphState) -> AdvancedRAGGraphState:
    print('question_node')
    print(state)
    return AdvancedRAGGraphState(step='IN-PROGRESS')


def retrieve_document_node(state: AdvancedRAGGraphState) -> AdvancedRAGGraphState:
    print('retrieve_document_node')
    retriever = VectorDatabase().load_hybrid_retriever(
        collection_name=state['index_name'],
        dense_embedding=TransformersDenseEmbeddings(),
        sparse_embedding=TransformersSparseEmbeddings(),
        top_k=20
    )
    documents = retriever.invoke(state['question'])
    return AdvancedRAGGraphState(contexts=format_docs_with_meta(documents))




