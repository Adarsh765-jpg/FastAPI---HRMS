"""Test edge cases and potential issues in Phase 2"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("PHASE 2 EDGE CASE TESTING")
print("=" * 60)

# Test 1: Login with empty credentials
print("\n1. Testing Login - Empty Email")
print("-" * 60)
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "", "password": "test"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Login with malformed email
print("\n2. Testing Login - Malformed Email")
print("-" * 60)
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "not-an-email", "password": "test"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Login without email field
print("\n3. Testing Login - Missing Email Field")
print("-" * 60)
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"password": "test"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Non-existent user
print("\n4. Testing Login - Non-existent User")
print("-" * 60)
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "nonexistent@example.com", "password": "test123"}
)
print(f"Status Code: {response.status_code}")
if response.status_code == 401:
    print(f"✅ Correctly rejected non-existent user")
else:
    print(f"⚠️  Unexpected status code")

# Test 5: SQL Injection attempt
print("\n5. Testing Login - SQL Injection Attempt")
print("-" * 60)
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin' OR '1'='1", "password": "anything"}
)
print(f"Status Code: {response.status_code}")
if response.status_code == 401:
    print(f"✅ Safe from basic SQL injection")
else:
    print(f"⚠️  May be vulnerable")

# Test 6: XSS attempt in email
print("\n6. Testing Login - XSS Attempt")
print("-" * 60)
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "<script>alert('xss')</script>@test.com", "password": "test"}
)
print(f"Status Code: {response.status_code}")
print(f"Response handled: {response.status_code in [400, 401, 422]}")

# Test 7: Very long password
print("\n7. Testing Login - Very Long Password")
print("-" * 60)
long_password = "a" * 10000
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin@example.com", "password": long_password}
)
print(f"Status Code: {response.status_code}")
print(f"Handled correctly: {response.status_code == 401}")

# Test 8: Case sensitivity in email
print("\n8. Testing Login - Email Case Sensitivity")
print("-" * 60)
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "ADMIN@EXAMPLE.COM", "password": "admin123"}
)
print(f"Status Code: {response.status_code}")
if response.status_code == 401:
    print(f"✅ Email is case-sensitive (secure)")
elif response.status_code == 200:
    print(f"⚠️  Email is case-insensitive (may want case-insensitive emails)")

# Test 9: Get valid token and test token expiry validation
print("\n9. Testing - Token Structure")
print("-" * 60)
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin@example.com", "password": "admin123"}
)
if response.status_code == 200:
    token = response.json()["access_token"]
    parts = token.split(".")
    print(f"Token parts count: {len(parts)}")
    print(f"✅ Valid JWT structure (3 parts)" if len(parts) == 3 else "❌ Invalid JWT")

# Test 10: Protected endpoint with Bearer prefix missing
print("\n10. Testing - Token without Bearer prefix")
print("-" * 60)
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin@example.com", "password": "admin123"}
)
if response.status_code == 200:
    token = response.json()["access_token"]
    # Send token without "Bearer " prefix
    headers = {"Authorization": token}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Properly requires 'Bearer' prefix: {response.status_code in [401, 403]}")

print("\n" + "=" * 60)
print("EDGE CASE TESTING COMPLETE")
print("=" * 60)
