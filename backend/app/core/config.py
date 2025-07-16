# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings from .env
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "plant_health_db"
    DB_USER: str = "plant_user"
    DB_PASSWORD: str = "plant_password"
    
    # PostgreSQL Admin (for setup)
    POSTGRES_ADMIN_USER: str = "postgres"
    POSTGRES_ADMIN_PASSWORD: str = "admin123"
    
    # App settings
    APP_NAME: str = "Plant Health Monitoring"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from individual components"""
        return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def ADMIN_DATABASE_URL(self) -> str:
        """Construct admin database URL for setup operations"""
        return f"postgres://{self.POSTGRES_ADMIN_USER}:{self.POSTGRES_ADMIN_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/postgres"

# Create global settings instance
settings = Settings()