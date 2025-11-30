import pytest
import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"

# Helper to generate unique emails
def random_email():
    return f"user_{uuid.uuid4()}@example.com"

@pytest.fixture(scope="module")
def admin_token():
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@example.com", "password": "admin123"})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def hr_token():
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": "hr@example.com", "password": "hr123"})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def employee_token():
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": "employee@example.com", "password": "emp123"})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_admin_can_create_hr(admin_token):
    """Admin should be able to create an HR user"""
    email = random_email()
    payload = {
        "name": "Test HR Created by Admin",
        "email": email,
        "password": "password123",
        "role": "hr",
        "department": "HR",
        "job_role": "Manager",
        "salary": 80000
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(f"{BASE_URL}/employees/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    
    # Verify login
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": "password123"})
    assert login_resp.status_code == 200
    assert login_resp.json()["role"] == "hr"

def test_hr_can_create_employee(hr_token):
    """HR should be able to create an Employee user"""
    email = random_email()
    payload = {
        "name": "Test Employee Created by HR",
        "email": email,
        "password": "password123",
        "role": "employee",
        "department": "Engineering",
        "job_role": "Dev",
        "salary": 60000
    }
    headers = {"Authorization": f"Bearer {hr_token}"}
    response = requests.post(f"{BASE_URL}/employees/", json=payload, headers=headers)
    assert response.status_code == 201
    
    # Verify login
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": "password123"})
    assert login_resp.status_code == 200
    assert login_resp.json()["role"] == "employee"

def test_hr_cannot_create_admin(hr_token):
    """HR should NOT be able to create an Admin user"""
    email = random_email()
    payload = {
        "name": "Illegal Admin",
        "email": email,
        "password": "password123",
        "role": "admin",
        "department": "IT",
        "job_role": "Admin",
        "salary": 100000
    }
    headers = {"Authorization": f"Bearer {hr_token}"}
    response = requests.post(f"{BASE_URL}/employees/", json=payload, headers=headers)
    assert response.status_code == 403
    assert "HR users are only allowed to create Employees" in response.json()["detail"]

def test_hr_cannot_create_hr(hr_token):
    """HR should NOT be able to create another HR user"""
    email = random_email()
    payload = {
        "name": "Illegal HR",
        "email": email,
        "password": "password123",
        "role": "hr",
        "department": "HR",
        "job_role": "Manager",
        "salary": 80000
    }
    headers = {"Authorization": f"Bearer {hr_token}"}
    response = requests.post(f"{BASE_URL}/employees/", json=payload, headers=headers)
    assert response.status_code == 403

def test_employee_cannot_create_anything(employee_token):
    """Employee should NOT be able to create any user"""
    email = random_email()
    payload = {
        "name": "Illegal User",
        "email": email,
        "password": "password123",
        "role": "employee",
        "department": "Sales",
        "job_role": "Rep",
        "salary": 50000
    }
    headers = {"Authorization": f"Bearer {employee_token}"}
    response = requests.post(f"{BASE_URL}/employees/", json=payload, headers=headers)
    assert response.status_code == 403
