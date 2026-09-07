import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "TicketPro"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super-secret-key-ticketpro-enterprise-change-in-prod-32bytes"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
    ]

    # Database
    DATABASE_URL: str = "sqlite:///./ticketpro.db"

    # Storage
    UPLOAD_DIR: str = "storage/uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: set = {
        "png", "jpg", "jpeg", "gif", "pdf", "doc", "docx",
        "xls", "xlsx", "txt", "zip", "tar", "gz", "log", "csv"
    }

    # Security & Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 120

    # Email
    EMAIL_PROVIDER: str = "mock"
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "support@ticketpro.internal"
    EMAILS_FROM_NAME: str = "TicketPro Operations"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
