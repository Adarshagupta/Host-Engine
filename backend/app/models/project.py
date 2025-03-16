from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base_class import Base


def generate_uuid():
    return str(uuid.uuid4())


class Project(Base):
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    repository_url = Column(String, nullable=False)
    branch = Column(String, default="main")
    build_command = Column(String, nullable=True)
    output_directory = Column(String, default="dist")
    webhook_secret = Column(String, nullable=True)
    environment_variables = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="projects")
    
    deployments = relationship("Deployment", back_populates="project", cascade="all, delete-orphan")
    domains = relationship("Domain", back_populates="project", cascade="all, delete-orphan") 