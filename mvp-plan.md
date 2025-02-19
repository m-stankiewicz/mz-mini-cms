# Plan MVP - Generator Stron Statycznych

## 1. BAZA DANYCH

### Podstawowe tabele
```sql
domains (
    id BIGINT PRIMARY KEY,
    domain VARCHAR(255) NOT NULL UNIQUE,
    theme VARCHAR(255) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    title_template VARCHAR(255),     # Szablon dla meta title
    description_template TEXT,        # Szablon dla meta description
    robots_txt TEXT,                 # Treść robots.txt
    created_at TIMESTAMP
);

domain_settings (
    id BIGINT PRIMARY KEY,
    domain_id BIGINT,
    key VARCHAR(255),
    value TEXT,
    FOREIGN KEY (domain_id) REFERENCES domains(id)
);

{prefix}_content (
    id BIGINT PRIMARY KEY,
    title VARCHAR(255),
    content LONGTEXT,
    slug VARCHAR(255) UNIQUE,
    category_id BIGINT,
    status ENUM('draft', 'published'),
    meta_title VARCHAR(255),         # SEO title
    meta_description TEXT,           # SEO description
    meta_keywords VARCHAR(255),      # SEO keywords
    h1 VARCHAR(255),                # Główny nagłówek
    canonical_url VARCHAR(255),      # URL kanoniczny
    robots_meta VARCHAR(255),        # noindex, nofollow, etc.
    schema_markup TEXT,             # JSON-LD
    image_id BIGINT,                # Relacja do obrazka
    created_at TIMESTAMP
);

{prefix}_categories (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    slug VARCHAR(255) UNIQUE,
    description TEXT,
    parent_id BIGINT NULL,
    meta_title VARCHAR(255),         # SEO title
    meta_description TEXT,           # SEO description
    meta_keywords VARCHAR(255),      # SEO keywords
    h1 VARCHAR(255),                # Główny nagłówek
    category_description TEXT,       # Treść strony kategorii
    image_id BIGINT                 # Relacja do obrazka
);

images (
    id BIGINT PRIMARY KEY,
    domain_id BIGINT,
    filename VARCHAR(255),          # UUID + extension
    data TEXT,                     # Base64
    created_at TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES domains(id)
);
```

## 2. STRUKTURA PROJEKTU

```
/
├── themes/          # Podstawowe szablony PC/Mobile
│   ├── default/
│   │   ├── desktop/
│   │   └── mobile/
├── content/         # Wygenerowane strony
│   └── {domain}/
│       ├── desktop/
│       ├── mobile/
│       ├── robots.txt
│       └── sitemap.xml
└── src/
    ├── api/        # FastAPI endpoints
    ├── models/     # SQLAlchemy models
    └── generator/  # Generator stron
```

## 3. API (FASTAPI)

```python
# Główne endpointy
@app.post("/api/domains")
async def create_domain(domain: DomainCreate):
    # Utworzenie nowej domeny

@app.post("/api/content")
async def create_content(content: ContentCreate):
    # Dodanie nowej treści

@app.post("/api/categories")
async def create_category(category: CategoryCreate):
    # Dodanie nowej kategorii

@app.post("/api/images")
async def create_image(domain_id: int, filename: str, data: str):
    # Zapis obrazka w base64

@app.post("/api/generate/{domain}")
async def generate_site(domain: str):
    # Wygenerowanie strony
```

## 4. GENEROWANIE

### Proces MVP
1. Pobranie konfiguracji domeny
2. Załadowanie podstawowego szablonu
3. Generowanie:
   - HTML dla PC i Mobile
   - robots.txt z konfiguracji domeny
   - sitemap.xml z listą wszystkich URL-i
4. Wstawienie metadanych SEO:
   - Meta tagi (title, description, keywords)
   - Canonical URL
   - Robots meta tagi
   - Schema.org markup
5. Zapis plików na dysk

### Generowane elementy
- Strona główna z metadanymi z domeny
- Strony kategorii z własnymi metadanymi
- Strony artykułów z własnymi metadanymi
- robots.txt per domena
- sitemap.xml z wszystkimi URL-ami

## 5. KOLEJNE KROKI

Funkcjonalności do dodania po MVP:
1. Pełny system zarządzania obrazkami:
   - Upload plików
   - Przetwarzanie i optymalizacja
   - Generowanie miniatur
   - CDN
   - Lazy loading
   - Galerie obrazków
2. Cache konfiguracji
3. Walidatory danych
4. Minifikacja HTML
5. Rozszerzone metadane (Open Graph, Twitter Cards)
6. System kolejkowania
7. Monitoring generowania
8. Panel administracyjny
9. Backup i przywracanie danych