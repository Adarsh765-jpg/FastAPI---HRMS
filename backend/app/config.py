"""
Application configuration settings
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./hrms.db"
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "monaco"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    class Config:
        env_file = ".env"


settings = Settings()
