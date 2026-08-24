import bcrypt
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config.settings import settings


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password_bytes,
        salt,
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = (
            datetime.now(timezone.utc)
            + timedelta(
                minutes=settings.jwt_expire_minutes
            )
        )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )