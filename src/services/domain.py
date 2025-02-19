from typing import List, Optional
from sqlalchemy.orm import Session
from ..db.repositories.domain import DomainRepository
from ..schemas.domain import DomainCreate, DomainUpdate, DomainInDB
from ..core.exceptions import NotFoundException, ValidationError

class DomainService:
    def __init__(self, db: Session):
        self.repository = DomainRepository(db)

    def create_domain(self, domain_create: DomainCreate) -> DomainInDB:
        # Check if domain already exists
        if self.repository.get_by_domain(domain_create.domain):
            raise ValidationError(f"Domain {domain_create.domain} already exists")
        return self.repository.create(domain_create)

    def get_domain(self, domain_id: int) -> DomainInDB:
        domain = self.repository.get(domain_id)
        if not domain:
            raise NotFoundException(f"Domain with id {domain_id} not found")
        return domain

    def get_domains(self) -> List[DomainInDB]:
        return self.repository.get_all()

    def update_domain(self, domain_id: int, domain_update: DomainUpdate) -> DomainInDB:
        domain = self.repository.update(domain_id, domain_update)
        if not domain:
            raise NotFoundException(f"Domain with id {domain_id} not found")
        return domain

    def delete_domain(self, domain_id: int) -> bool:
        if not self.repository.delete(domain_id):
            raise NotFoundException(f"Domain with id {domain_id} not found")
        return True

    def get_active_domains(self) -> List[DomainInDB]:
        return self.repository.get_active_domains()
