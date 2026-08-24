from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.conversations import router as conversations_router


app = FastAPI(
    title="Enterprise AI Support Platform",
)


app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(conversations_router)