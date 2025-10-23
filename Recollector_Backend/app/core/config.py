import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import EmailStr

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    MESHY_API_KEY: str
    MESHY_API_BASE_URL: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    OUTPUT_DIR: Path = BASE_DIR.parent / "static/models"
    METADATA_DIR: Path = BASE_DIR.parent / "metadata"
    UPLOAD_DIR: Path = BASE_DIR.parent / "uploads"

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_FROM_NAME: str
    
    # Anthropic API for Blender MCP
    ANTHROPIC_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()

os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
os.makedirs(settings.METADATA_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)