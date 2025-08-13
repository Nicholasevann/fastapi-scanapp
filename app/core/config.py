from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # App Settings - these can have defaults since they're less likely to change
    PROJECT_NAME: str = "FastAPI Template"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A FastAPI template with authentication and database"
    API_V1_STR: str = "/api/v1"
    
    # Database - no default, must be provided via .env
    DATABASE_URL: str
    
    # Security - no defaults for sensitive values
    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # This can have a default
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # This can have a default
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    OPENAI_API_KEY: str
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True  # Optional: makes env vars case sensitive

settings = Settings()