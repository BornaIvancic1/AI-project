from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from app.services.cache_service import embedding_exists, get_embedding, store_embedding

# Use the actual model name as a constant
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

# Initialize embedding model and FAISS index at module level
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
dimension = embedder.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)
all_chunks = []  # Each item: {"filename": ..., "text": ...}

def chunk_text(text, chunk_size=500):
    """Splits text into chunks of specified character length."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def add_document(text, filename=None):
    if not isinstance(text, str):
        raise ValueError(f"add_document expected a string, got {type(text)}: {text}")
    chunks = chunk_text(text)
    if not chunks:
        return
    embeddings = []
    for chunk in chunks:
        # If chunk is a dict (with filename and text), extract just the text for embedding
        if isinstance(chunk, dict):
            text_for_embedding = chunk["text"]
            fname = chunk.get("filename")
        else:
            text_for_embedding = chunk
            fname = filename  # fallback

        # Only pass the text to the embedder
        embedding = embedder.encode([text_for_embedding])[0]
        embeddings.append(embedding)
        # Store filename and text for debugging/traceability
        all_chunks.append({"filename": fname, "text": text_for_embedding})
    embeddings = np.asarray(embeddings).astype('float32')
    index.add(embeddings)

def retrieve_relevant_chunks(query, k=3):
    """
    Retrieves the k most relevant chunks for the query using FAISS.
    Returns a list of chunk dicts: {"filename": ..., "text": ...}
    """
    if len(all_chunks) == 0 or index.ntotal == 0:
        return []
    query_embedding = embedder.encode([query])
    query_embedding = np.asarray(query_embedding).astype('float32')
    k = min(k, index.ntotal)
    distances, indices = index.search(query_embedding, k)
    return [all_chunks[i] for i in indices[0] if 0 <= i < len(all_chunks)]
