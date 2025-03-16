from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from app.db.models import Deployment, Project
from app.api.schemas.deployment import DeploymentCreate, DeploymentUpdate


def get_by_id(db: Session, deployment_id: str) -> Optional[Deployment]:
    return db.query(Deployment).filter(Deployment.id == deployment_id).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Deployment]:
    return db.query(Deployment).offset(skip).limit(limit).all()


def get_by_project(
    db: Session, *, project_id: str, skip: int = 0, limit: int = 100
) -> List[Deployment]:
    return (
        db.query(Deployment)
        .filter(Deployment.project_id == project_id)
        .order_by(Deployment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_by_user(
    db: Session, *, user_id: str, skip: int = 0, limit: int = 100
) -> List[Deployment]:
    return (
        db.query(Deployment)
        .filter(Deployment.user_id == user_id)
        .order_by(Deployment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(
    db: Session, *, obj_in: DeploymentCreate, user_id: str
) -> Deployment:
    db_obj = Deployment(
        commit_hash=obj_in.commit_hash,
        commit_message=obj_in.commit_message,
        project_id=obj_in.project_id,
        user_id=user_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Deployment, obj_in: Union[DeploymentUpdate, Dict[str, Any]]
) -> Deployment:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_status(
    db: Session, *, deployment_id: str, status: str
) -> Optional[Deployment]:
    deployment = get_by_id(db=db, deployment_id=deployment_id)
    if not deployment:
        return None
        
    deployment.status = status
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment


def remove(db: Session, *, deployment_id: str) -> Optional[Deployment]:
    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    if not deployment:
        return None
    db.delete(deployment)
    db.commit()
    return deployment 