"""
Database seed script to create initial users and employees
"""
from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models.user_model import UserModel
from app.models.employee_model import EmployeeModel
from app.utils.hashing import hash_password


def seed_database():
    """Seed the database with initial users and employees"""
    
    # Create tables first
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if users already exist
        existing_users = session.query(UserModel).first()
        if existing_users:
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding database...")
        
        # Create initial users
        users = [
            UserModel(
                name="Admin User",
                email="admin@example.com",
                password_hash=hash_password("admin123"),
                role="admin"
            ),
            UserModel(
                name="HR Manager",
                email="hr@example.com",
                password_hash=hash_password("hr123"),
                role="hr"
            ),
            UserModel(
                name="John Doe",
                email="employee@example.com",
                password_hash=hash_password("emp123"),
                role="employee"
            ),
        ]
        
        for user in users:
            session.add(user)
        
        # Create sample employees
        employees = [
            EmployeeModel(
                name="Alice Johnson",
                department="Engineering",
                job_role="Software Engineer",
                salary=85000.00
            ),
            EmployeeModel(
                name="Bob Smith",
                department="HR",
                job_role="HR Manager",
                salary=75000.00
            ),
            EmployeeModel(
                name="Carol Williams",
                department="Finance",
                job_role="Senior Accountant",
                salary=70000.00
            ),
            EmployeeModel(
                name="David Brown",
                department="Sales",
                job_role="Sales Executive",
                salary=65000.00
            ),
            EmployeeModel(
                name="Eve Davis",
                department="Marketing",
                job_role="Marketing Specialist",
                salary=68000.00
            ),
            EmployeeModel(
                name="Frank Miller",
                department="Engineering",
                job_role="Senior Software Engineer",
                salary=95000.00
            ),
            EmployeeModel(
                name="Grace Wilson",
                department="Engineering",
                job_role="DevOps Engineer",
                salary=90000.00
            ),
            EmployeeModel(
                name="Henry Taylor",
                department="Finance",
                job_role="Financial Analyst",
                salary=72000.00
            ),
        ]
        
        for employee in employees:
            session.add(employee)
        
        session.commit()
        print("Database seeded successfully!")
        print("\nTest Users:")
        print("Admin: admin@example.com / admin123")
        print("HR: hr@example.com / hr123")
        print("Employee: employee@example.com / emp123")


if __name__ == "__main__":
    seed_database()
