# Konfiguracja .env w Projekcie

## 1. Instalacja
```toml
# pyproject.toml
[tool.poetry.dependencies]
python-dotenv = "^1.0.0"
pydantic-settings = "^2.1.0"
```

## 2. Pliki konfiguracyjne

```ini
# .env.example
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

```gitignore
# .gitignore
.env
.env.*
!.env.example
```

## 3. Implementacja

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
```

## 4. Użycie

```python
# Przykład w db.py
from sqlalchemy.ext.asyncio import create_async_engine
from .config import get_settings

settings = get_settings()
DATABASE_URL = f"mysql+aiomysql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"

# Przykład w api
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from .config import get_settings

settings = get_settings()
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403)
    return api_key

# Przykład w generator
from pathlib import Path
from .config import get_settings

settings = get_settings()
output_path = Path(settings.output_dir) / "domain.com"
```

## 5. Local Development

1. Skopiuj `.env.example` do `.env`
2. Uzupełnij wartości w `.env`
3. Nigdy nie commituj `.env`
4. Aktualizuj `.env.example` przy dodawaniu nowych zmiennych

## 6. CI/CD

1. W środowisku produkcyjnym użyj zmiennych środowiskowych
2. Możesz też użyć `.env.prod` (pamiętaj o `.gitignore`)
3. Ustaw odpowiednie secrety w CI/CD pipeline