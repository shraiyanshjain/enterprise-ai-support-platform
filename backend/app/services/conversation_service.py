from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:

    def __init__(
        self,
        repository: ConversationRepository,
    ):
        self.repository = repository

    def create_conversation(
        self,
        db: Session,
        user_id: int,
    ) -> Conversation:

        return self.repository.create(
            db,
            user_id,
        )

    def get_conversation(
        self,
        db: Session,
        conversation_id: int,
    ) -> Conversation:

        conversation = self.repository.find_by_id(
            db,
            conversation_id,
        )

        if not conversation:
            raise ValueError("Conversation not found")

        return conversation

    def get_user_conversations(
        self,
        db: Session,
        user_id: int,
    ) -> list[Conversation]:

        return self.repository.find_by_user_id(
            db,
            user_id,
        )