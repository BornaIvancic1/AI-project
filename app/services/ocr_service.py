import easyocr
import fitz
from fastapi import  HTTPException
from docx import Document
import pandas as pd

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return text
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
        # Always return as a string, never as dict or DataFrame
        return df.to_string(index=False)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Text extraction failed for CSV: {str(e)}")