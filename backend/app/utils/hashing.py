"""
Password hashing utilities using hashlib with salting
"""
import hashlib
import secrets


def hash_password(password: str) -> str:
    """
    Hash a plain text password with a random salt
    
    Returns: salt$hash format
    """
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}${pwd_hash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hash in format "salt$hash"
    
    Returns:
        True if password matches, False otherwise
    """
    try:
        salt, pwd_hash = hashed_password.split("$")
        computed_hash = hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest()
        return computed_hash == pwd_hash
    except (ValueError, AttributeError):
        return False

# Alias for compatibility with other services
get_password_hash = hash_password
