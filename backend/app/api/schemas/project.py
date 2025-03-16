from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.api.schemas.user import User


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    repository_url: str
    branch: Optional[str] = "main"
    build_command: Optional[str] = None
    output_directory: Optional[str] = "build"
    environment_variables: Optional[Dict[str, str]] = {}


class ProjectCreate(ProjectBase):
    webhook_secret: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    branch: Optional[str] = None
    build_command: Optional[str] = None
    output_directory: Optional[str] = None
    environment_variables: Optional[Dict[str, str]] = None
    webhook_secret: Optional[str] = None


class ProjectInDBBase(ProjectBase):
    id: str
    webhook_secret: Optional[str] = None
    created_at: datetime
    user_id: str

    class Config:
        orm_mode = True


class Project(ProjectInDBBase):
    pass


class ProjectInDB(ProjectInDBBase):
    pass 