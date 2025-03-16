from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import crud
from app.api.deps import get_current_active_user
from app.api.schemas.deployment import Deployment, DeploymentCreate, DeploymentUpdate
from app.db.base import get_db
from app.db.models import User
from app.workers.tasks import deploy_project

router = APIRouter()


@router.get("/", response_model=List[Deployment])
def read_deployments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve deployments.
    """
    deployments = crud.deployment.get_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return deployments


@router.post("/", response_model=Deployment)
def create_deployment(
    *,
    db: Session = Depends(get_db),
    deployment_in: DeploymentCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new deployment.
    """
    # Check if project exists
    project = crud.project.get_by_id(db=db, project_id=deployment_in.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check if user has access to this project
    if project.owner_id != current_user.id and current_user not in project.team_members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Create deployment
    deployment = crud.deployment.create(
        db=db, obj_in=deployment_in, user_id=current_user.id
    )
    
    # Trigger deployment task
    deploy_project.delay(deployment_id=deployment.id)
    
    return deployment


@router.get("/{deployment_id}", response_model=Deployment)
def read_deployment(
    *,
    db: Session = Depends(get_db),
    deployment_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get deployment by ID.
    """
    deployment = crud.deployment.get_by_id(db=db, deployment_id=deployment_id)
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found",
        )
    
    # Check if user has access to this deployment's project
    project = deployment.project
    if project.owner_id != current_user.id and current_user not in project.team_members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return deployment


@router.delete("/{deployment_id}", response_model=Deployment)
def delete_deployment(
    *,
    db: Session = Depends(get_db),
    deployment_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a deployment.
    """
    deployment = crud.deployment.get_by_id(db=db, deployment_id=deployment_id)
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found",
        )
    
    # Check if user has access to this deployment's project
    project = deployment.project
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    deployment = crud.deployment.remove(db=db, deployment_id=deployment_id)
    return deployment


@router.get("/project/{project_id}", response_model=List[Deployment])
def read_project_deployments(
    *,
    db: Session = Depends(get_db),
    project_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all deployments for a project.
    """
    # Check if project exists
    project = crud.project.get_by_id(db=db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check if user has access to this project
    if project.owner_id != current_user.id and current_user not in project.team_members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    deployments = crud.deployment.get_by_project(
        db=db, project_id=project_id, skip=skip, limit=limit
    )
    return deployments 