from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.domain import Domain
from pydantic import BaseModel

router = APIRouter()

class DomainBase(BaseModel):
    domain: str
    theme: str
    title_template: str | None = None
    description_template: str | None = None
    robots_txt: str | None = None

class DomainCreate(DomainBase):
    pass

class DomainResponse(DomainBase):
    id: int
    status: str
    created_at: str

    class Config:
        from_attributes = True

@router.post("/domains", response_model=DomainResponse)
async def create_domain(domain: DomainCreate, db: Session = Depends(get_db)):
    db_domain = Domain(**domain.model_dump())
    db.add(db_domain)
    try:
        db.commit()
        db.refresh(db_domain)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_domain

@router.get("/domains", response_model=List[DomainResponse])
async def list_domains(db: Session = Depends(get_db)):
    return db.query(Domain).all()
