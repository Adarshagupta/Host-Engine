from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.api.schemas.user import User
from app.api.schemas.project import Project


class DeploymentBase(BaseModel):
    commit_hash: str
    commit_message: Optional[str] = None


class DeploymentCreate(DeploymentBase):
    project_id: str


class DeploymentUpdate(BaseModel):
    status: Optional[str] = None
    deployment_url: Optional[str] = None
    build_logs: Optional[str] = None
    error_message: Optional[str] = None


class DeploymentInDBBase(DeploymentBase):
    id: str
    created_at: datetime
    updated_at: datetime
    status: str
    deployment_url: Optional[str] = None
    build_logs: Optional[str] = None
    error_message: Optional[str] = None
    project_id: str
    user_id: str

    class Config:
        orm_mode = True


class Deployment(DeploymentInDBBase):
    project: Project
    user: User


class DeploymentInDB(DeploymentInDBBase):
    pass 