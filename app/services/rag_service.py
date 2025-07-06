from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize embedding model and FAISS index at module level
embedder = SentenceTransformer('all-MiniLM-L6-v2')
dimension = embedder.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)
all_chunks = []

def add_document(text):
    # Split text into chunks
    chunks = chunk_text(text)
    if not chunks:
        return
    embeddings = embedder.encode(chunks)
    # Ensure embeddings are 2D numpy arrays of type float32
    embeddings = np.asarray(embeddings).astype('float32')
    index.add(embeddings)
    all_chunks.extend(chunks)

def retrieve_relevant_chunks(query, k=3):
    if len(all_chunks) == 0 or index.ntotal == 0:
        return []
    query_embedding = embedder.encode([query])
    # Ensure correct shape and dtype
    query_embedding = np.asarray(query_embedding).astype('float32')
    # Limit k to the number of available chunks
    k = min(k, index.ntotal)
    distances, indices = index.search(query_embedding, k)
    # Only return valid indices
    return [all_chunks[i] for i in indices[0] if 0 <= i < len(all_chunks)]


def chunk_text(text, chunk_size=500):
    # Simple chunking by character count
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
