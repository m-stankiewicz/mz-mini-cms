from sqlalchemy import Column, Integer, String, Enum, Text, TIMESTAMP
from datetime import datetime
from ..database import Base

class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), unique=True, nullable=False)
    theme = Column(String(255), nullable=False)
    status = Column(Enum('active', 'inactive', name='domain_status'), default='active')
    title_template = Column(String(255))
    description_template = Column(Text)
    robots_txt = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
