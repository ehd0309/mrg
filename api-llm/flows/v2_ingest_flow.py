from chains.graph_state import AdvancedDocumentPreprocessorState
from langgraph.graph import START, END, StateGraph

from chains.v2_prep_node import (ocr_node,
                                 text_node,
                                 table_node,
                                 table_summary_node,
                                 de_identify_node,
                                 semantic_text_splitter_node,
                                 merge_documents_node,
                                 gen_keywords_node,
                                 embedding_node,
                                 get_markdown_node
                                 )


def init_workflow():
    _workflow = StateGraph(AdvancedDocumentPreprocessorState)
    _workflow.add_node('Text REC&DET + Layout DET', ocr_node)
    _workflow.add_node('Generate Markdown Format', get_markdown_node)
    _workflow.add_node('Extract Text', text_node)
    _workflow.add_node('Extract Table', table_node)
    _workflow.add_node('Generate Table Summary', table_summary_node)
    _workflow.add_node('Semantic Chunking', semantic_text_splitter_node)
    _workflow.add_node('Merge Document', merge_documents_node)
    _workflow.add_node('가명화', de_identify_node)
    _workflow.add_node('키워드 추출', gen_keywords_node)
    _workflow.add_node('벡터 임베딩(dense+BM25)', embedding_node)

    _workflow.add_edge(START, 'Text REC&DET + Layout DET')
    _workflow.add_edge('Text REC&DET + Layout DET', 'Generate Markdown Format')
    _workflow.add_edge('Generate Markdown Format', 'Extract Text')
    _workflow.add_edge('Generate Markdown Format', 'Extract Table')
    _workflow.add_edge('Extract Table', 'Generate Table Summary')
    _workflow.add_edge('Extract Text', 'Semantic Chunking')
    _workflow.add_edge('Generate Table Summary', 'Merge Document')
    _workflow.add_edge('Semantic Chunking', 'Merge Document')
    _workflow.add_edge('Merge Document', '가명화')
    _workflow.add_edge('가명화', '키워드 추출')
    _workflow.add_edge('키워드 추출', '벡터 임베딩(dense+BM25)')
    _workflow.add_edge('벡터 임베딩(dense+BM25)', END)

    return _workflow.compile()


if __name__ == '__main__':
    from IPython.display import Image

    output = init_workflow().get_graph(xray=True)
    image = Image(output.draw_mermaid_png())
    with open("output_image.png", "wb") as f:
        f.write(output.draw_mermaid_png())
