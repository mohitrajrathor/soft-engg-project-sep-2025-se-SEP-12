from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database Configuration ---
DATABASE_URL = "sqlite:///./app.db"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Create session factory
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# --- Dependency for FastAPI Routes ---
def get_db():
    """Provide a SQLAlchemy DB session as a dependency."""
    db = session()
    try:
        yield db
    finally:
        db.close()
