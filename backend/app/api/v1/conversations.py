from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)
from app.schemas.message import MessageCreate, MessageResponse
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.repositories.message_repository import MessageRepository

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import AIService
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


repository = ConversationRepository()
service = ConversationService(repository)

message_repository = MessageRepository()

message_service = MessageService(
    message_repository,
    repository,
)
ai_service = AIService()

chat_service = ChatService(
    message_service,
    ai_service,
)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_conversation(
            db,
            conversation_data.user_id,
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    try:
        return service.get_conversation(
            db,
            conversation_id,
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        )


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
):
    try:
        return message_service.add_message(
            db,
            conversation_id,
            message_data.role,
            message_data.content,
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        )


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    try:
        return message_service.get_messages(
            db,
            conversation_id,
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        )

@router.post(
    "/{conversation_id}/chat",
    response_model=ChatResponse,
)
def chat(
    conversation_id: int,
    chat_data: ChatRequest,
    db: Session = Depends(get_db),
):
    try:
        user_message, assistant_message = chat_service.chat(
            db,
            conversation_id,
            chat_data.content,
        )

        return ChatResponse(
            user_message=user_message,
            assistant_message=assistant_message,
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        )