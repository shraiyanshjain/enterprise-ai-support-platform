from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:

        return self.repository.find_by_email(
            db,
            email,
        )

    def register_user(
        self,
        db: Session,
        user_data: UserCreate,
    ) -> User:

        existing_user = self.repository.find_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise ValueError("Email already registered")

        password_hash = hash_password(
            user_data.password
        )

        user = User(
            email=user_data.email,
            password_hash=password_hash,
            full_name=user_data.full_name,
        )

        return self.repository.create(
            db,
            user,
        )

    def login_user(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> str:

        user = self.repository.find_by_email(
            db,
            email,
        )

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return access_token