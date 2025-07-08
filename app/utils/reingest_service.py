import os

current_dir = os.path.abspath(__file__)
while not os.path.isdir(os.path.join(current_dir, 'app')):
    current_dir = os.path.dirname(current_dir)
PROJECT_ROOT = current_dir

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "app", "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Import your add_document function from RAG service
from app.services.rag_service import add_document

# Import text extraction functions for each file type
from app.services.ocr_service import extract_text_from_pdf, extract_text_from_image
from app.api.upload import (
    extract_text_from_txt,
    extract_text_from_docx,
    extract_text_from_csv
)

def extract_text_from_file(file_path):
    """
    Determines the file type by extension and extracts text accordingly.
    Returns the extracted text or None if unsupported.
    """
    ext = file_path.lower()
    if ext.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif ext.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(file_path)
    elif ext.endswith(".txt"):
        return extract_text_from_txt(file_path)
    elif ext.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif ext.endswith(".csv"):
        return extract_text_from_csv(file_path)
    else:
        # Unsupported file type
        return None

def reingest_all_documents():
    """
    Scans the upload directory and re-ingests all valid documents.
    """
    for fname in os.listdir(UPLOAD_DIR):
        fpath = os.path.join(UPLOAD_DIR, fname)
        if os.path.isfile(fpath):
            try:
                text = extract_text_from_file(fpath)
                if text and isinstance(text, str) and text.strip():
                    add_document(text, filename=fname)  # Pass filename here!
            except Exception as e:
                print(f"[reingest_service] Failed to process {fname}: {e}")
