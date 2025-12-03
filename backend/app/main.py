"""
Main FastAPI application entry point
"""
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import create_db_and_tables
from app.seed_data import seed_database
from app.routers import auth_router, employee_router
from app.dependencies.auth import get_current_user
from app.models.user_model import UserModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    print("🚀 Starting up application...")
    create_db_and_tables()
    seed_database()
    print("✅ Database initialized")
    yield
    print("🛑 Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="HRMS Employee Management API",
    description="Production-ready HRMS with JWT Auth and RBAC",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "HRMS Employee Management API is running",
        "version": "1.0.0"
    }


# Include routers
app.include_router(auth_router.router)
app.include_router(employee_router.router)


# Test protected endpoint
@app.get("/me", tags=["User"])
def get_my_profile(current_user: Annotated[UserModel, Depends(get_current_user)]):
    """
    Test endpoint to verify authentication.
    Returns the current user's profile.
    Requires: Authorization header with Bearer token
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

