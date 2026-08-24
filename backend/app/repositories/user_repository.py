from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def create(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def find_by_email(
        self,
        db: Session,
        email: str
    ) -> User | None:

        statement = select(User).where(User.email == email)

        return db.scalar(statement)

    def find_by_id(
        self,
        db: Session,
        user_id: int
    ) -> User | None:

        statement = select(User).where(User.id == user_id)

        return db.scalar(statement)