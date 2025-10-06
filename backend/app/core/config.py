from __future__ import annotations
import json
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # DB
    DATABASE_URL: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None

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
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = ["http://localhost", "http://localhost:80"]
    TRUSTED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _parse_cors(cls, v):
        if v is None or v == "": return []
        if isinstance(v, (list, tuple)): return list(v)
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                try: return json.loads(s)
                except Exception: pass
            return [i.strip() for i in s.split(",") if i.strip()]
        return v

    @field_validator("TRUSTED_HOSTS", mode="before")
    @classmethod
    def _parse_hosts(cls, v):
        if v is None or v == "": return ["localhost", "127.0.0.1"]
        if isinstance(v, (list, tuple)): return list(v)
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                try: return json.loads(s)
                except Exception: pass
            return [i.strip() for i in s.split(",") if i.strip()]
        return v

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def _compose_db_url(cls, v, values):
        if v: return v
        pieces = (values.get("DB_USER"), values.get("DB_PASSWORD"), values.get("DB_HOST"),
                  values.get("DB_PORT"), values.get("DB_NAME"))
        if all(pieces):
            return f"postgresql+psycopg://{pieces[0]}:{pieces[1]}@{pieces[2]}:{pieces[3]}/{pieces[4]}"
        return v

settings = Settings()