# Stos Technologiczny MVP

## 1. Podstawowe Technologie

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- Alembic (migracje)
- Jinja2 (szablony)
- uvicorn (serwer)

### Baza Danych
- MySQL 8.0+ / MariaDB 10.6+
- aiomysql (async driver)

## 2. Zależności Python

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
sqlalchemy = "^2.0.25"
alembic = "^1.13.1"
aiomysql = "^0.2.0"
jinja2 = "^3.1.3"
python-multipart = "^0.0.6"
pydantic = "^2.5.3"
pydantic-settings = "^2.1.0"
python-dotenv = "^1.0.0"
uvicorn = "^0.27.0"
python-jose = "^3.3.0"  # JWT dla API auth
```

## 3. Konfiguracja środowiska

### Przykładowy .env
```ini
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=user
DB_PASS=pass
DB_NAME=static_generator

# API
API_KEY=your-secret-key
API_DEBUG=false

# Paths
THEMES_DIR=/path/to/themes
OUTPUT_DIR=/path/to/output

# Features
ENABLE_CACHE=false
```

### Settings z Pydantic
```python
# src/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    # API
    api_key: str
    api_debug: bool = False

    # Paths
    themes_dir: str
    output_dir: str

    # Features
    enable_cache: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

# Użycie w innych modułach:
# from config import get_settings
# settings = get_settings()
# db_url = f"mysql+aiomysql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"
```

## 4. Struktura Projektu

```
/
├── alembic/              # Migracje
├── src/
│   ├── api/             # Endpoints FastAPI
│   │   ├── __init__.py
│   │   ├── domains.py
│   │   ├── content.py
│   │   └── generator.py
│   ├── models/          # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── domain.py
│   │   ├── content.py
│   │   └── image.py
│   ├── generator/       # Generator stron
│   │   ├── __init__.py
│   │   ├── html.py     # Generowanie HTML
│   │   └── seo.py      # Generowanie meta
│   ├── templates/       # Szablony Jinja2
│   ├── db.py           # DB connection
│   └── config.py       # Konfiguracja
├── pyproject.toml
└── README.md
```

## 4. Przykładowa Implementacja

### Konfiguracja DB
```python
# src/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()
DATABASE_URL = f"mysql+aiomysql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Model SQLAlchemy
```python
# src/models/domain.py
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.sql import func
from .base import Base

class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True)
    domain = Column(String(255), unique=True, nullable=False)
    theme = Column(String(255), nullable=False)
    status = Column(Enum('active', 'inactive'), default='active')
    title_template = Column(String(255))
    description_template = Column(Text)
    robots_txt = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
```

### FastAPI Endpoint
```python
# src/api/domains.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..models import Domain

router = APIRouter()

@router.post("/domains")
async def create_domain(
    domain: DomainCreate,
    db: AsyncSession = Depends(get_db)
):
    db_domain = Domain(**domain.model_dump())
    db.add(db_domain)
    await db.commit()
    await db.refresh(db_domain)
    return db_domain
```

### Generator HTML
```python
# src/generator/html.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class HTMLGenerator:
    def __init__(self, theme_path: str):
        self.env = Environment(
            loader=FileSystemLoader(theme_path),
            autoescape=True
        )

    async def generate_article(self, article, template='article.html'):
        template = self.env.get_template(template)
        return template.render(
            meta_title=article.meta_title,
            meta_description=article.meta_description,
            h1=article.h1,
            content=article.content,
            image=article.image.data
        )
```

## 5. API Endpoints

```python
# Główne endpointy
/api
  ├── /domains
  │   ├── POST /              # Nowa domena
  │   └── GET /{domain_id}    # Pobranie domeny
  ├── /content
  │   ├── POST /              # Nowa treść
  │   └── PUT /{content_id}   # Aktualizacja
  ├── /categories
  │   └── POST /              # Nowa kategoria
  ├── /images
  │   └── POST /              # Nowy obrazek (base64)
  └── /generate
      └── POST /{domain}      # Generowanie strony
```

## 6. Kolejne Kroki

1. Dodanie testów (pytest)
2. Dodanie logowania (strukturalnego)
3. Monitoring i metryki
4. CI/CD pipeline
5. Docker setup
6. Cache
7. Rate limiting dla API