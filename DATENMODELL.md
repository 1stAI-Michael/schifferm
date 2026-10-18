# Datenmodell career.db — Referenz für schifferm.de

> Diese Datei erklärt das Datenmodell der career.db und der daraus generierten
> `career_data.json` für die Claude-Instanz, die schifferm.de betreut.

## Überblick

```
career.db  →  career_data.json  →  NextCloud Sync  →  schifferm.de
```

- **career.db** ist die Single Source of Truth für alle Lebenslaufdaten
- **career_data.json** wird automatisch bei jeder CV-PDF-Generierung exportiert
  (siehe `export_career_json()` in `generate_cv_de_pdf.py` / `generate_cv_pdf.py`)
- Die JSON-Datei enthält alle Tabellen als Key-Value-Objekt
- Alle Textfelder existieren in **DE und EN** (Suffix `_de` / `_en`)
- Datumsfelder verwenden **YYYY-MM** Format

---

## Tabellen

### personal_info (1 Record)
Persönliche Daten, Kontakt, Summary.

| Feld | Beschreibung |
|------|-------------|
| title_de / title_en | Vollständiger Name mit Titeln |
| summary_de / summary_en | Profilzusammenfassung (Freitext) |
| street, zip_code, city, country_de/en | Adresse |
| email, phone, website, linkedin_url | Kontakt |
| birth_date, birth_place | Geburtsdaten |
| citizenship_de/en, marital_status_de/en | Persönliches |
| photo_path | Pfad zum Profilfoto |

### work_experience (12 Records)
Arbeitgeber-Stationen (JCI, TI GmbH, etc.).

| Feld | Beschreibung |
|------|-------------|
| employer | Firmenname |
| role_de / role_en | Positionsbezeichnung |
| description_de / description_en | Beschreibung der Tätigkeit |
| date_from / date_to | Zeitraum (YYYY-MM, date_to=NULL → aktuell) |
| is_current | 1 = aktuelle Position (The Implementers GmbH) |
| industry_de / industry_en | Branche |
| location | Standort |

**Wichtig:** `is_current=1` markiert The Implementers GmbH. Unter dieser Station
werden in den CV-Generatoren alle **Projekte** aufgelistet.

### projects (19 Records) ⭐ Wichtigste Tabelle für die Website

Einzelne Projekte unter TI GmbH. **Jedes Projekt hat drei Beschreibungsstufen:**

| Feld | Zweck | Wann verwenden |
|------|-------|----------------|
| **description_de / description_en** | Volle Beschreibung (5-15 Zeilen) | Wenn das Projekt im Fokus steht |
| **description_short_de / description_short_en** | Eye-Catcher (1-2 Zeilen) | Wenn das Projekt NICHT im Fokus steht |
| **category** | Projektkategorie | Für Filterung und Fokus-Logik |

#### Kategorien

| category | Bedeutung | Beispiel-Projekte |
|----------|-----------|-------------------|
| `ai` | KI/ML/GenAI-Projekte | Klinische Dokumentation, VIVO PainCare, Dokumentenerkennung, Invoice API |
| `manufacturing` | Klassische Industrie/Automotive | KTM Lieferantenentwicklung, PWG Interim COO, Toyota Boshoku |
| `consulting` | Beratung/Prozessoptimierung | Von Roll Lean-Beratung, Existenzgründungsberatung |
| `healthcare` | Healthcare (ohne KI-Fokus) | Back Office Praxis, Leistungsdokumentation Schmerztherapie |

#### Fokus-Logik in den CV-Generatoren

```python
python generate_cv_de_pdf.py --focus ai
# → AI-Projekte: description_de (volle Beschreibung)
# → Alle anderen: description_short_de (Eye-Catcher)

python generate_cv_de_pdf.py --focus manufacturing
# → Manufacturing-Projekte: description_de (volle Beschreibung)
# → Alle anderen: description_short_de (Eye-Catcher)

python generate_cv_de_pdf.py
# → Alle Projekte: description_de (volle Beschreibung)
```

**Empfehlung für die Website:** Verwende `description_short_de/en` als Vorschau
in Übersichtslisten und `description_de/en` in der Detailansicht. Die `category`
kann für Filter oder farbliche Kennzeichnung genutzt werden.

#### Weitere Felder in projects

| Feld | Beschreibung |
|------|-------------|
| work_experience_id | FK → work_experience (immer 11 = TI GmbH) |
| client | Kundenname (NULL = Eigenentwicklung) |
| date_from / date_to | Zeitraum (date_to=NULL → laufend) |
| title_de / title_en | Projekttitel |
| sort_order | Reihenfolge (niedrig = oben) |

### education (4 Records)
Ausbildungsstationen.

| Feld | Beschreibung |
|------|-------------|
| degree_de / degree_en | Abschluss (MBA, Dipl.-Ing., etc.) |
| field_de / field_en | Fachrichtung |
| institution | Name der Hochschule/Schule |
| grade | Note (z.B. "1,3") |
| thesis_de / thesis_en | Abschlussarbeit |

### certifications (43 Records)
Zertifikate und Weiterbildungen, gruppiert nach Kategorie.

| Feld | Beschreibung |
|------|-------------|
| name_de / name_en | Name des Zertifikats |
| issuer | Aussteller (z.B. "IBM / Coursera") |
| category | `ai_healthcare`, `ai_data`, `quality`, `management`, `misc` |
| date_from / date_to | Zeitraum |
| pdf_path | Pfad zum Zertifikats-PDF |

### skills (32 Records)
IT- und Fachkenntnisse mit Niveaustufen.

| Feld | Beschreibung |
|------|-------------|
| name | Skill-Name (z.B. "Python", "SAP") |
| category | `programming`, `ai_automation`, `databases`, `office`, `cad`, `pm_tools`, `os`, `pdm`, `mrp` |
| level_de / level_en | Niveau ("sehr gut"/"advanced", "gut"/"proficient", "Basis"/"basic") |

### languages (5 Records)
Sprachkenntnisse: Deutsch (Muttersprache), Englisch (fließend), Französisch, Spanisch, Polnisch.

### awards (2 Records)
Auszeichnungen: Pallas Athene-Medaille (1998), Innungsbester Kfz-Mechaniker (1995).

### driving_licenses (5 Records)
Führerscheine: Klasse A-CE, Staplerschein, Motorboot.

### hobbies (6 Records)
Persönliche Interessen.

### memberships (2 Records)
VDI, DARC (Amateurfunk).

---

## Sortierung

- Tabellen mit `sort_order`-Spalte: sortiert nach `sort_order, id`
- Tabellen ohne `sort_order`: sortiert nach `id`
- Projects in den CV-Generatoren: sortiert nach `date_from DESC` (neueste zuerst)

---

## JSON-Struktur (career_data.json)

```json
{
  "awards": [...],
  "certifications": [...],
  "driving_licenses": [...],
  "education": [...],
  "hobbies": [...],
  "languages": [...],
  "memberships": [...],
  "personal_info": [{ /* 1 Record */ }],
  "projects": [{ /* 19 Records, inkl. category + description_short_* */ }],
  "skills": [...],
  "work_experience": [...]
}
```

Jeder Eintrag ist ein vollständiges Objekt mit allen Spalten der jeweiligen Tabelle.

---

## Wichtig für die Website

1. **description_short vs. description:** Immer `description_short_de/en` für
   Listenansichten verwenden, `description_de/en` für Detailansichten
2. **category:** Kann für farbliche Tags verwendet werden (ai=grün, manufacturing=braun,
   healthcare=türkis, consulting=mint — wie im `career_db_viewer.html`)
3. **date_to=null:** Bedeutet "laufend" / "heute" — in der Anzeige als "heute" / "present" darstellen
4. **is_current=1:** Nur bei work_experience, markiert die aktuelle TI GmbH-Position
5. **Die JSON wird automatisch aktualisiert** bei jeder CV-PDF-Generierung — kein manueller Export nötig
