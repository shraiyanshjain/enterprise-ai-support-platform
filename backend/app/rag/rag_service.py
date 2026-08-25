from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


class RAGService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        query_vector = self.embedding_service.create_embedding(
            query
        )

        return self.vector_store.search(
            query_vector,
            limit,
        )