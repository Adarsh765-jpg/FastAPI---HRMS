"""
JWT token generation and validation service
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from app.config import settings


def create_access_token(user_id: int, role: str) -> str:
    """
    Create a JWT access token
    
    Args:
        user_id: User's database ID
        role: User's role (admin, hr, employee)
    
    Returns:
        Encoded JWT token string
    """
    expiration = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": expiration
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dict if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
