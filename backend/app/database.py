"""
Database configuration and session management
"""
from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Create database engine
# Note: For SQLite in production with multiple workers, use external PostgreSQL instead
# or deploy with single worker: gunicorn app.main:app -w 1 ...
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DATABASE_ECHO,  # Configurable via environment
    pool_pre_ping=True  # Verify connections before checkout
)


def create_db_and_tables():
    """Create all database tables"""
    # checkfirst=True prevents "table already exists" errors
    SQLModel.metadata.create_all(engine, checkfirst=True)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
