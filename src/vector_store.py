"""Vector store management for ChromaDB.

Handles creating, persisting, and querying vector stores for multi-domain RAG.
"""

import os

from dotenv import load_dotenv

load_dotenv()

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever


DOMAINS = {
    "hr": ("data/hr_docs", "hr_docs"),
    "tech": ("data/tech_docs", "tech_docs"),
    "finance": ("data/finance_docs", "finance_docs"),
}


class VectorStoreManager:
    """Manages ChromaDB vector stores for multi-domain RAG.

    Supports creating, loading, and querying persistent collections
    for the hr, tech, and finance document domains.
    """

    def __init__(self, persist_directory: str = "./chroma_db") -> None:
        """Initialize OpenAIEmbeddings and store persist_directory.

        Args:
            persist_directory: Path where ChromaDB collections are persisted.
        """
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()

    def create_store(self, documents: list[Document], collection_name: str) -> Chroma:
        """Create a ChromaDB collection from documents and persist to disk.

        Args:
            documents: List of LangChain Document objects to embed and store.
            collection_name: Name of the ChromaDB collection to create.

        Returns:
            A Chroma vector store instance backed by the created collection.
        """
        store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=collection_name,
            persist_directory=self.persist_directory,
        )
        return store

    def load_store(self, collection_name: str) -> Chroma:
        """Load an existing ChromaDB collection from disk.

        Args:
            collection_name: Name of the ChromaDB collection to load.

        Returns:
            A Chroma vector store instance backed by the existing collection.
        """
        store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )
        return store

    def get_retriever(self, collection_name: str, k: int = 4) -> VectorStoreRetriever:
        """Return a similarity-based retriever for the given collection.

        Args:
            collection_name: Name of the ChromaDB collection to retrieve from.
            k: Number of documents to return per query (default 4).

        Returns:
            A VectorStoreRetriever configured for similarity search.
        """
        store = self.load_store(collection_name)
        return store.as_retriever(search_kwargs={"k": k})

    def _collection_exists(self, collection_name: str) -> bool:
        """Check whether a ChromaDB collection already exists on disk.

        A collection is considered to exist when the persist_directory contains
        a non-empty subdirectory or SQLite database file associated with it.
        ChromaDB stores data in a single SQLite file (chroma.sqlite3) at the
        root of persist_directory, so we check for that file as a proxy.

        Args:
            collection_name: Name of the collection to check.

        Returns:
            True if the collection data is present on disk, False otherwise.
        """
        sqlite_path = os.path.join(self.persist_directory, "chroma.sqlite3")
        if not os.path.exists(sqlite_path):
            return False

        # Verify the collection actually has documents by loading it
        try:
            store = self.load_store(collection_name)
            count = store._collection.count()
            return count > 0
        except Exception:
            return False

    def initialize_all_stores(self) -> dict[str, Chroma]:
        """Load all three domain collections, creating them if they do not exist.

        For each domain (hr, tech, finance):
        - If the collection already exists on disk, reload it without re-embedding.
        - If the collection does not exist, load and split the source documents
          using DocumentLoader, then create the collection via create_store().

        Prints stats (collection name and document count) for each domain.

        Returns:
            A dict mapping collection name to its Chroma vector store instance.
            Keys: "hr_docs", "tech_docs", "finance_docs".
        """
        from src.document_loader import DocumentLoader

        loader = DocumentLoader()
        stores: dict[str, Chroma] = {}

        for domain, (directory, collection_name) in DOMAINS.items():
            if self._collection_exists(collection_name):
                print(f"[{collection_name}] Collection found on disk — reloading...")
                store = self.load_store(collection_name)
                count = store._collection.count()
                print(f"[{collection_name}] Loaded {count} chunks.")
            else:
                print(f"[{collection_name}] Collection not found — creating from source docs...")
                documents = loader.load_and_split(directory=directory, domain=domain)
                store = self.create_store(documents=documents, collection_name=collection_name)
                count = store._collection.count()
                print(f"[{collection_name}] Created with {count} chunks.")

            stores[collection_name] = store

        return stores


if __name__ == "__main__":
    manager = VectorStoreManager()
    stores = manager.initialize_all_stores()

    # Smoke test: 1 query por dominio
    test_queries = {
        "hr_docs": "employee benefits and compensation",
        "tech_docs": "API architecture and microservices",
        "finance_docs": "quarterly revenue and budget",
    }

    print("\n--- Smoke Test: Retriever Queries ---")
    for collection_name, query in test_queries.items():
        retriever = manager.get_retriever(collection_name, k=2)
        results = retriever.invoke(query)
        print(f"\n[{collection_name}] Query: '{query}'")
        print(f"  Results: {len(results)} chunks returned")
        for i, doc in enumerate(results):
            preview = doc.page_content[:100].replace('\n', ' ')
            print(f"  Chunk {i+1}: [{doc.metadata.get('source_file', '?')}] {preview}...")

    print("\nSmoke test complete.")
