"""
Employee service layer - Business logic for employee management
"""
from typing import Optional, List, Union
from datetime import datetime, timezone
from sqlmodel import Session, select, or_, col

from app.models.employee_model import EmployeeModel
from app.models.user_model import UserModel
from app.utils.hashing import get_password_hash
from app.schemas.employee_schema import (
    EmployeeCreate, 
    EmployeeUpdate, 
    EmployeeResponse,
    EmployeeResponseNoSalary
)


class EmployeeService:
    """Service class for employee business logic"""
    
    @staticmethod
    def get_all_employees(
        session: Session,
        search: Optional[str] = None,
        department: Optional[str] = None,
        job_role: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        include_salary: bool = True
    ) -> tuple[List[Union[EmployeeResponse, EmployeeResponseNoSalary]], int]:
        """
        Get all employees with optional filtering and pagination.
        
        Args:
            session: Database session
            search: Search query for name
            department: Filter by department
            job_role: Filter by job role
            page: Page number (1-indexed)
            limit: Items per page
            include_salary: Whether to include salary in response
        
        Returns:
            Tuple of (list of employees, total count)
        """
        # Build query
        statement = select(EmployeeModel)
        
        # Apply filters
        if search:
            statement = statement.where(
                EmployeeModel.name.ilike(f"%{search}%")
            )
        
        if department:
            statement = statement.where(EmployeeModel.department == department)
        
        if job_role:
            statement = statement.where(EmployeeModel.job_role == job_role)
        
        # Get total count before pagination (efficient COUNT query)
        from sqlalchemy import func
        count_statement = select(func.count()).select_from(EmployeeModel)
        
        # Apply same filters to count query
        if search:
            count_statement = count_statement.where(
                EmployeeModel.name.ilike(f"%{search}%")
            )
        if department:
            count_statement = count_statement.where(EmployeeModel.department == department)
        if job_role:
            count_statement = count_statement.where(EmployeeModel.job_role == job_role)
        
        total_count = session.exec(count_statement).one()
        
        # Apply pagination
        offset = (page - 1) * limit
        statement = statement.offset(offset).limit(limit)
        
        # Execute query
        employees = session.exec(statement).all()
        
        # Convert to response schemas
        if include_salary:
            response_list = [EmployeeResponse.model_validate(emp) for emp in employees]
        else:
            response_list = [EmployeeResponseNoSalary.model_validate(emp) for emp in employees]
        
        return response_list, total_count
    
    @staticmethod
    def get_employee_by_id(
        session: Session,
        employee_id: int,
        include_salary: bool = True
    ) -> Optional[Union[EmployeeResponse, EmployeeResponseNoSalary]]:
        """
        Get a single employee by ID.
        
        Args:
            session: Database session
            employee_id: Employee ID
            include_salary: Whether to include salary in response
        
        Returns:
            Employee if found, None otherwise
        """
        employee = session.get(EmployeeModel, employee_id)
        
        if employee is None:
            return None
        
        if include_salary:
            return EmployeeResponse.model_validate(employee)
        else:
            return EmployeeResponseNoSalary.model_validate(employee)
    
    @staticmethod
    def create_employee(
        session: Session,
        employee_data: EmployeeCreate
    ) -> EmployeeResponse:
        """
        Create a new employee.
        
        Args:
            session: Database session
            employee_data: Employee creation data
        
        Returns:
            Created employee
        """
        # 1. Create User account first
        password_hash = get_password_hash(employee_data.password)
        
        user = UserModel(
            name=employee_data.name,
            email=employee_data.email,
            password_hash=password_hash,
            role=employee_data.role
        )
        
        session.add(user)
        session.flush()  # Flush to get the user ID if needed (though we don't link them by FK yet)
        
        # 2. Create Employee record
        employee = EmployeeModel(
            name=employee_data.name,
            department=employee_data.department,
            job_role=employee_data.job_role,
            salary=employee_data.salary
        )
        
        session.add(employee)
        session.commit()
        session.refresh(employee)
        
        return EmployeeResponse.model_validate(employee)
    
    @staticmethod
    def update_employee(
        session: Session,
        employee_id: int,
        employee_data: EmployeeUpdate
    ) -> Optional[EmployeeResponse]:
        """
        Update an existing employee.
        
        Args:
            session: Database session
            employee_id: Employee ID
            employee_data: Employee update data
        
        Returns:
            Updated employee if found, None otherwise
        """
        employee = session.get(EmployeeModel, employee_id)
        
        if employee is None:
            return None
        
        # Update only provided fields
        update_data = employee_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(employee, key, value)
        
        # Update timestamp
        employee.updated_at = datetime.now(timezone.utc)
        
        session.add(employee)
        session.commit()
        session.refresh(employee)
        
        return EmployeeResponse.model_validate(employee)
    
    @staticmethod
    def delete_employee(
        session: Session,
        employee_id: int
    ) -> bool:
        """
        Delete an employee.
        
        Args:
            session: Database session
            employee_id: Employee ID
        
        Returns:
            True if deleted, False if not found
        """
        employee = session.get(EmployeeModel, employee_id)
        
        if employee is None:
            return False
        
        session.delete(employee)
        session.commit()
        
        return True
