from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os

from app.services.ocr_service import extract_text_from_image, extract_text_from_pdf
from app.storage.storage_service import store_text
from app.services.rag_service import add_document

from docx import Document
import pandas as pd

UPLOAD_DIR = r"C:\Projekti\AI-project\app\uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Text extraction failed for TXT: {str(e)}")

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Text extraction failed for DOCX: {str(e)}")

def extract_text_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.to_string(index=False)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Text extraction failed for CSV: {str(e)}")

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

        if not text or not isinstance(text, str) or not text.strip():
            raise HTTPException(status_code=400, detail="Extracted text is empty or invalid.")

        try:
            add_document(text)
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
