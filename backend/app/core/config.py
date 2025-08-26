
from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
from typing import Optional, List


class Settings(BaseSettings):
    # Prefer a single DATABASE_URL; fall back to components if provided
    DATABASE_URL: Optional[str] = None

    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Shop Floor API"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:80"]

    # Environment
    ENVIRONMENT: str = "development"

    @model_validator(mode="after")
    def build_database_url(self):
        # If DATABASE_URL is explicitly provided, use it as-is
        if self.DATABASE_URL:
            return self

        # Otherwise, try to build it from components
        required = [self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_NAME]
        if all(required):
            self.DATABASE_URL = (
                f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
            return self

        # If neither DATABASE_URL nor components are present, leave as None; the app can error clearly later.
        return self

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
