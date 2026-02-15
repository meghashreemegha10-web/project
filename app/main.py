from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.endpoints import router as api_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Enterprise AI Resume Analyzer API"}
