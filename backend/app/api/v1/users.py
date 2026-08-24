from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


repository = UserRepository()
service = UserService(repository)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.register_user(
            db,
            user_data,
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception),
        )