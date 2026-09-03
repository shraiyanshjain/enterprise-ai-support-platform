from app.rag.prompt_builder import PromptBuilder
from app.rag.rag_service import RAGService
from app.services.ai_service import AIService


class RAGAnswerService:

    def __init__(
        self,
        rag_service: RAGService,
        prompt_builder: PromptBuilder,
        ai_service: AIService,
    ):
        self.rag_service = rag_service
        self.prompt_builder = prompt_builder
        self.ai_service = ai_service

    def answer(
        self,
        question: str,
        limit: int = 5,
        history: list[dict] | None = None,
    ) -> str:

        documents = self.rag_service.search(
            question,
            limit,
        )

        messages = self.prompt_builder.build(
            question=question,
            documents=documents,
            history=history,
        )

        return self.ai_service.generate_response(messages)