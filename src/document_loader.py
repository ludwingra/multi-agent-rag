"""Document loader for multi-domain RAG system.

Handles loading and chunking documents from hr_docs/, tech_docs/, and finance_docs/.
"""

from langchain_core.documents import Document


def load_documents(directory: str) -> list[Document]:
    """Load documents from a directory and return as LangChain Documents."""
    raise NotImplementedError


def chunk_documents(documents: list[Document], chunk_size: int = 500, chunk_overlap: int = 50) -> list[Document]:
    """Split documents into chunks with specified size and overlap."""
    raise NotImplementedError
