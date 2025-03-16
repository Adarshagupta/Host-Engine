from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, JSON, Table
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.db.base import Base

def generate_uuid():
    return str(uuid.uuid4())

# Association table for many-to-many relationship
project_team_members = Table(
    "project_team_members",
    Base.metadata,
    Column("project_id", String, ForeignKey("projects.id")),
    Column("user_id", String, ForeignKey("users.id")),
)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # OAuth info
    github_id = Column(String, nullable=True)
    github_access_token = Column(String, nullable=True)
    
    # Relationships
    owned_projects = relationship("Project", back_populates="owner")
    team_projects = relationship("Project", secondary=project_team_members, back_populates="team_members")
    deployments = relationship("Deployment", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    repository_url = Column(String)
    branch = Column(String, default="main")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Environment variables
    environment_variables = Column(JSON, default=dict)
    
    # Build settings
    build_command = Column(String, nullable=True)
    output_directory = Column(String, default="build")
    
    # Owner
    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="owned_projects")
    
    # Team members
    team_members = relationship("User", secondary=project_team_members, back_populates="team_projects")
    
    # Deployments
    deployments = relationship("Deployment", back_populates="project")
    
    # Domains
    domains = relationship("Domain", back_populates="project")


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(String, primary_key=True, default=generate_uuid)
    commit_hash = Column(String)
    commit_message = Column(Text, nullable=True)
    status = Column(String, default="queued")  # queued, building, ready, failed, canceled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deployment_url = Column(String, nullable=True)
    build_logs = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    project_id = Column(String, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="deployments")
    
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="deployments")


class Domain(Base):
    __tablename__ = "domains"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, index=True)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project_id = Column(String, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="domains") 