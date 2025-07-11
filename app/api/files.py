from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os

current_dir = os.path.abspath(__file__)
while not os.path.isdir(os.path.join(current_dir, 'app')):
    current_dir = os.path.dirname(current_dir)
PROJECT_ROOT = current_dir

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "app", "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

class FileInfo(BaseModel):
    filename: str
    size: int  # size in bytes

class FilesResponse(BaseModel):
    files: List[FileInfo]

@router.get("/files", response_model=FilesResponse)
async def get_all_files():
    try:
        files = []
        for fname in os.listdir(UPLOAD_DIR):
            fpath = os.path.join(UPLOAD_DIR, fname)
            if os.path.isfile(fpath):
                files.append(FileInfo(filename=fname, size=os.path.getsize(fpath)))
        return FilesResponse(files=files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not list files: {str(e)}")
