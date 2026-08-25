from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config.settings import settings


COLLECTION_NAME = "enterprise_support_knowledge"


class VectorStore:

    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url
        )

    def create_collection(
        self,
        vector_size: int,
    ):
        collections = self.client.get_collections()

        collection_exists = any(
            collection.name == COLLECTION_NAME
            for collection in collections.collections
        )

        if not collection_exists:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add_document(
        self,
        text: str,
        vector: list[float],
        source: str,
    ):

        point = PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload={
                "text": text,
                "source": source,
            },
        )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point],
        )

    def search(
    self,
    vector: list[float],
    limit: int = 5,
    ) -> list[dict]:
        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=limit,
            with_payload=True,
        ).points

        return [
            {
                "text": result.payload.get("text"),
                "source": result.payload.get("source"),
                "score": result.score,
            }
            for result in results
        ]