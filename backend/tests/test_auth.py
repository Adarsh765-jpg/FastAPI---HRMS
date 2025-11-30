"""Test authentication endpoints"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("TESTING AUTHENTICATION SYSTEM")
print("=" * 60)

# Test 1: Login with admin credentials
print("\n1. Testing Login - Admin User")
print("-" * 60)
login_data = {
    "email": "admin@example.com",
    "password": "admin123"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    token_data = response.json()
    print(f"✅ Login successful!")
    print(f"   Token: {token_data['access_token'][:50]}...")
    print(f"   Role: {token_data['role']}")
    print(f"   Name: {token_data['name']}")
    print(f"   User ID: {token_data['user_id']}")
    admin_token = token_data['access_token']
else:
    print(f"❌ Login failed: {response.json()}")
    admin_token = None

# Test 2: Login with HR credentials
print("\n2. Testing Login - HR User")
print("-" * 60)
login_data = {
    "email": "hr@example.com",
    "password": "hr123"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    token_data = response.json()
    print(f"✅ Login successful!")
    print(f"   Role: {token_data['role']}")
    print(f"   Name: {token_data['name']}")
    hr_token = token_data['access_token']
else:
    print(f"❌ Login failed: {response.json()}")
    hr_token = None

# Test 3: Login with Employee credentials
print("\n3. Testing Login - Employee User")
print("-" * 60)
login_data = {
    "email": "employee@example.com",
    "password": "emp123"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    token_data = response.json()
    print(f"✅ Login successful!")
    print(f"   Role: {token_data['role']}")
    print(f"   Name: {token_data['name']}")
    employee_token = token_data['access_token']
else:
    print(f"❌ Login failed: {response.json()}")
    employee_token = None

# Test 4: Login with wrong password
print("\n4. Testing Login - Wrong Password")
print("-" * 60)
login_data = {
    "email": "admin@example.com",
    "password": "wrongpassword"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status Code: {response.status_code}")
if response.status_code == 401:
    print(f"✅ Correctly rejected invalid credentials")
    print(f"   Error: {response.json()['detail']}")
else:
    print(f"❌ Should have rejected invalid credentials")

# Test 5: Test protected endpoint with valid token
print("\n5. Testing Protected Endpoint - Valid Token")
print("-" * 60)
if admin_token:
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Protected endpoint accessed successfully!")
        print(f"   User: {user_data['name']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Role: {user_data['role']}")
    else:
        print(f"❌ Failed to access protected endpoint")

# Test 6: Test protected endpoint without token
print("\n6. Testing Protected Endpoint - No Token")
print("-" * 60)
response = requests.get(f"{BASE_URL}/me")
print(f"Status Code: {response.status_code}")
if response.status_code == 403:
    print(f"✅ Correctly rejected request without token")
    print(f"   Error: {response.json()['detail']}")
else:
    print(f"Status: May fail with 403 (expected)")

# Test 7: Test protected endpoint with invalid token
print("\n7. Testing Protected Endpoint - Invalid Token")
print("-" * 60)
headers = {"Authorization": "Bearer invalid.token.here"}
response = requests.get(f"{BASE_URL}/me", headers=headers)
print(f"Status Code: {response.status_code}")
if response.status_code == 401:
    print(f"✅ Correctly rejected invalid token")
    print(f"   Error: {response.json()['detail']}")
else:
    print(f"Status Code: {response.status_code}")

print("\n" + "=" * 60)
print("AUTHENTICATION TESTS COMPLETE")
print("=" * 60)
