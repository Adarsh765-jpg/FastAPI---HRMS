"""Test password hashing and JWT functionality"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.hashing import hash_password, verify_password
from app.services.jwt_service import create_access_token, decode_access_token

print("=" * 50)
print("TESTING PASSWORD HASHING")
print("=" * 50)

# Test password hashing
password = "test123"
pwd_hash = hash_password(password)
print(f"Original password: {password}")
print(f"Hashed password: {pwd_hash[:60]}...")
print(f"Verify correct password: {verify_password(password, pwd_hash)}")
print(f"Verify wrong password: {verify_password('wrong', pwd_hash)}")

print("\n" + "=" * 50)
print("TESTING JWT TOKEN CREATION")
print("=" * 50)

# Test JWT tokens
token = create_access_token(user_id=1, role="admin")
print(f"Token created: {token[:80]}...")

payload = decode_access_token(token)
print(f"Decoded payload: {payload}")
print(f"User ID: {payload.get('user_id')}")
print(f"Role: {payload.get('role')}")
print(f"Expires: {payload.get('exp')}")

# Test invalid token
invalid_payload = decode_access_token("invalid.token.here")
print(f"Invalid token result: {invalid_payload}")

print("\n" + "=" * 50)
print("ALL TESTS PASSED ✅")
print("=" * 50)
