"""
Role-based access control utilities
"""
from fastapi import HTTPException, status


def allow_roles(current_user_role: str, *allowed_roles: str) -> None:
    """
    Check if the current user's role is in the allowed roles.
    Raises 403 Forbidden if not authorized.
    
    Args:
        current_user_role: The role of the current user
        *allowed_roles: Variable number of allowed role strings
    
    Raises:
        HTTPException: 403 if user role is not in allowed roles
    """
    if current_user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action"
        )
