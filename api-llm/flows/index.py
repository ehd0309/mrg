from pathlib import Path
from IPython.display import Image
import base64


def draw_workflow(pre_process_workflow, post_process_workflow, index_name):
    path = Path(__file__).parent.parent / 'assets/outputs' / index_name
    path.mkdir(parents=True, exist_ok=True)  # 경로가 없을 경우 생성

    pre_process_path = path / "pre_process_workflow.png"
    post_process_path = path / "post_process_workflow.png"

    if pre_process_path.exists() and post_process_path.exists():
        return pre_process_path, post_process_path

    output_pre = pre_process_workflow().get_graph(xray=True)
    with open(pre_process_path, "wb") as f:
        f.write(output_pre.draw_mermaid_png())

    output_post = post_process_workflow().get_graph(xray=True)
    with open(post_process_path, "wb") as f:
        f.write(output_post.draw_mermaid_png())

    return pre_process_path, post_process_path


def encode_image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == '__main__':
    from flows.v1_ingest_flow import init_workflow as int
    from flows.v1_retrieve_flow import init_workflow as ret

    res1, res2 = draw_workflow(int, ret, 'yunv1')
    print(res1)
