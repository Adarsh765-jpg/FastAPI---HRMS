"""
Employee router - API endpoints for employee management
"""
from typing import Annotated, Optional, List, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from app.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user_model import UserModel
from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeResponseNoSalary
)
from app.services.employee_service import EmployeeService
from app.utils.role_check import allow_roles

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=dict)
def get_all_employees(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    search: Optional[str] = Query(None, description="Search by employee name"),
    department: Optional[str] = Query(None, description="Filter by department"),
    job_role: Optional[str] = Query(None, description="Filter by job role"),
    page: int = Query(1, ge=1,description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Get all employees with optional filtering and pagination.
    
    **Access:**
    - Admin: Can see all employees with salary
    - HR: Can see all employees with salary
    - Employee: Can see all employees WITHOUT salary
    
    **Query Parameters:**
    - `search`: Search by employee name (case-insensitive)
    - `department`: Filter by specific department
    - `job_role`: Filter by specific job role
    - `page`: Page number (default: 1)
    - `limit`: Items per page (default: 10, max: 100)
    
    **Response:**
    ```json
    {
      "employees": [...],
      "total": 50,
      "page": 1,
      "limit": 10,
      "total_pages": 5
    }
    ```
    """
    # Determine if salary should be included based on role
    include_salary = current_user.role in ["admin", "hr"]
    
    # Get employees from service
    employees, total = EmployeeService.get_all_employees(
        session=session,
        search=search,
        department=department,
        job_role=job_role,
        page=page,
        limit=limit,
        include_salary=include_salary
    )
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit
    
    return {
        "employees": employees,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }


@router.get("/{employee_id}", response_model=Union[EmployeeResponse, EmployeeResponseNoSalary])
def get_employee(
    employee_id: int,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Get a single employee by ID.
    
    **Access:**
    - Admin: Can see employee with salary
    - HR: Can see employee with salary
    - Employee: Can see employee WITHOUT salary
    """
    # Determine if salary should be included based on role
    include_salary = current_user.role in ["admin", "hr"]
    
    # Get employee from service
    employee = EmployeeService.get_employee_by_id(
        session=session,
        employee_id=employee_id,
        include_salary=include_salary
    )
    
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )
    
    return employee


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee_data: EmployeeCreate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Create a new employee AND a corresponding user account.
    
    **Access:** 
    - Admin: Can create Admin, HR, or Employee
    - HR: Can create Employee ONLY
    
    **Request Body:**
    ```json
    {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "password": "securepassword",
      "role": "employee",
      "department": "Engineering",
      "job_role": "Software Engineer",
      "salary": 90000.00
    }
    ```
    """
    # Check authorization - only admin and hr can create
    allow_roles(current_user.role, "admin", "hr")
    
    # RBAC Enforcement: HR can ONLY create "employee" role
    if current_user.role == "hr" and employee_data.role != "employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="HR users are only allowed to create Employees. You cannot create Admin or HR users."
        )
    
    # Create employee via service
    employee = EmployeeService.create_employee(
        session=session,
        employee_data=employee_data
    )
    
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Update an existing employee.
    
    **Access:** Admin, HR only
    
    **Request Body:**
    ```json
    {
      "name": "Jane Smith",
      "department": "Engineering",
      "salary": 95000.00
    }
    ```
    
    Note: All fields are optional. Only provided fields will be updated.
    """
    # Check authorization - only admin and hr can update
    allow_roles(current_user.role, "admin", "hr")
    
    # Update employee via service
    employee = EmployeeService.update_employee(
        session=session,
        employee_id=employee_id,
        employee_data=employee_data
    )
    
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )
    
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Delete an employee.
    
    **Access:** Admin, HR only
    """
    # Check authorization - only admin and hr can delete
    allow_roles(current_user.role, "admin", "hr")
    
    # Delete employee via service
    success = EmployeeService.delete_employee(
        session=session,
        employee_id=employee_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )
    
    return None
