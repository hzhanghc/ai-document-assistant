import chromadb


CHROMA_PATH = "data/chroma"


class VectorStore:
    """Manage the ChromaDB vector database."""

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def reset(self) -> None:
        """Delete and recreate the entire document collection."""

        try:
            self.client.delete_collection("documents")
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def delete_document(self, source: str) -> None:
        """
        Delete all chunks belonging to a specific document.
        """

        self.collection.delete(
            where={
                "source": source
            }
        )

    def add_documents(
        self,
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
        ids: list[str]
    ) -> None:
        """Add documents and their embeddings to ChromaDB."""

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5
    ) -> dict:
        """Search for the most similar documents."""

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def count(self) -> int:
        """Return the number of stored documents."""

        return self.collection.count()

    def get_documents(self) -> dict:
        """Return all stored document metadata."""

        return self.collection.get(
            include=["metadatas"]
        )