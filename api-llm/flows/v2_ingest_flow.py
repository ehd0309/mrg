from chains.graph_state import AdvancedDocumentPreprocessorState
from langgraph.graph import START, END, StateGraph

from chains.v2_prep_node import (ocr_node,
                                 text_node,
                                 table_node,
                                 table_summary_node,
                                 de_identify_node,
                                 semantic_text_splitter_node,
                                 gen_keywords_node,
                                 embedding_node,
                                 get_markdown_node,
                                 image_node,
                                 save_image_node,
                                 )


def init_workflow():
    # table_builder = StateGraph(AdvancedDocumentPreprocessorState)
    # table_builder.add_node("Extract Table", table_node)
    # table_builder.add_node("Summarize Table", table_summary_node)
    # table_builder.add_edge(START, "Extract Table")
    # table_builder.add_edge("Extract Table", "Summarize Table")
    # table_graph = table_builder.compile()

    parent_builder = StateGraph(AdvancedDocumentPreprocessorState)
    parent_builder.add_node('OCR', ocr_node)
    parent_builder.add_node('Generate Markdown Format', get_markdown_node)
    parent_builder.add_node('Extract Text', text_node)
    parent_builder.add_node('Extract Table', table_node)
    parent_builder.add_node('Extract Image', image_node)
    parent_builder.add_node('Save Image', save_image_node)
    parent_builder.add_node('Generate Table Summary', table_summary_node)
    parent_builder.add_node('Semantic Chunking', semantic_text_splitter_node)
    parent_builder.add_node('가명화', de_identify_node)
    parent_builder.add_node('키워드 추출', gen_keywords_node)
    parent_builder.add_node('vector&bm25 embedding', embedding_node)

    parent_builder.add_edge(START, 'OCR')
    parent_builder.add_edge('OCR', 'Generate Markdown Format')
    parent_builder.add_edge('Generate Markdown Format', '가명화')
    parent_builder.add_edge('가명화', 'Extract Text')
    parent_builder.add_edge('가명화', 'Extract Table')
    parent_builder.add_edge('가명화', 'Extract Image')
    parent_builder.add_edge('Extract Table', 'Generate Table Summary')
    parent_builder.add_edge('Extract Image', 'Save Image')
    parent_builder.add_edge(['Extract Text', 'Generate Table Summary'], 'Semantic Chunking')
    parent_builder.add_edge('Semantic Chunking', '키워드 추출')
    parent_builder.add_edge('키워드 추출', 'vector&bm25 embedding')
    parent_builder.add_edge('vector&bm25 embedding', END)

    return parent_builder.compile()


if __name__ == '__main__':
    from IPython.display import Image

    output = init_workflow().get_graph(xray=True)
    image = Image(output.draw_mermaid_png())
    with open("output_image.png", "wb") as f:
        f.write(output.draw_mermaid_png())
