from sqlalchemy.orm import Session

from app.services.ai_service import AIService
from app.services.message_service import MessageService


class ChatService:

    def __init__(
        self,
        message_service: MessageService,
        ai_service: AIService,
    ):
        self.message_service = message_service
        self.ai_service = ai_service

    def chat(
        self,
        db: Session,
        conversation_id: int,
        user_message: str,
    ) -> tuple[str, str]:

        # 1. Save user message
        user_message_obj = self.message_service.add_message(
            db,
            conversation_id,
            "USER",
            user_message,
        )

        # 2. Get conversation history
        messages = self.message_service.get_messages(
            db,
            conversation_id,
        )

        # 3. Convert database messages
        #    into OpenAI message format
        openai_messages = []

        for message in messages:
            role = message.role.lower()

            if role not in ["user", "assistant", "system"]:
                continue

            openai_messages.append(
                {
                    "role": role,
                    "content": message.content,
                }
            )

        # 4. Call OpenAI
        assistant_response = self.ai_service.generate_response(
            openai_messages
        )

        # 5. Save assistant response
        self.message_service.add_message(
            db,
            conversation_id,
            "ASSISTANT",
            assistant_response,
        )

        return user_message_obj.content, assistant_response