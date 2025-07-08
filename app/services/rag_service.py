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
all_chunks = []

def chunk_text(text, chunk_size=500):
    # Simple chunking by character count
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def add_document(text):
    chunks = chunk_text(text)
    if not chunks:
        return
    embeddings = []
    for chunk in chunks:
        if embedding_exists(chunk, EMBEDDING_MODEL_NAME):
            embedding = get_embedding(chunk, EMBEDDING_MODEL_NAME)
        else:
            embedding = embedder.encode([chunk])[0]
            store_embedding(chunk, EMBEDDING_MODEL_NAME, embedding)
        embeddings.append(embedding)
    embeddings = np.asarray(embeddings).astype('float32')
    index.add(embeddings)
    all_chunks.extend(chunks)

def retrieve_relevant_chunks(query, k=3):
    if len(all_chunks) == 0 or index.ntotal == 0:
        return []
    query_embedding = embedder.encode([query])
    query_embedding = np.asarray(query_embedding).astype('float32')
    k = min(k, index.ntotal)
    distances, indices = index.search(query_embedding, k)
    return [all_chunks[i] for i in indices[0] if 0 <= i < len(all_chunks)]
