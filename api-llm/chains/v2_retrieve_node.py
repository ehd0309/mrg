from langchain.retrievers.document_compressors import CrossEncoderReranker, EmbeddingsFilter

from chains.graph_state import AdvancedRAGGraphState
from components import TransformersDenseEmbeddings, Prompt, LLM, TransformersSparseEmbeddings, TransformerReranker
from components.vdb import VectorDatabase
from utils import format_docs_with_meta
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_transformers import LongContextReorder

from utils.logger import log_execution_time


@log_execution_time('QUESTION')
def question_node(state: AdvancedRAGGraphState) -> AdvancedRAGGraphState:
    question = state['question']
    return AdvancedRAGGraphState(step='IN-PROGRESS', question=question)


@log_execution_time('HYBRID_SEARCH')
def retrieve_document_node(state: AdvancedRAGGraphState) -> AdvancedRAGGraphState:
    question = state['question']
    retriever = VectorDatabase().load_hybrid_retriever(
        collection_name=state['index_name'],
        dense_embedding=TransformersDenseEmbeddings(),
        sparse_embedding=TransformersSparseEmbeddings(),
        top_k=20)
    # contexts = retriever.invoke(question)
    return AdvancedRAGGraphState(
        # contexts=contexts,
        retriever=retriever
    )


@log_execution_time("RERANKING")
def rerank_node(state: AdvancedRAGGraphState) -> AdvancedRAGGraphState:
    retriever = state['retriever']
    model = TransformerReranker()
    compressor = CrossEncoderReranker(model=model, top_n=10)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=retriever
    )
    return AdvancedRAGGraphState(
        retriever=compression_retriever
    )


@log_execution_time("Q-CLASSIFIER")
def classify_question_node(state: AdvancedRAGGraphState):
    question = state['question']
    chain = (
            {"question": itemgetter('question'), "subject": itemgetter('subject')}
            | Prompt.question_abstraction()
            | LLM().load_local(temp=0)
            | StrOutputParser()
    )
    response = chain.invoke(
        {"question": question,
         "subject": '암 환자 진료 기록'}).strip()
    result = response
    if response != 'abstract' and response != 'specific':
        result = 'abstract'
    return result


@log_execution_time("CONTEXT_FILTERING")
def filter_node(state: AdvancedRAGGraphState) -> AdvancedRAGGraphState:
    retriever = state['retriever']
    embeddings_filter = EmbeddingsFilter(
        embeddings=TransformersDenseEmbeddings(),
        similarity_threshold=0.5
    )
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=embeddings_filter, base_retriever=retriever,
    )
    # contexts = compression_retriever.invoke(state['question'])
    return AdvancedRAGGraphState(
        # contexts=contexts,
        retriever=compression_retriever
    )


@log_execution_time("CONTEXT_REORDER")
def reorder_node(state: AdvancedRAGGraphState) -> AdvancedRAGGraphState:
    reordering = LongContextReorder()
    retriever = state['retriever']
    documents = retriever.invoke(state['question'])
    formatted_documents = format_docs_with_meta(reordering.transform_documents(documents))
    return AdvancedRAGGraphState(contexts=formatted_documents)


# @log_execution_time("GENERATE_ANSWER")
async def llm_answer_node(state: AdvancedRAGGraphState) -> AdvancedRAGGraphState:
    chain = (
            {"question": itemgetter("question"), "context": itemgetter("context")}
            | Prompt.rag()
            | LLM().load_local(
        temp=0.3,
        streaming=True,
        frequency_penalty=1,
        # top_p=0.95,
        # top_k=40,
    )
            | StrOutputParser()
    )
    answer = await chain.ainvoke(
        {"question": state["question"], "context": state["contexts"]}
    )
    print('question:', state['question'])
    print('contexts:', len(state['contexts']))
    for context in state['contexts']:
        print('context:', context)
    return AdvancedRAGGraphState(
        answer=answer,
        question=state["question"],
        contexts=state["contexts"],
    )
