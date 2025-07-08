from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os

from app.services.ocr_service import extract_text_from_image, extract_text_from_pdf, extract_text_from_txt, \
    extract_text_from_docx, extract_text_from_csv
from app.storage.storage_service import store_text
from app.services.rag_service import add_document




current_dir = os.path.abspath(__file__)
while not os.path.isdir(os.path.join(current_dir, 'app')):
    current_dir = os.path.dirname(current_dir)
PROJECT_ROOT = current_dir

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "app", "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)


router = APIRouter()



@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        try:
            with open(file_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

        ext = file.filename.lower()
        try:
            if ext.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif ext.endswith((".png", ".jpg", ".jpeg")):
                text = extract_text_from_image(file_path)
            elif ext.endswith(".txt"):
                text = extract_text_from_txt(file_path)
            elif ext.endswith(".docx"):
                text = extract_text_from_docx(file_path)
            elif ext.endswith(".csv"):
                text = extract_text_from_csv(file_path)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Text extraction failed: {str(e)}")

        # Ensure the extracted text is a non-empty string
        if not text or not isinstance(text, str) or not text.strip():
            raise HTTPException(status_code=400, detail="Extracted text is empty or invalid.")

        # Defensive: Ensure text is a string before ingestion
        try:
            if not isinstance(text, str):
                text = str(text)
            add_document(text, filename=file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to ingest document: {str(e)}")

        try:
            store_text(file.filename, text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to store text: {str(e)}")

        results.append({
            "filename": file.filename,
            "text_excerpt": text[:200]
        })
    return {"uploaded": results}
