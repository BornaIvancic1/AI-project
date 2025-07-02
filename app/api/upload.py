from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
from app.services.ocr_service import extract_text_from_image, extract_text_from_pdf
from app.storage.storage_service import store_text

UPLOAD_DIR = r"C:\Projekti\AI-project\app\uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        if file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            text = extract_text_from_image(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        store_text(file.filename, text)

        results.append({
            "filename": file.filename,
            "text_excerpt": text[:200]
        })
    return {"uploaded": results}
