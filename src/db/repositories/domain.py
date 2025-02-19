from typing import Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from ...models.domain import Domain
from ...schemas.domain import DomainCreate, DomainUpdate

class DomainRepository(BaseRepository[Domain, DomainCreate, DomainUpdate]):
    def __init__(self, db: Session):
        super().__init__(Domain, db)

    def get_by_domain(self, domain: str) -> Optional[Domain]:
        return self.db.query(self.model).filter(self.model.domain == domain).first()

    def get_active_domains(self):
        return self.db.query(self.model).filter(self.model.status == 'active').all()
