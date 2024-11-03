from chains.graph_state import BaseRAGGraphState
from components import TransformersDenseEmbeddings, Prompt, LLM
from components.vdb import VectorDatabase
from utils import format_docs
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter


def question_node(state: BaseRAGGraphState) -> BaseRAGGraphState:
    print('question_node')
    print(state)
    return BaseRAGGraphState(step='IN-PROGRESS')


def retrieve_document_node(state: BaseRAGGraphState) -> BaseRAGGraphState:
    print('retrieve_document_node')
    vector_store = VectorDatabase().load(collection_name=state['index_name'], embeddings=TransformersDenseEmbeddings())
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    documents = retriever.invoke(state['question'])
    return BaseRAGGraphState(contexts=format_docs(documents))


async def llm_answer_node(state: BaseRAGGraphState) -> BaseRAGGraphState:
    print('llm_answer_node')
    chain = (
            {"question": itemgetter("question"), "context": itemgetter("context")}
            | Prompt.rag()
            | LLM().load_local(temp=0.2, streaming=True)
            | StrOutputParser()
    )
    answer = await chain.ainvoke(
        {"question": state["question"], "context": state["contexts"]}
    )
    return BaseRAGGraphState(
        answer=answer,
        question=state["question"],
        contexts=state["contexts"],
    )
