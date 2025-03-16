from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
import random
import string

from app.models.domain import Domain
from app.api.schemas.domain import DomainCreate, DomainUpdate


def get_domain(db: Session, domain_id: str) -> Optional[Domain]:
    """Get a domain by ID."""
    return db.query(Domain).filter(Domain.id == domain_id).first()


def get_domain_by_name(db: Session, name: str) -> Optional[Domain]:
    """Get a domain by name."""
    return db.query(Domain).filter(Domain.name == name).first()


def get_domains_by_project(db: Session, project_id: str) -> List[Domain]:
    """Get all domains for a project."""
    return db.query(Domain).filter(Domain.project_id == project_id).all()


def create_domain(db: Session, domain: DomainCreate, project_id: str) -> Domain:
    """Create a new domain."""
    # Generate a random verification code
    verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    db_domain = Domain(
        id=str(uuid.uuid4()),
        name=domain.name,
        verified=False,
        verification_code=verification_code,
        project_id=project_id
    )
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain


def update_domain(db: Session, domain_id: str, domain_update: DomainUpdate) -> Optional[Domain]:
    """Update a domain."""
    db_domain = get_domain(db, domain_id)
    if not db_domain:
        return None
    
    update_data = domain_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_domain, field, value)
    
    db.commit()
    db.refresh(db_domain)
    return db_domain


def verify_domain(db: Session, domain_id: str) -> Optional[Domain]:
    """Mark a domain as verified."""
    db_domain = get_domain(db, domain_id)
    if not db_domain:
        return None
    
    db_domain.verified = True
    db.commit()
    db.refresh(db_domain)
    return db_domain


def delete_domain(db: Session, domain_id: str) -> bool:
    """Delete a domain."""
    db_domain = get_domain(db, domain_id)
    if not db_domain:
        return False
    
    db.delete(db_domain)
    db.commit()
    return True 