# File that we'll import engine and session from
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from config import PROJECT_ROOT, DATABASE_SUBDIRECTORY, DATABASE_FILENAME

# Construct the database path using configuration from config.py
db_path = os.path.join(PROJECT_ROOT, DATABASE_SUBDIRECTORY, DATABASE_FILENAME)

# Create an engine that'll setup a database in the assets folder
# To enable SQLAlchemy logging, set echo=True (e.g., for debugging)
engine = create_engine(f"sqlite:///{db_path}", echo=False)

# Create a configured "Session" class
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Provides a new database session."""
    return _SessionLocal()

# For components that might still expect a global session (legacy use, try to refactor)
# This is not recommended for new code. Use get_session() instead.
session = get_session()
