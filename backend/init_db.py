import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User, Project, Deployment, Domain
from app.core.config import settings

def init_db():
    """Initialize the database with necessary tables."""
    try:
        # Create engine
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return False

if __name__ == "__main__":
    # Add the current directory to system path for module imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    init_db() 