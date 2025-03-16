from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base_class import Base


def generate_uuid():
    return str(uuid.uuid4())


class Domain(Base):
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project_id = Column(String, ForeignKey("project.id"), nullable=False)
    project = relationship("Project", back_populates="domains") 