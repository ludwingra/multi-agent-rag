"""Document loader for multi-domain RAG system.

Handles loading and chunking documents from hr_docs/, tech_docs/, and finance_docs/.
"""

from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Maps directory name suffixes to domain labels
_DOMAIN_MAP = {
    "hr_docs": "hr",
    "tech_docs": "tech",
    "finance_docs": "finance",
}


class DocumentLoader:
    """Loads and splits markdown/text documents for multi-domain RAG ingestion."""

    def load_documents(self, directory: str) -> list[Document]:
        """Load all .md and .txt files from *directory*.

        Each returned Document carries two metadata keys:
        - ``source_file``: the filename (not the full path)
        - ``domain``: inferred from the last component of *directory*
          (``hr_docs`` → ``"hr"``, ``tech_docs`` → ``"tech"``,
           ``finance_docs`` → ``"finance"``; unknown dirs keep the dir name)
        """
        dir_path = Path(directory)
        dir_name = dir_path.name
        domain = _DOMAIN_MAP.get(dir_name, dir_name)

        documents: list[Document] = []
        for file_path in sorted(dir_path.glob("*.md")) + sorted(dir_path.glob("*.txt")):
            loader = TextLoader(str(file_path), encoding="utf-8")
            loaded = loader.load()
            for doc in loaded:
                doc.metadata["source_file"] = file_path.name
                doc.metadata["domain"] = domain
            documents.extend(loaded)

        return documents

    def split_documents(
        self,
        documents: list[Document],
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> list[Document]:
        """Split *documents* into chunks using RecursiveCharacterTextSplitter.

        Original metadata is preserved in every chunk.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return splitter.split_documents(documents)

    def load_and_split(self, directory: str, domain: str = "") -> list[Document]:
        """Convenience method: load all files in *directory*, then split.

        Prints stats (number of documents loaded and number of chunks produced).
        The *domain* parameter is accepted for API compatibility but the domain
        is always inferred from the directory name inside :meth:`load_documents`.
        """
        documents = self.load_documents(directory)
        chunks = self.split_documents(documents)

        print(
            f"[DocumentLoader] directory='{directory}' — "
            f"{len(documents)} document(s) loaded, {len(chunks)} chunk(s) generated."
        )
        return chunks


if __name__ == "__main__":
    loader = DocumentLoader()
    for domain_dir in ["data/hr_docs", "data/tech_docs", "data/finance_docs"]:
        chunks = loader.load_and_split(domain_dir)
        # load_and_split ya imprime stats
    print("Document loading complete.")
