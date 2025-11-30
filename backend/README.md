# HRMS Backend API

A robust FastAPI-based backend for the Employee Management System, featuring strict Role-Based Access Control (RBAC), JWT Authentication, and SQLite database.

## 🚀 Features

- **Authentication:** JWT-based login with secure password hashing (bcrypt).
- **RBAC:** Strict role enforcement:
  - **Admin:** Full access (Create Admin, HR, Employee).
  - **HR:** Restricted access (Can ONLY create Employees).
  - **Employee:** Read-only access to own data (Salaries hidden).
- **Employee Management:** CRUD operations with filtering, searching, and pagination.
- **User Management:** Automatic user account creation when adding employees.

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite (with SQLModel/SQLAlchemy)
- **Validation:** Pydantic
- **Security:** Passlib (bcrypt), PyJWT

## 📦 Setup & Installation

1.  **Prerequisites:** Python 3.10+

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Server:**
    ```bash
    # Using the helper script (Windows)
    .\start.bat

    # OR manually
    python -m uvicorn app.main:app --reload
    ```
    Server will start at `http://127.0.0.1:8000`.

## 🔑 API Documentation

Once running, visit the interactive Swagger UI:
👉 **http://127.0.0.1:8000/docs**

### Key Endpoints

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/login` | Login & get Token | Public |
| `GET` | `/employees/` | List employees | Auth Required |
| `POST` | `/employees/` | Create Employee + User | Admin/HR* |
| `PUT` | `/employees/{id}` | Update Employee | Admin/HR |
| `DELETE` | `/employees/{id}` | Delete Employee | Admin |

*\*HR can only create 'Employee' role users.*

## 🧪 Testing

Run the test suite to verify RBAC rules:

```bash
# Install pytest if needed
pip install pytest httpx

# Run tests
python -m pytest test_rbac_enhanced.py -v
```

## 🔒 Default Users (Seed Data)

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@example.com` | `admin123` |
| **HR** | `hr@example.com` | `hr123` |
| **Employee** | `employee@example.com` | `emp123` |
