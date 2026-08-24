from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationRepository:

    def create(
        self,
        db: Session,
        user_id: int,
    ) -> Conversation:

        conversation = Conversation(
            user_id=user_id,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def find_by_id(
        self,
        db: Session,
        conversation_id: int,
    ) -> Conversation | None:

        return (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

    def find_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> list[Conversation]:

        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )