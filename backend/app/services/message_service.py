from sqlalchemy.orm import Session

from app.models.message import Message
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository


class MessageService:

    def __init__(
        self,
        message_repository: MessageRepository,
        conversation_repository: ConversationRepository,
    ):
        self.message_repository = message_repository
        self.conversation_repository = conversation_repository

    def add_message(
        self,
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:

        conversation = self.conversation_repository.find_by_id(
            db,
            conversation_id,
        )

        if not conversation:
            raise ValueError("Conversation not found")

        return self.message_repository.create(
            db,
            conversation_id,
            role,
            content,
        )

    def get_messages(
        self,
        db: Session,
        conversation_id: int,
    ) -> list[Message]:

        conversation = self.conversation_repository.find_by_id(
            db,
            conversation_id,
        )

        if not conversation:
            raise ValueError("Conversation not found")

        return self.message_repository.find_by_conversation_id(
            db,
            conversation_id,
        )