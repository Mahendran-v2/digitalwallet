from __future__ import annotations

import os


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./wallet_system.db")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501").split(",")
        if origin.strip()
    ]


settings = Settings()
