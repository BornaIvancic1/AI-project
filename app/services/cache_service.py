import os
from redisvl.extensions.cache.embeddings import EmbeddingsCache

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
    """
    Store an embedding in the cache.
    """
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
    Returns None if not found.
    """
    return cache.get(text=text, model_name=model_name)

def embedding_exists(text, model_name):
    """
    Check if an embedding exists in the cache.
    """
    return cache.exists(text=text, model_name=model_name)

def store_embeddings_batch(batch_items, ttl=None):
    """
    Store multiple embeddings in a batch.
    batch_items: list of dicts with keys 'text', 'model_name', 'embedding', 'metadata'
    """
    return cache.mset(batch_items, ttl=ttl)

def get_embeddings_batch(texts, model_name):
    """
    Retrieve multiple embeddings in a batch.
    """
    return cache.mget(texts, model_name)

def drop_embedding(text, model_name):
    """
    Remove an embedding from the cache.
    """
    cache.drop(text=text, model_name=model_name)

# Optional: Async wrappers can be added here if needed

if __name__ == "__main__":
    # Example usage
    text = "Sample document text"
    model_name = "your-embedding-model"
    embedding = [0.1, 0.2, 0.3]  # Replace with your actual embedding
    metadata = {"doc_id": "123", "source": "upload"}

    # Store
    key = store_embedding(text, model_name, embedding, metadata)
    print(f"Stored with key: {key}")

    # Retrieve
    result = get_embedding(text, model_name)
    if result:
        print("Found in cache:", result)
    else:
        print("Not found in cache.")
