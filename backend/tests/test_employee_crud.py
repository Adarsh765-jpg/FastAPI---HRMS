"""Test employee CRUD operations with different roles"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("TESTING EMPLOYEE CRUD API - PHASE 3")
print("=" * 70)

# Get tokens for all three roles
def get_token(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

admin_token = get_token("admin@example.com", "admin123")
hr_token = get_token("hr@example.com", "hr123")
employee_token = get_token("employee@example.com", "emp123")

print(f"Tokens obtained: Admin={bool(admin_token)}, HR={bool(hr_token)}, Employee={bool(employee_token)}\n")

# Test 1: Get all employees (Admin - should see salary)
print("=" * 70)
print("1. GET ALL EMPLOYEES - ADMIN (should see salary)")
print("-" * 70)
headers = {"Authorization": f"Bearer {admin_token}"}
response = requests.get(f"{BASE_URL}/employees/", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Total employees: {data['total']}")
    print(f"   Page: {data['page']}, Limit: {data['limit']}, Total Pages: {data['total_pages']}")
    if data['employees']:
        first_emp = data['employees'][0]
        print(f"   First employee: {first_emp['name']}")
        print(f"   Has salary: {'salary' in first_emp}")
        if 'salary' in first_emp:
            print(f"   Salary: ${first_emp['salary']:,.2f}")

# Test 2: Get all employees (Employee - should NOT see salary)
print("\n" + "=" * 70)
print("2. GET ALL EMPLOYEES - EMPLOYEE (should NOT see salary)")
print("-" * 70)
headers = {"Authorization": f"Bearer {employee_token}"}
response =requests.get(f"{BASE_URL}/employees/", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Total employees: {data['total']}")
    if data['employees']:
        first_emp = data['employees'][0]
        print(f"   First employee: {first_emp['name']}")
        print(f"   Has salary: {'salary' in first_emp}")
        if 'salary' not in first_emp:
            print(f"   ✅ Salary correctly hidden!")

# Test 3: Filter by department
print("\n" + "=" * 70)
print("3. FILTER BY DEPARTMENT - Engineering")
print("-" * 70)
headers = {"Authorization": f"Bearer {admin_token}"}
response = requests.get(f"{BASE_URL}/employees/?department=Engineering", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Found {data['total']} Engineering employees")

# Test 4: Search by name
print("\n" + "=" * 70)
print("4. SEARCH BY NAME - 'Alice'")
print("-" * 70)
response = requests.get(f"{BASE_URL}/employees/?search=Alice", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Found {data['total']} employees matching 'Alice'")
    if data['employees']:
        print(f"   Name: {data['employees'][0]['name']}")

# Test 5: Pagination
print("\n" + "=" * 70)
print("5. PAGINATION - Page 1, Limit 3")
print("-" * 70)
response = requests.get(f"{BASE_URL}/employees/?page=1&limit=3", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Page {data['page']} of {data['total_pages']}")
    print(f"   Showing {len(data['employees'])} of {data['total']} total")

# Test 6: Create employee (Admin - should work)
print("\n" + "=" * 70)
print("6. CREATE EMPLOYEE - ADMIN (should work)")
print("-" * 70)
headers = {"Authorization": f"Bearer {admin_token}"}
new_employee = {
    "name": "Test Employee",
    "email": "test.employee@example.com",
    "password": "test123",
    "role": "employee",
    "department": "QA",
    "job_role": "QA Engineer",
    "salary": 80000.00
}
response = requests.post(f"{BASE_URL}/employees/", json=new_employee, headers=headers)
print(f"Status: {response.status_code}")
test_employee_id = None  # Initialize variable
if response.status_code == 201:
    created = response.json()
    print(f"✅ Employee created with ID: {created['id']}")
    print(f"   Name: {created['name']}, Salary: ${created['salary']:,.2f}")
    test_employee_id = created['id']
elif response.status_code == 200:
    created = response.json()
    print(f"✅ Employee created with ID: {created['id']}")
    test_employee_id = created['id']
else:
    print(f"❌ Failed to create employee: {response.text}")

# Test 7: Create employee (Employee role - should fail)
print("\n" + "=" * 70)
print("7. CREATE EMPLOYEE - EMPLOYEE ROLE (should fail with 403)")
print("-" * 70)
headers = {"Authorization": f"Bearer {employee_token}"}
response = requests.post(f"{BASE_URL}/employees/", json=new_employee, headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 403:
    print(f"✅ Correctly blocked: {response.json()['detail']}")
else:
    print(f"❌ Should have returned 403")

# Test 8: Get single employee by ID
print("\n" + "=" * 70)
print("8. GET SINGLE EMPLOYEE BY ID")
print("-" * 70)
headers = {"Authorization": f"Bearer {admin_token}"}
response = requests.get(f"{BASE_URL}/employees/1", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    emp = response.json()
    print(f"✅ Found employee: {emp['name']}")
    print(f"   Department: {emp['department']}, Role: {emp['job_role']}")

# Test 9: Update employee (HR - should work)
print("\n" + "=" * 70)
print("9. UPDATE EMPLOYEE - HR (should work)")
print("-" * 70)
if test_employee_id:
    headers = {"Authorization": f"Bearer {hr_token}"}
    update_data = {"salary": 85000.00}
    response = requests.put(f"{BASE_URL}/employees/{test_employee_id}", json=update_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        updated = response.json()
        print(f"✅ Employee updated")
        print(f"   New salary: ${updated['salary']:,.2f}")
else:
    print("⚠️ Skipped - no test employee created")

# Test 10: Update employee (Employee role - should fail)
print("\n" + "=" * 70)
print("10. UPDATE EMPLOYEE - EMPLOYEE ROLE (should fail with 403)")
print("-" * 70)
headers = {"Authorization": f"Bearer {employee_token}"}
update_data = {"salary": 85000.00}
response = requests.put(f"{BASE_URL}/employees/1", json=update_data, headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 403:
    print(f"✅ Correctly blocked: {response.json()['detail']}")

# Test 11: Delete employee (Admin - should work)
print("\n" + "=" * 70)
print(f"11. DELETE EMPLOYEE - ADMIN (should work)")
print("-" * 70)
if test_employee_id:
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.delete(f"{BASE_URL}/employees/{test_employee_id}", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 204:
        print(f"✅ Employee deleted successfully")
else:
    print("⚠️ Skipped - no test employee created")

# Test 12: Delete employee (Employee role - should fail)
print("\n" + "=" * 70)
print("12. DELETE EMPLOYEE - EMPLOYEE ROLE (should fail with 403)")
print("-" * 70)
headers = {"Authorization": f"Bearer {employee_token}"}
response = requests.delete(f"{BASE_URL}/employees/1", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 403:
    print(f"✅ Correctly blocked: {response.json()['detail']}")

# Test 13: Get non-existent employee
print("\n" + "=" * 70)
print("13. GET NON-EXISTENT EMPLOYEE (should return 404)")
print("-" * 70)
headers = {"Authorization": f"Bearer {admin_token}"}
response = requests.get(f"{BASE_URL}/employees/99999", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 404:
    print(f"✅ Correctly returned 404: {response.json()['detail']}")

print("\n" + "=" * 70)
print("EMPLOYEE CRUD TESTING COMPLETE")
print("=" * 70)
