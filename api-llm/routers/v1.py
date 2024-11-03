from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from utils import check_history_exists, gen_history

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)


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
    if check_history_exists(index_name):
        return HTTPException(status_code=400, detail="already exists")
    from flows.v1_ingest_flow import init_workflow
    ingest = init_workflow()
    result = ingest.invoke({"index_name": index_name})
    gen_history(index_name,
                {"file_name": file_name, "ocr_result_paths": result.get("ocr_result_paths"), "step": result.get("step"),
                 "version": "v1"})
    return {'message': index_name + ' was ingested successfully', 'index_name': index_name}


@router.post("/rags/chat")
async def invoke_chat(invoke_request: InvokeChatRequest):
    from flows.v1_retrieve_flow import init_workflow
    retrieve = init_workflow()

    async def event_stream() -> AsyncGenerator[str, None]:
        async for event in retrieve.astream_events(
                {"question": invoke_request.question, "index_name": invoke_request.index_name}, version="v1",
                stream_mode="answer"):
            kind = event["event"]
            if kind == "on_llm_stream":
                yield f"{event['data']['chunk']}"
            if kind == 'on_llm_end':
                print(event)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
