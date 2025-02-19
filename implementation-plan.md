# Plan Implementacji - Generator Stron Statycznych

## 1. STRUKTURA BAZY DANYCH

### A. Tabele konfiguracyjne
```sql
domains (
    id BIGINT PRIMARY KEY,
    domain VARCHAR(255) NOT NULL UNIQUE,
    theme VARCHAR(255) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

domain_settings (
    id BIGINT PRIMARY KEY,
    domain_id BIGINT,
    key VARCHAR(255),
    value TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES domains(id),
    UNIQUE KEY (domain_id, key)
);

themes (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    path VARCHAR(255) NOT NULL,
    version VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

theme_settings (
    id BIGINT PRIMARY KEY,
    theme_id BIGINT,
    key VARCHAR(255),
    default_value TEXT,
    is_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (theme_id) REFERENCES themes(id),
    UNIQUE KEY (theme_id, key)
);
```

### B. Tabele treści (prefiks per domena)
```sql
{prefix}_content (
    id BIGINT PRIMARY KEY,
    title VARCHAR(255),
    meta_title VARCHAR(255),
    meta_description TEXT,
    content LONGTEXT,
    slug VARCHAR(255) UNIQUE,
    category_id BIGINT,
    status ENUM('draft', 'published'),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

{prefix}_categories (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    slug VARCHAR(255) UNIQUE,
    description TEXT,
    meta_title VARCHAR(255),
    meta_description TEXT,
    parent_id BIGINT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## 2. PROOF OF CONCEPT

### A. Podstawowa struktura projektu
- Utworzenie repozytorium
- Konfiguracja środowiska Python
- Struktura katalogów:
  ```
  /
  ├── themes/          # Szablony
  ├── images/          # Pliki graficzne
  ├── content/         # Wygenerowane strony
  └── src/
      ├── generators/  # Logika generowania
      ├── database/    # Modele i migracje
      └── utils/       # Narzędzia pomocnicze
  ```

### B. System konfiguracji
- Model dostępu do konfiguracji w bazie
- Cache konfiguracji
- Walidatory danych
- Obsługa wielu domen

### C. Generator
- Moduł generowania artykułu
- Moduł generowania kategorii
- Moduł generowania strony głównej
- System szablonów (z bazy)

## 3. API

### A. Endpointy konfiguracyjne
```
POST   /api/domains
PUT    /api/domains/{id}
POST   /api/domains/{id}/settings
PUT    /api/domains/{id}/settings/{key}
POST   /api/themes
PUT    /api/themes/{id}
POST   /api/themes/{id}/settings
```

### B. Endpointy treści
```
POST   /api/content
PUT    /api/content/{id}
DELETE /api/content/{id}
POST   /api/generate/{domain_id}
```

## 4. BEZPIECZEŃSTWO

### A. Walidacja i sanityzacja
- Walidacja danych wejściowych
- Sanityzacja danych z bazy
- Escaped output w szablonach

### B. Izolacja
- Izolacja domen
- Separacja treści
- Walidacja ścieżek

## 5. GENEROWANIE

### A. Process
- Pobranie konfiguracji z bazy
- Załadowanie odpowiedniego szablonu
- Generowanie plików HTML (PC + Mobile)
- Minifikacja
- Zapis na dysk

### B. Monitoring
- Logi operacji
- Status generowania
- Walidacja wygenerowanych plików
