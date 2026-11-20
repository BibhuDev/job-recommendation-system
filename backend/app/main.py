from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.core.config import settings
from backend.app.db.database import get_db


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Job Search and Recommendation Agent",
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG
)


@app.get("/")
def home():
    return {
        "message": "Welcome to CareerAI!",
        "status": "API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/db-health")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "status": "healthy"
    }
