import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import User
from app.core.config import settings
from app.api.crud.user import create
from app.db.base import SessionLocal
from app.api.schemas.user import UserCreate

def create_superuser():
    """Create a superuser for the application."""
    try:
        db = SessionLocal()
        
        # Check if superuser already exists
        superuser = db.query(User).filter(User.email == "admin@example.com").first()
        if superuser:
            print("Superuser already exists!")
            return True
            
        # Create superuser
        user_in = UserCreate(
            email="admin@example.com",
            username="admin",
            password="adminpassword",
            is_superuser=True,
        )
        
        user = create(db, obj_in=user_in)
        print(f"Superuser created successfully: {user.email}")
        return True
    except Exception as e:
        print(f"Error creating superuser: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # Add the current directory to system path for module imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    create_superuser() 