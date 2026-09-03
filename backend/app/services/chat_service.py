from app.rag.rag_service import RAGService
from app.rag.prompt_builder import PromptBuilder
from app.services.ai_service import AIService
from app.services.tool_calling_service import ToolCallingService


class ChatService:

    def __init__(
        self,
        message_service,
        rag_service: RAGService,
        prompt_builder: PromptBuilder,
        ai_service: AIService,
        tool_calling_service: ToolCallingService,
    ):
        self.message_service = message_service
        self.rag_service = rag_service
        self.prompt_builder = prompt_builder
        self.ai_service = ai_service
        self.tool_calling_service = tool_calling_service

    def chat(
        self,
        db,
        conversation_id: int,
        user_content: str,
    ):

        # 1. Save user message
        self.message_service.add_message(
            db,
            conversation_id=conversation_id,
            role="USER",
            content=user_content,
        )

        # 2. Load conversation history
        messages = self.message_service.get_messages(
            db,
            conversation_id,
        )

        # 3. Convert previous messages to OpenAI format
        history = []

        for message in messages[:-1]:
            role = message.role.lower()

            if role in ("user", "assistant", "system"):
                history.append(
                    {
                        "role": role,
                        "content": message.content,
                    }
                )

        # 4. Retrieve relevant knowledge
        documents = self.rag_service.search(
            user_content,
            limit=5,
        )

        # 5. Build prompt
        prompt_messages = self.prompt_builder.build(
            question=user_content,
            documents=documents,
            history=history,
        )

        # 6. Let the LLM decide whether a tool is needed
        assistant_response = self.tool_calling_service.process(
            prompt_messages
        )

        # 7. Save assistant response
        self.message_service.add_message(
            db,
            conversation_id=conversation_id,
            role="ASSISTANT",
            content=assistant_response,
        )

        return assistant_response