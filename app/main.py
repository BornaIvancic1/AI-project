from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.utils import indexed_files
from app.utils.reingest_service import reingest_all_documents
from app.api import upload, files, ask

@asynccontextmanager
async def lifespan(app: FastAPI):
    reingest_all_documents()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(indexed_files.router)
app.include_router(files.router)
