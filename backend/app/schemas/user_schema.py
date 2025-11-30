"""
Pydantic schemas for User-related requests and responses
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema (without password)"""
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str
    role: str
    name: str
    user_id: int
