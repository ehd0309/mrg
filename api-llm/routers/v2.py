from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from langchain_core.outputs.generation import GenerationChunk

import json

from utils.pubsub import RedisPubSub, channels

router = APIRouter(
    prefix="/api/v2",
    tags=["v2"]
)

redis = RedisPubSub()


class GenerateRequest(BaseModel):
    index_name: str
    file_name: str


class InvokeChatRequest(BaseModel):
    question: str
    index_name: str


@router.post("/rags")
async def generate(generate_request: GenerateRequest):
    index_name = generate_request.index_name
    file_name = generate_request.file_name
    from flows.v2_ingest_flow import init_workflow
    ingest = init_workflow()
    ingest.invoke({"index_name": index_name})
    redis.publish(channels.get('document'), json.dumps({
        "status": "embedded",
        "idxName": index_name,
        'name': file_name,
    }))
    return {'message': index_name + ' was ingested successfully', 'index_name': index_name}


@router.post("/rags/chat")
async def invoke_chat(invoke_request: InvokeChatRequest):
    from flows.v2_retrieve_flow import init_workflow
    retrieve = init_workflow()

    async def event_stream() -> AsyncGenerator[str, None]:
        async for event in retrieve.astream_events(
                {"question": invoke_request.question, "index_name": invoke_request.index_name}, version="v2",
                stream_mode="answer"):
            kind = event["event"]
            metadata = event['metadata']
            if kind == "on_llm_stream" and metadata.get('langgraph_node') == "Generate Answer":
                chunk = event['data']['chunk']
                if isinstance(chunk, GenerationChunk):
                    yield f"{chunk.text}"
                else:
                    yield f"{chunk}"
            if kind == 'on_llm_end' and metadata.get('langgraph_node') == "Generate Answer":
                print(event)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/rags/pipeline/{pipeline_id}")
async def load_pipeline(pipeline_id):
    from flows.index import draw_workflow, encode_image_to_base64
    from flows.v2_retrieve_flow import init_workflow as retrieve
    from flows.v2_ingest_flow import init_workflow as ingest
    try:
        pre_path, post_path = draw_workflow(pre_process_workflow=ingest, post_process_workflow=retrieve,
                                            index_name=pipeline_id)
        pre_base64 = encode_image_to_base64(pre_path)
        post_base64 = encode_image_to_base64(post_path)
        return JSONResponse(content={
            "pre_process_image": f"data:image/png;base64,{pre_base64}",
            "post_process_image": f"data:image/png;base64,{post_base64}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config='../logging.conf')
