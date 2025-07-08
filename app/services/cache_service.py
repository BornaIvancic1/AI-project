import os
from redisvl.extensions.cache.embeddings import EmbeddingsCache
import numpy as np

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_NAME = "embedcache"
CACHE_TTL = 3600  # seconds (1 hour), or None for no expiration

# Initialize the Embeddings Cache
cache = EmbeddingsCache(
    name=CACHE_NAME,
    redis_url=REDIS_URL,
    ttl=CACHE_TTL
)

def store_embedding(text, model_name, embedding, metadata=None, ttl=None):
    if not (isinstance(embedding, list) or isinstance(embedding, np.ndarray)):
        raise ValueError(f"Embedding must be a list or numpy array, got {type(embedding)}")
    return cache.set(
        text=text,
        model_name=model_name,
        embedding=embedding,
        metadata=metadata,
        ttl=ttl
    )


def get_embedding(text, model_name):
    """
    Retrieve an embedding from the cache.
    Returns the embedding or None if not found.
    """
    return cache.get(text=text, model_name=model_name)

def embedding_exists(text, model_name):
    """
    Check if an embedding exists in the cache.
    Returns True if exists, False otherwise.
    """
    return cache.exists(text=text, model_name=model_name)

def store_embeddings_batch(batch_items, ttl=None):
    """
    Store multiple embeddings in a batch.
    batch_items: list of dicts with keys 'text', 'model_name', 'embedding', 'metadata'
    Returns a list of cache keys.
    """
    return cache.mset(batch_items, ttl=ttl)

def get_embeddings_batch(texts, model_name):
    """
    Retrieve multiple embeddings in a batch.
    Returns a list of embeddings (or None for missing).
    """
    return cache.mget(texts, model_name)

def drop_embedding(text, model_name):
    """
    Remove an embedding from the cache.
    Returns True if removed, False otherwise.
    """
    return cache.drop(text=text, model_name=model_name)

# Optional: Async wrappers can be added here if needed

if __name__ == "__main__":
    # Example usage
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    text = "Sample document text"
    embedding = [0.1, 0.2, 0.3]  # Replace with your actual embedding
    metadata = {"doc_id": "123", "source": "upload"}

    # Store
    key = store_embedding(text, EMBEDDING_MODEL_NAME, embedding, metadata)
    print(f"Stored with key: {key}")

    # Retrieve
    result = get_embedding(text, EMBEDDING_MODEL_NAME)
    if result:
        print("Found in cache:", result)
    else:
        print("Not found in cache.")
