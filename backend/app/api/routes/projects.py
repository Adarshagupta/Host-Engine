from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.crud import project
from app.api.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve projects.
    """
    projects = project.get_user_projects(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return projects


@router.post("/", response_model=Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new project.
    """
    project_obj = project.create_project(db=db, project_create=project_in, user_id=current_user.id)
    return project_obj


@router.get("/{project_id}", response_model=Project)
def read_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get project by ID.
    """
    project_obj = project.get_project(db=db, project_id=project_id)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return project_obj


@router.put("/{project_id}", response_model=Project)
def update_project_by_id(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    project_in: ProjectUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a project.
    """
    project_obj = project.get_project(db=db, project_id=project_id)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    project_obj = project.update_project(db=db, project_id=project_id, project_update=project_in)
    return project_obj


@router.patch("/{project_id}", response_model=Project)
def patch_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    project_in: ProjectUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Partially update a project.
    """
    project_obj = project.get_project(db=db, project_id=project_id)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    project_obj = project.update_project(db=db, project_id=project_id, project_update=project_in)
    return project_obj


@router.delete("/{project_id}", response_model=bool)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a project.
    """
    project_obj = project.get_project(db=db, project_id=project_id)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return project.delete_project(db=db, project_id=project_id)


@router.put("/{project_id}/env-vars", response_model=Project)
def update_project_environment_variables(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    env_vars: Dict[str, str],
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a project's environment variables.
    """
    project_obj = project.get_project(db=db, project_id=project_id)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    project_obj = project.update_project_env_vars(db=db, project_id=project_id, env_vars=env_vars)
    return project_obj 