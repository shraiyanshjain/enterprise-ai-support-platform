from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)
from app.schemas.message import MessageCreate, MessageResponse
from app.schemas.chat import ChatRequest, ChatResponse

from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.services.ai_service import AIService
from app.services.chat_service import ChatService

from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.rag_service import RAGService
from app.rag.prompt_builder import PromptBuilder
from app.rag.rag_answer_service import RAGAnswerService

from app.services.tool_calling_service import ToolCallingService
from app.tools.tool_executor import ToolExecutor


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


# ---------------------------------------------------------
# Conversation dependencies
# ---------------------------------------------------------

repository = ConversationRepository()

service = ConversationService(
    repository,
)


# ---------------------------------------------------------
# Message dependencies
# ---------------------------------------------------------

message_repository = MessageRepository()

message_service = MessageService(
    message_repository,
    repository,
)


# ---------------------------------------------------------
# RAG dependencies
# ---------------------------------------------------------

embedding_service = EmbeddingService()

vector_store = VectorStore()

rag_service = RAGService(
    embedding_service,
    vector_store,
)

prompt_builder = PromptBuilder()


# ---------------------------------------------------------
# AI + RAG Answer dependencies
# ---------------------------------------------------------

ai_service = AIService()

rag_answer_service = RAGAnswerService(
    rag_service,
    prompt_builder,
    ai_service,
)


# ---------------------------------------------------------
# Chat service
# ---------------------------------------------------------

tool_executor = ToolExecutor()

tool_calling_service = ToolCallingService(
    ai_service,
    tool_executor,
)

chat_service = ChatService(
    message_service,
    rag_service,
    prompt_builder,
    ai_service,
    tool_calling_service,
)


# =========================================================
# Create conversation
# =========================================================

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


# =========================================================
# Get conversation
# =========================================================

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


# =========================================================
# Add message
# =========================================================

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


# =========================================================
# Get messages
# =========================================================

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


# =========================================================
# AI Chat - RAG + Conversation History
# =========================================================

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
        assistant_message = chat_service.chat(
            db,
            conversation_id,
            chat_data.content,
        )

        return ChatResponse(
            user_message=chat_data.content,
            assistant_message=assistant_message,
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        )