from fastapi import APIRouter, HTTPException

# Import or reference all_chunks from your RAG/indexing module
from app.services.rag_service import all_chunks

router = APIRouter()

@router.get("/indexed_files")
def get_indexed_files():
    """
    Returns a list of unique filenames that have been successfully ingested and indexed for QA.
    """
    try:
        # Ensure all_chunks is not empty and contains 'filename' keys
        files = set(chunk.get('filename') for chunk in all_chunks if chunk.get('filename'))
        return {"indexed_files": list(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving indexed files: {e}")
