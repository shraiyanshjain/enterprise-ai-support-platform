from app.rag.chunker import DocumentChunker
from app.rag.document_loader import DocumentLoader
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


class IngestionService:

    def __init__(
        self,
        document_loader: DocumentLoader,
        chunker: DocumentChunker,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self.document_loader = document_loader
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def ingest(
        self,
        file_path: str,
    ) -> int:

        # 1. Load document
        text = self.document_loader.load(file_path)

        # 2. Split document into chunks
        chunks = self.chunker.chunk(text)

        if not chunks:
            return 0

        # 3. Create first embedding
        first_vector = self.embedding_service.create_embedding(
            chunks[0]
        )

        # 4. Create Qdrant collection
        self.vector_store.create_collection(
            vector_size=len(first_vector)
        )

        # 5. Embed and store every chunk
        for chunk in chunks:

            vector = self.embedding_service.create_embedding(
                chunk
            )

            self.vector_store.add_document(
                text=chunk,
                vector=vector,
                source=file_path,
            )

        return len(chunks)