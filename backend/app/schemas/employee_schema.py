"""
Pydantic schemas for Employee-related requests and responses
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    """Schema for creating a new employee"""
    name: str
    department: str
    job_role: str
    salary: float
    email: str
    password: str
    role: str = "employee"


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee"""
    name: Optional[str] = None
    department: Optional[str] = None
    job_role: Optional[str] = None
    salary: Optional[float] = None


class EmployeeResponse(BaseModel):
    """Full employee response schema (includes salary)"""
    id: int
    name: str
    department: str
    job_role: str
    salary: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EmployeeResponseNoSalary(BaseModel):
    """Employee response schema without salary (for employee role)"""
    id: int
    name: str
    department: str
    job_role: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
