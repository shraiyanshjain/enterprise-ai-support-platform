from fastapi import FastAPI

from app.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/")
async def root():
    return {
        "status": "running",
        "application": settings.app_name,
        "version": settings.app_version,
    }