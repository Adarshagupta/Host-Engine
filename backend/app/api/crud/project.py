from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from app.db.models import Project, User
from app.api.schemas.project import ProjectCreate, ProjectUpdate


def get_by_id(db: Session, project_id: str) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Project]:
    return db.query(Project).offset(skip).limit(limit).all()


def get_by_owner(
    db: Session, *, owner_id: str, skip: int = 0, limit: int = 100
) -> List[Project]:
    return (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_projects(
    db: Session, *, user_id: str, skip: int = 0, limit: int = 100
) -> List[Project]:
    """Get all projects a user has access to (owned + team)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    owned_projects = get_by_owner(db=db, owner_id=user_id, skip=skip, limit=limit)
    team_projects = user.team_projects
    
    # Combine and deduplicate projects
    all_projects = {p.id: p for p in owned_projects}
    for p in team_projects:
        if p.id not in all_projects:
            all_projects[p.id] = p
    
    return list(all_projects.values())


def create(
    db: Session, *, obj_in: ProjectCreate, owner_id: str
) -> Project:
    db_obj = Project(
        name=obj_in.name,
        description=obj_in.description,
        repository_url=obj_in.repository_url,
        branch=obj_in.branch,
        build_command=obj_in.build_command,
        output_directory=obj_in.output_directory,
        environment_variables=obj_in.environment_variables,
        owner_id=owner_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Project, obj_in: Union[ProjectUpdate, Dict[str, Any]]
) -> Project:
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


def remove(db: Session, *, project_id: str) -> Optional[Project]:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    db.delete(project)
    db.commit()
    return project


def add_team_member(db: Session, *, project_id: str, user_id: str) -> Optional[Project]:
    project = db.query(Project).filter(Project.id == project_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not project or not user:
        return None
    
    # Check if user is already a team member
    if user in project.team_members:
        return project
    
    # Add user to team
    project.team_members.append(user)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def remove_team_member(db: Session, *, project_id: str, user_id: str) -> Optional[Project]:
    project = db.query(Project).filter(Project.id == project_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not project or not user:
        return None
    
    # Check if user is a team member
    if user not in project.team_members:
        return project
    
    # Remove user from team
    project.team_members.remove(user)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_projects_by_repo_and_branch(
    db: Session, repository_url: str, branch: str
) -> List[Project]:
    """
    Get projects that match a specific repository URL and branch.
    Used for webhook integrations to trigger auto-deployments.
    """
    return db.query(Project).filter(
        Project.repository_url == repository_url,
        Project.branch == branch
    ).all()


def update_project(
    db: Session, project_id: str, project_update: ProjectUpdate
) -> Optional[Project]:
    """
    Update a project.
    """
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project_env_vars(
    db: Session, project_id: str, env_vars: Dict[str, str]
) -> Optional[Project]:
    """
    Update a project's environment variables.
    """
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    db_project.environment_variables = env_vars
    db.commit()
    db.refresh(db_project)
    return db_project 