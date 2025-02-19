from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ....db.session import get_db
from ....schemas.domain import DomainCreate, DomainUpdate, DomainInDB
from ....services.domain import DomainService
from ....core.exceptions import NotFoundException, ValidationError

router = APIRouter()

@router.post("/", response_model=DomainInDB, status_code=status.HTTP_201_CREATED)
def create_domain(domain: DomainCreate, db: Session = Depends(get_db)):
    try:
        domain_service = DomainService(db)
        return domain_service.create_domain(domain)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[DomainInDB])
def list_domains(db: Session = Depends(get_db)):
    domain_service = DomainService(db)
    return domain_service.get_domains()

@router.get("/{domain_id}", response_model=DomainInDB)
def get_domain(domain_id: int, db: Session = Depends(get_db)):
    try:
        domain_service = DomainService(db)
        return domain_service.get_domain(domain_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{domain_id}", response_model=DomainInDB)
def update_domain(domain_id: int, domain: DomainUpdate, db: Session = Depends(get_db)):
    try:
        domain_service = DomainService(db)
        return domain_service.update_domain(domain_id, domain)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{domain_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_domain(domain_id: int, db: Session = Depends(get_db)):
    try:
        domain_service = DomainService(db)
        domain_service.delete_domain(domain_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
