
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
env_path = Path(__file__).resolve().parent / ".venv-1" / ".env"
load_dotenv(dotenv_path=env_path)

MY_SQL_URL = os.getenv("MY_SQL_URL")

if not MY_SQL_URL:
    raise ValueError("MY_SQL_URL was not found in .env")

# Create MySQL engine
engine = create_engine(MY_SQL_URL, echo=True)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
Base = declarative_base()


# Dependency for getting database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
