from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Shop Floor API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost", "http://localhost:80"]
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 