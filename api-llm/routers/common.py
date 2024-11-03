from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from utils import check_history_exists, get_existing_keys, get_values_from_history

router = APIRouter(
    prefix="/api/v0",
    tags=["v0"]
)


@router.get("/rags")
async def get_all_indexes():
    return {"keys": get_existing_keys()}


@router.get("/rags/{id}")
async def read_item(id):
    response = get_values_from_history(id)
    return {"info": response}


@router.get("/rags/check")
async def generate(index_name: str):
    return {"exists": check_history_exists(index_name)}