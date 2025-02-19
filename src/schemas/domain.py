from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class DomainBase(BaseModel):
    domain: str
    theme: str
    title_template: Optional[str] = None
    description_template: Optional[str] = None
    robots_txt: Optional[str] = None

class DomainCreate(DomainBase):
    pass

class DomainUpdate(BaseModel):
    domain: Optional[str] = None
    theme: Optional[str] = None
    title_template: Optional[str] = None
    description_template: Optional[str] = None
    robots_txt: Optional[str] = None
    status: Optional[str] = None

class DomainInDB(DomainBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
