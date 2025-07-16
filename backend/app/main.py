from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.database import init_db, close_db
from .routers import users, plants, diagnoses

# Database lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("🌱 Plant Health API Started!")
    yield
    # Shutdown
    await close_db()
    print("🌱 Plant Health API Stopped!")

# Create FastAPI instance with lifespan
app = FastAPI(
    title="Plant Health Monitoring API",
    description="API for plant health diagnosis and monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api")
app.include_router(plants.router, prefix="/api")
app.include_router(diagnoses.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Plant Health Monitoring API is running!"}

@app.get("/health")
async def health_check():
    from tortoise import Tortoise
    db_status = "connected" if Tortoise._inited else "disconnected"
    
    return {
        "status": "healthy",
        "service": "plant-health-api",
        "version": "1.0.0",
        "database": db_status
    }