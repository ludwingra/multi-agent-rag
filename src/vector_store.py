"""Vector store management for ChromaDB.

Handles creating, persisting, and querying the vector store.
"""

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma


def create_vector_store(documents: list[Document], collection_name: str = "multi_agent_rag") -> Chroma:
    """Create a ChromaDB vector store from documents."""
    raise NotImplementedError


def load_vector_store(collection_name: str = "multi_agent_rag") -> Chroma:
    """Load an existing ChromaDB vector store."""
    raise NotImplementedError
