import os
from typing import List
from langchain_openai import OpenAIEmbeddings

# Note: In a real environment, you would instantiate this with your OpenAI API key
# passed via environment variables (e.g., OPENAI_API_KEY).
# For local dev without a key, you could swap this for HuggingFaceEmbeddings.

def get_embeddings_model():
    """
    Returns the configured embeddings model.
    Using text-embedding-ada-002 as standard for 1536 dimensions.
    """
    # Assuming OPENAI_API_KEY is in the environment
    return OpenAIEmbeddings(model="text-embedding-ada-002")

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of text chunks.
    """
    model = get_embeddings_model()
    return model.embed_documents(texts)
    
def generate_query_embedding(query: str) -> List[float]:
    """
    Generates an embedding for a single search query.
    """
    model = get_embeddings_model()
    return model.embed_query(query)
