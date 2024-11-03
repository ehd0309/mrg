from chains.graph_state import BaseRAGGraphState
from langgraph.graph import START, END, StateGraph

from chains.v1_retrieve_node import retrieve_document_node, question_node, llm_answer_node


def init_workflow():
    _workflow = StateGraph(BaseRAGGraphState)
    _workflow.add_node('Get Question', question_node)
    _workflow.add_node('Retrieve Document', retrieve_document_node)
    _workflow.add_node('Generate Answer', llm_answer_node)

    _workflow.add_edge(START, 'Get Question')
    _workflow.add_edge('Get Question', 'Retrieve Document')
    _workflow.add_edge('Retrieve Document', 'Generate Answer')
    _workflow.add_edge('Generate Answer', END)

    return _workflow.compile()


if __name__ == '__main__':
    from IPython.display import Image

    output = init_workflow().get_graph(xray=True)
    image = Image(output.draw_mermaid_png())
    with open("output_image.png", "wb") as f:
        f.write(output.draw_mermaid_png())
