from langchain.retrievers.document_compressors import LLMChainExtractor, LLMChainFilter

from chains.graph_state import AdvancedRAGGraphState
from langgraph.graph import START, END, StateGraph

from chains.v2_retrieve_node import retrieve_document_node, question_node, llm_answer_node, rerank_node, \
    classify_question_node, filter_node
from components import Prompt, LLM
from operator import itemgetter


def init_workflow():
    parent_builder = StateGraph(AdvancedRAGGraphState)
    parent_builder.add_node('Take Question', question_node)
    parent_builder.add_node('Retrieve Document', retrieve_document_node)
    parent_builder.add_node('Reranking', rerank_node)
    parent_builder.add_node('Return Answer', llm_answer_node)
    parent_builder.add_node('Filter Contexts', filter_node)

    parent_builder.add_edge(START, 'Take Question')
    parent_builder.add_edge('Take Question', 'Retrieve Document')
    parent_builder.add_edge('Retrieve Document', 'Reranking')

    parent_builder.add_conditional_edges(
        "Reranking",
        classify_question_node,
        {
            "abstract": "Return Answer",
            "specific": "Filter Contexts",
        }
    )
    parent_builder.add_edge('Filter Contexts', 'Return Answer')
    parent_builder.add_edge('Return Answer', END)
    return parent_builder.compile()


if __name__ == '__main__':
    output = init_workflow().get_graph(xray=True)
    with open("output_image.png", "wb") as f:
        f.write(output.draw_mermaid_png())

    result = init_workflow().invoke({"question": '2019년 3월 28일에 고환 절제술을 받았나요?',
                                     "index_name": 'yunv2'})
    print(result)
    # for context in contexts:
    #     print(context)
    # chain = ({"question": itemgetter('question'), "subject": itemgetter('subject')}
    #          | Prompt.question_abstraction()
    #          | LLM().load_local(temp=0)
    #          )
    # result = chain.invoke({"question": '2023년 10월에 방사선 치료 기록이 있습니까', 'subject': '암 환자 진료 기록'})
    # print(result)
    # from langchain.retrievers import ContextualCompressionRetriever
    # print("GO!")
    # compression_retriever = ContextualCompressionRetriever(
    #     base_compressor=LLMChainFilter.from_llm(LLM().load_local(temp=0)),
    #     base_retriever=ret,
    #     k=1
    # )
    # compressed_docs = (
    #     compression_retriever.invoke(
    #         "진료 기록을 요약해주세요"
    #     )
    # )
    # print(compressed_docs)
    from langchain_community.cross_encoders import HuggingFaceCrossEncoder

    from langchain_community.document_compressors.rankllm_rerank import RankLLMRerank
