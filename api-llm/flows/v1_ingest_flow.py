from chains.graph_state import BaseDocumentPreProcessorState
from langgraph.graph import START, END, StateGraph

from chains.v1_prep_node import ocr_node, pdf_to_docs_node, docs_split_node, ingest_node


def init_workflow():
    _workflow = StateGraph(BaseDocumentPreProcessorState)
    _workflow.add_node('Text REC & DET', ocr_node)
    _workflow.add_node('PDF To Documents', pdf_to_docs_node)
    _workflow.add_node('Split Documents Text', docs_split_node)
    _workflow.add_node('Embedding & Save', ingest_node)

    _workflow.add_edge(START, 'Text REC & DET')
    _workflow.add_edge('Text REC & DET', 'PDF To Documents')
    _workflow.add_edge('PDF To Documents', 'Split Documents Text')
    _workflow.add_edge('Split Documents Text', 'Embedding & Save')
    _workflow.add_edge('Embedding & Save', END)

    return _workflow.compile()


if __name__ == '__main__':
    from IPython.display import Image

    output = init_workflow().get_graph(xray=True)
    image = Image(output.draw_mermaid_png())
    with open("output_image.png", "wb") as f:
        f.write(output.draw_mermaid_png())
