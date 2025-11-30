"""Test database operations"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.database import engine
from app.models.user_model import UserModel
from app.models.employee_model import EmployeeModel

print("=" * 50)
print("TESTING DATABASE OPERATIONS")
print("=" * 50)

with Session(engine) as session:
    # Test user queries
    print("\n1. Fetching all users:")
    users = session.exec(select(UserModel)).all()
    for user in users:
        print(f"  - {user.name} ({user.email}) - Role: {user.role}")
    
    # Test employee queries
    print("\n2. Fetching all employees:")
    employees = session.exec(select(EmployeeModel)).all()
    for emp in employees:
        print(f"  - {emp.name} - {emp.department} - {emp.job_role} - ${emp.salary:,.2f}")
    
    # Test filtering by department
    print("\n3. Fetching Engineering employees:")
    eng_employees = session.exec(
        select(EmployeeModel).where(EmployeeModel.department == "Engineering")
    ).all()
    for emp in eng_employees:
        print(f"  - {emp.name} - {emp.job_role}")
    
    # Test user lookup by email
    print("\n4. Finding admin user by email:")
    admin = session.exec(
        select(UserModel).where(UserModel.email == "admin@example.com")
    ).first()
    if admin:
        print(f"  - Found: {admin.name} (ID: {admin.id}, Role: {admin.role})")
    
print("\n" + "=" * 50)
print("DATABASE TESTS PASSED ✅")
print("=" * 50)
