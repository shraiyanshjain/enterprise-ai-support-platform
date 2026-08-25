from app.core.openai_client import client


class EmbeddingService:

    def create_embedding(self, text: str) -> list[float]:

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return response.data[0].embedding