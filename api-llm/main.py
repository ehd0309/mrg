from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import v1, v2, common

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(common.router)
app.include_router(v1.router)
app.include_router(v2.router)


@app.get("/")
async def root():
    return {"message": "llm api server"}
