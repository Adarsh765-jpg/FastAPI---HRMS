"""
Authentication dependencies for protected routes
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from app.database import get_session
from app.models.user_model import UserModel
from app.services.jwt_service import decode_access_token

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session)]
) -> UserModel:
    """
    Dependency to get the current authenticated user from JWT token.
    
    This validates the JWT token and retrieves the user from database.
    Used in all protected routes.
    
    Args:
        credentials: HTTP Authorization header with Bearer token
        session: Database session
    
    Returns:
        UserModel: The authenticated user
    
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    token = credentials.credentials
    
    # Decode and validate token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    
    # Extract user_id from payload
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    
    # Fetch user from database
    user = session.get(UserModel, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    
    return user
