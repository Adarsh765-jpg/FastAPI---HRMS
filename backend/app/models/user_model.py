"""
User model for authentication and RBAC
"""
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class UserModel(SQLModel, table=True):
    """User model with authentication and role information"""
    
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="employee")  # admin | hr | employee
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
