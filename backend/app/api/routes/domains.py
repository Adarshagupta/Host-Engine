from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.crud import domain, project
from app.api.schemas.domain import Domain, DomainCreate, DomainUpdate
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[Domain])
def get_domains_by_project(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get all domains for a project.
    """
    # Check if project exists and user has access
    project_obj = project.get_project(db, project_id)
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
    
    return domain.get_domains_by_project(db, project_id)


@router.post("/", response_model=Domain)
def create_domain_for_project(
    *,
    project_id: str,
    domain_in: DomainCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a new domain for a project.
    """
    # Check if project exists and user has access
    project_obj = project.get_project(db, project_id)
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
    
    # Check if domain already exists
    existing_domain = domain.get_domain_by_name(db, domain_in.name)
    if existing_domain:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Domain already exists",
        )
    
    return domain.create_domain(db, domain_in, project_id)


@router.get("/{domain_id}", response_model=Domain)
def get_domain(
    domain_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a domain by ID.
    """
    domain_obj = domain.get_domain(db, domain_id)
    if not domain_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found",
        )
    
    # Check if user has access to the project
    project_obj = project.get_project(db, domain_obj.project_id)
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return domain_obj


@router.put("/{domain_id}", response_model=Domain)
def update_domain_by_id(
    *,
    domain_id: str,
    domain_in: DomainUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a domain.
    """
    domain_obj = domain.get_domain(db, domain_id)
    if not domain_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found",
        )
    
    # Check if user has access to the project
    project_obj = project.get_project(db, domain_obj.project_id)
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return domain.update_domain(db, domain_id, domain_in)


@router.post("/{domain_id}/verify", response_model=Domain)
def verify_domain_by_id(
    domain_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Verify a domain.
    """
    domain_obj = domain.get_domain(db, domain_id)
    if not domain_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found",
        )
    
    # Check if user has access to the project
    project_obj = project.get_project(db, domain_obj.project_id)
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # In a real implementation, we would check if the domain has the verification record
    # For now, we'll just mark it as verified
    return domain.verify_domain(db, domain_id)


@router.delete("/{domain_id}", response_model=bool)
def delete_domain_by_id(
    domain_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a domain.
    """
    domain_obj = domain.get_domain(db, domain_id)
    if not domain_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found",
        )
    
    # Check if user has access to the project
    project_obj = project.get_project(db, domain_obj.project_id)
    if project_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return domain.delete_domain(db, domain_id) 