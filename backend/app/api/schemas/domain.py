from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class DomainBase(BaseModel):
    name: str


class DomainCreate(DomainBase):
    pass


class DomainUpdate(BaseModel):
    name: Optional[str] = None
    verified: Optional[bool] = None
    verification_code: Optional[str] = None


class DomainInDBBase(DomainBase):
    id: str
    verified: bool
    verification_code: str
    created_at: datetime
    project_id: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Domain(DomainInDBBase):
    pass


# Additional properties stored in DB
class DomainInDB(DomainInDBBase):
    pass 