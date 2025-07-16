# backend/app/core/database.py
from tortoise import Tortoise
import os

from .config import settings

# Resolve database URL:
# 1. Use explicit environment variable DATABASE_URL if provided (e.g. by Docker Compose)
# 2. Fallback to URL assembled from individual DB_* settings

DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

# Tortoise-ORM configuration
TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    }
}

async def init_db():
    """Initialize database connection"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print("Database initialized successfully!")

async def close_db():
    """Close database connection"""
    await Tortoise.close_connections()
    print("Database connection closed!")