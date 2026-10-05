import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Analyzer & Job Matcher"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security / Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-production-ai-resume-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    # Supports PostgreSQL (postgresql+psycopg2://user:pass@localhost:5432/resumedb)
    # Automatically falls back to local SQLite if postgres url is not set for easy plug & play
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'app.db'}"
    )
    
    # AI Providers & Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    DEFAULT_AI_PROVIDER: str = os.getenv("DEFAULT_AI_PROVIDER", "auto") # auto, openai, gemini, groq, local_nlp
    
    # Uploads
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    MAX_FILE_SIZE_MB: int = 15
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt"]
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure uploads directory exists
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
