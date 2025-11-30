"""
Comprehensive backend testing suite - All components
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

print("=" * 80)
print("COMPREHENSIVE BACKEND TESTING - PHASES 1-3")
print("=" * 80)

# Utility functions
def get_token(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_section(name):
    print(f"\n{'=' * 80}")
    print(f"{name}")
    print("-" * 80)

# Initialize test results
tests_passed = 0
tests_failed = 0
test_results = []

def record_test(test_name, passed, details=""):
    global tests_passed, tests_failed
    if passed:
        tests_passed += 1
        status = "✅ PASS"
    else:
        tests_failed += 1
        status = "❌ FAIL"
    test_results.append((test_name, passed, details))
    print(f"{status}: {test_name}")
    if details:
        print(f"   {details}")

# Get tokens
test_section("SECTION 1: AUTHENTICATION")
admin_token = get_token("admin@example.com", "admin123")
hr_token = get_token("hr@example.com", "hr123")
employee_token = get_token("employee@example.com", "emp123")

record_test("Admin login", admin_token is not None)
record_test("HR login", hr_token is not None)
record_test("Employee login", employee_token is not None)

# Test invalid credentials
response = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@example.com", "password": "wrong"})
record_test("Invalid password rejected", response.status_code == 401)

# Test health endpoint
test_section("SECTION 2: HEALTH & BASIC ENDPOINTS")
response = requests.get(f"{BASE_URL}/")
record_test("Health endpoint", response.status_code == 200 and response.json()["status"] == "ok")

# Test protected endpoint without token
response = requests.get(f"{BASE_URL}/me")
record_test("Protected endpoint blocks unauthenticated", response.status_code in [401, 403])

# Test protected endpoint with token
headers = {"Authorization": f"Bearer {admin_token}"}
response = requests.get(f"{BASE_URL}/me", headers=headers)
record_test("Protected endpoint allows authenticated", response.status_code == 200)

# Test employee CRUD operations
test_section("SECTION 3: EMPLOYEE CRUD - ADMIN ROLE")
headers = {"Authorization": f"Bearer {admin_token}"}

# GET all employees
response = requests.get(f"{BASE_URL}/employees/", headers=headers)
record_test("GET all employees", response.status_code == 200)
if response.status_code == 200:
    data = response.json()
    record_test("Response has pagination fields", 
                all(k in data for k in ["employees", "total", "page", "limit", "total_pages"]))
    if data["employees"]:
        record_test("Admin sees salary", "salary" in data["employees"][0])

# GET single employee
response = requests.get(f"{BASE_URL}/employees/1", headers=headers)
record_test("GET employee by ID", response.status_code == 200)

# CREATE employee
new_employee = {
    "name": "Integration Test User",
    "department": "Testing",
    "job_role": "Test Engineer",
    "salary": 75000.00
}
response = requests.post(f"{BASE_URL}/employees/", json=new_employee, headers=headers)
record_test("CREATE employee (admin)", response.status_code in [200, 201])
created_id = None
if response.status_code in [200, 201]:
    created_id = response.json()["id"]

# UPDATE employee
if created_id:
    update_data = {"salary": 80000.00}
    response = requests.put(f"{BASE_URL}/employees/{created_id}", json=update_data, headers=headers)
    record_test("UPDATE employee (admin)", response.status_code == 200)

# DELETE employee
if created_id:
    response = requests.delete(f"{BASE_URL}/employees/{created_id}", headers=headers)
    record_test("DELETE employee (admin)", response.status_code == 204)

test_section("SECTION 4: RBAC - HR ROLE")
headers = {"Authorization": f"Bearer {hr_token}"}

# HR can create
response = requests.post(f"{BASE_URL}/employees/", json=new_employee, headers=headers)
record_test("CREATE employee (hr)", response.status_code in [200, 201])
hr_created_id = None
if response.status_code in [200, 201]:
    hr_created_id = response.json()["id"]

# HR can read with salary
response = requests.get(f"{BASE_URL}/employees/", headers=headers)
if response.status_code == 200:
    data = response.json()
    record_test("HR sees salary", data["employees"] and "salary" in data["employees"][0])

# HR can update
if hr_created_id:
    response = requests.put(f"{BASE_URL}/employees/{hr_created_id}", json={"salary": 82000}, headers=headers)
    record_test("UPDATE employee (hr)", response.status_code == 200)

# HR can delete
if hr_created_id:
    response = requests.delete(f"{BASE_URL}/employees/{hr_created_id}", headers=headers)
    record_test("DELETE employee (hr)", response.status_code == 204)

test_section("SECTION 5: RBAC - EMPLOYEE ROLE")
headers = {"Authorization": f"Bearer {employee_token}"}

# Employee can read
response = requests.get(f"{BASE_URL}/employees/", headers=headers)
record_test("GET employees (employee role)", response.status_code == 200)

# Employee salary hidden
if response.status_code == 200:
    data = response.json()
    record_test("Employee salary hidden", data["employees"] and "salary" not in data["employees"][0])

# Employee cannot create
response = requests.post(f"{BASE_URL}/employees/", json=new_employee, headers=headers)
record_test("CREATE blocked for employee", response.status_code == 403)

# Employee cannot update
response = requests.put(f"{BASE_URL}/employees/1", json={"name": "Test"}, headers=headers)
record_test("UPDATE blocked for employee", response.status_code == 403)

# Employee cannot delete
response = requests.delete(f"{BASE_URL}/employees/1", headers=headers)
record_test("DELETE blocked for employee", response.status_code == 403)

test_section("SECTION 6: FILTERING & SEARCH")
headers = {"Authorization": f"Bearer {admin_token}"}

# Search by name
response = requests.get(f"{BASE_URL}/employees/?search=alice", headers=headers)
record_test("Search by name", response.status_code == 200)
if response.status_code == 200:
    record_test("Search returns results", response.json()["total"] >= 1)

# Filter by department
response = requests.get(f"{BASE_URL}/employees/?department=Engineering", headers=headers)
record_test("Filter by department", response.status_code == 200)
if response.status_code == 200:
    data = response.json()
    record_test("Department filter works", data["total"] >= 1)
    if data["employees"]:
        record_test("All results match department", 
                    all(emp["department"] == "Engineering" for emp in data["employees"]))

# Combined filters
response = requests.get(f"{BASE_URL}/employees/?department=Engineering&search=alice", headers=headers)
record_test("Combined filters", response.status_code == 200)

test_section("SECTION 7: PAGINATION")
# Page 1
response = requests.get(f"{BASE_URL}/employees/?page=1&limit=3", headers=headers)
record_test("Pagination page 1", response.status_code == 200)
if response.status_code == 200:
    data = response.json()
    record_test("Page 1 has correct limit", len(data["employees"]) <= 3)
    record_test("Total pages calculated", data["total_pages"] >= 1)

# Page 2
response = requests.get(f"{BASE_URL}/employees/?page=2&limit=3", headers=headers)
record_test("Pagination page 2", response.status_code == 200)

# Invalid page (should still work, return empty)
response = requests.get(f"{BASE_URL}/employees/?page=999", headers=headers)
record_test("High page number handled", response.status_code == 200)

test_section("SECTION 8: ERROR HANDLING")
# Non-existent employee
response = requests.get(f"{BASE_URL}/employees/99999", headers=headers)
record_test("404 for missing employee", response.status_code == 404)

# Invalid employee ID
response = requests.get(f"{BASE_URL}/employees/abc", headers=headers)
record_test("Invalid ID handled", response.status_code in [400, 422])

# Missing fields in create
response = requests.post(f"{BASE_URL}/employees/", json={"name": "Test"}, headers=headers)
record_test("Missing required fields rejected", response.status_code == 422)

# Update non-existent
response = requests.put(f"{BASE_URL}/employees/99999", json={"name": "Test"}, headers=headers)
record_test("404 on update non-existent", response.status_code == 404)

# Delete non-existent
response = requests.delete(f"{BASE_URL}/employees/99999", headers=headers)
record_test("404 on delete non-existent", response.status_code == 404)

test_section("SECTION 9: SECURITY")
# Test invalid token
headers = {"Authorization": "Bearer invalid.token.here"}
response = requests.get(f"{BASE_URL}/employees/", headers=headers)
record_test("Invalid token rejected",response.status_code == 401)

# Test expired/malformed token
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid"}
response = requests.get(f"{BASE_URL}/employees/", headers=headers)
record_test("Malformed token rejected", response.status_code == 401)

# Test missing Authorization header
response = requests.get(f"{BASE_URL}/employees/")
record_test("Missing auth header rejected", response.status_code in [401, 403])

# Print summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print(f"Total Tests: {tests_passed + tests_failed}")
print(f"Passed: {tests_passed} ✅")
print(f"Failed: {tests_failed} ❌")
print(f"Success Rate: {tests_passed / (tests_passed + tests_failed) * 100:.1f}%")

if tests_failed > 0:
    print("\nFailed Tests:")
    for name, passed, details in test_results:
        if not passed:
            print(f"  ❌ {name}")
            if details:
                print(f"     {details}")

print("\n" + "=" * 80)
if tests_failed == 0:
    print("🎉 ALL TESTS PASSED - BACKEND IS READY!")
else:
    print(f"⚠️  {tests_failed} TEST(S) FAILED - REVIEW NEEDED")
print("=" * 80)
