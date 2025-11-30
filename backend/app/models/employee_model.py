"""
Employee model for employee management
"""
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class EmployeeModel(SQLModel, table=True):
    """Employee model with all required employee information"""
    
    __tablename__ = "employees"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    department: str = Field(index=True)
    job_role: str = Field(index=True)
    salary: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
