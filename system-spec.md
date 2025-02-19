# Specyfikacja Systemu Generowania Stron Statycznych

## 1. NATURA SYSTEMU
- Generator stron statycznych
- Obsługa wielu domen (dziesiątki tysięcy)
- Miliony wpisów w bazie
- Dwie wersje każdej strony (PC/Mobile)

## 2. STRUKTURA FOLDERÓW
```
/
├── config/           # Konfiguracje domen
├── themes/           # Szablony (PC + Mobile)
├── images/           # Pliki graficzne
└── content/         # Wygenerowane strony
    └── domena.pl/
        ├── desktop/
        └── mobile/
```

## 3. STRUKTURA DANYCH
- Jedna baza danych
- Prefiksy tabel dla domen
- Konfiguracja domen w bazie
- Metadane w bazie

### 3.1 METADANE SEO
#### Poziom Domeny
- title_template (szablon dla meta title)
- description_template (szablon dla meta description)
- custom_robots.txt
- sitemap_settings

#### Poziom Kategorii
- meta_title
- meta_description
- meta_keywords
- category_h1
- category_description (treść dla strony kategorii)

#### Poziom Artykułu
- meta_title
- meta_description
- meta_keywords
- og_title
- og_description
- og_image
- article_h1
- canonical_url
- robots_meta_tags (noindex, nofollow, etc.)
- schema_markup (JSON-LD)

## 4. FUNKCJONALNOŚCI
- Dodawanie treści przez API
- Zarządzanie domenami przez API
- Współdzielenie szablonów między domenami
- Minifikacja wygenerowanych stron
- Automatyczne generowanie stron

## 5. TECHNICZNE
- Python jako język programowania
- API do zarządzania
- Autentykacja przez API key
- Generowanie statycznego HTML

---

## MAPA SYSTEMU

### 1. INFRASTRUKTURA
- Jedna baza danych
- API
- Generator stron statycznych
- System szablonów
- Cache i optymalizacje

### 2. DOMENY
- Setki tysięcy domen
- Współdzielenie szablonów
- Konfiguracja w bazie
- Metadane i ustawienia

### 3. CONTENT
- Miliony wpisów
- Artykuły
- Kategorie
- Obrazki
- Wersje (PC/Mobile)
- Minifikacja

### 4. BAZA DANYCH
- Tabele z prefiksami per domena
- Indeksowanie
- Optymalizacje
- Partycjonowanie

### 5. SZABLONY
- Współdzielone między domenami
- Wersje PC/Mobile
- Konfiguracja per domena
- Customizacja

### 6. API
- Dodawanie treści
- Zarządzanie domenami
- Konfiguracja
- Autentykacja

### 7. OPERACJE
- Generowanie stron
- Zarządzanie obrazkami
- Kolejkowanie zadań
- Monitoring