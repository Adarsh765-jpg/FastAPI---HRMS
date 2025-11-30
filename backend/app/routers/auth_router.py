"""
Authentication router for login endpoint
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user_model import UserModel
from app.schemas.user_schema import UserLogin, TokenResponse
from app.services.jwt_service import create_access_token
from app.utils.hashing import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: UserLogin,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Login endpoint - authenticate user and return JWT token.
    
    Request body:
    ```json
    {
      "email": "admin@example.com",
      "password": "admin123"
    }
    ```
    
    Response:
    ```json
    {
      "access_token": "eyJ...",
      "token_type": "bearer",
      "role": "admin",
      "name": "Admin User",
      "user_id": 1
    }
    ```
    
    Args:
        credentials: Email and password
        session: Database session
    
    Returns:
        TokenResponse with JWT token and user info
    
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Find user by email
    statement = select(UserModel).where(UserModel.email == credentials.email)
    user = session.exec(statement).first()
    
    # Check if user exists and password is correct
    if user is None or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create JWT token
    access_token = create_access_token(user_id=user.id, role=user.role)
    
    # Return token response
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        name=user.name,
        user_id=user.id
    )
