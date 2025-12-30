from __future__ import annotations

import json
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("app.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # DB (primary)
    DATABASE_URL: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None  # keep as str for flexible env inputs

    # DB (fallbacks: standard Postgres envs)
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    # Pooling (override per env)
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Shop Floor API"
    ENVIRONMENT: str = "development"

    # CORS
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = [
        "http://localhost",
        "http://localhost:80",
    ]
    TRUSTED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _parse_cors(cls, v):
        if v is None or v == "":
            return []
        if isinstance(v, (list, tuple)):
            return list(v)
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                try:
                    arr = json.loads(s)
                    return arr if isinstance(arr, list) else []
                except Exception:
                    return []
            return [i.strip() for i in s.split(",") if i.strip()]
        return []

    @field_validator("TRUSTED_HOSTS", mode="before")
    @classmethod
    def _parse_hosts(cls, v):
        if v is None or v == "":
            return ["localhost", "127.0.0.1"]
        if isinstance(v, (list, tuple)):
            return list(v)
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                try:
                    arr = json.loads(s)
                    return arr if isinstance(arr, list) else ["localhost", "127.0.0.1"]
                except Exception:
                    return ["localhost", "127.0.0.1"]
            return [i.strip() for i in s.split(",") if i.strip()]
        return ["localhost", "127.0.0.1"]

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def _compose_db_url(cls, v, info: ValidationInfo):
        # Respect explicit DATABASE_URL
        if isinstance(v, str) and v.strip():
            return v

        data = info.data or {}
        user = data.get("DB_USER") or data.get("POSTGRES_USER")
        password = data.get("DB_PASSWORD") or data.get("POSTGRES_PASSWORD")
        host = data.get("DB_HOST") or data.get("POSTGRES_HOST") or "shopfloor_db"
        port = data.get("DB_PORT") or data.get("POSTGRES_PORT") or 5432
        name = data.get("DB_NAME") or data.get("POSTGRES_DB")

        if user and password and host and name:
            return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"

        # Leave None; caller can emit a clear error later if needed
        return v


settings = Settings()
