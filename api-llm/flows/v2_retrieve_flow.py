from chains.graph_state import AdvancedRAGGraphState
from langgraph.graph import START, END, StateGraph

from chains.v2_retrieve_node import retrieve_document_node, question_node, llm_answer_node, rerank_node, \
    classify_question_node, filter_node, reorder_node


def init_workflow():
    parent_builder = StateGraph(AdvancedRAGGraphState)
    parent_builder.add_node('Take Question', question_node)
    parent_builder.add_node('Retrieve Document', retrieve_document_node)
    parent_builder.add_node('Reranking', rerank_node)
    parent_builder.add_node('Filter Contexts', filter_node)
    parent_builder.add_node('Reorder Context', reorder_node)
    parent_builder.add_node('Generate Answer', llm_answer_node)

    parent_builder.add_edge(START, 'Take Question')
    parent_builder.add_edge('Take Question', 'Retrieve Document')
    parent_builder.add_edge('Retrieve Document', 'Reranking')

    parent_builder.add_conditional_edges(
        "Reranking",
        classify_question_node,
        {
            "abstract": "Reorder Context",
            "specific": "Filter Contexts",
        }
    )
    parent_builder.add_edge('Filter Contexts', 'Reorder Context')
    parent_builder.add_edge('Reorder Context', 'Generate Answer')
    parent_builder.add_edge('Generate Answer', END)
    return parent_builder.compile()


if __name__ == '__main__':
    output = init_workflow().get_graph(xray=True)
    with open("output_image2.png", "wb") as f:
        f.write(output.draw_mermaid_png())
    # result = init_workflow().invoke({"question": '고환암의 재발과 관련된 정보들을 말씀해주세요',
    #                                  "index_name": 'yunv2'})
    # print(result)
