#!/usr/bin/env python3
"""
Generate machine-readable career data formats from the career device API.

Quelle ist seit 27.08.2026 die Device-API auf app.ti-ub-ki.ddns.net (Postgres,
Schema `career`). Die frühere SQLite `career.db` auf Nextcloud ist abgeschaltet;
der WebDAV-Weg ist deshalb entfallen.

Outputs (into public/):
  - llms.txt                   — LLM discovery file (root)
  - career/career_data.json    — Roh-Export, versorgt die Website-UI
  - career/profile.json        — JSON Resume format (DE+EN)
  - career/profile.md          — Full markdown (DE+EN)
  - career/schema.jsonld       — schema.org Person JSON-LD

Usage:
  python scripts/generate-career-formats.py
  python scripts/generate-career-formats.py --json /pfad/career_data.json
  python scripts/generate-career-formats.py --db /pfad/career.db   # Altbestand

Das Gerätetoken kommt aus $FLOWS_CAREER_TOKEN oder aus der Schienen-Token-Datei
(~/.config/flows/tokens/VM-30-Web.token). Es wird nie ausgegeben und nie als
Kommandozeilen-Argument weitergereicht.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
PUBLIC_DIR = ROOT_DIR / "public"

def _api_basis():
    """Wirt wie bei allen Flotten-Werkzeugen: Umgebung, dann maschine.env
    (fA-645/fA-681). KEIN fester Name und kein Rueckfall auf den Altnamen
    `app.ti-ub-ki.ddns.net` — der ist seit 08.09.2026 tot, und weil er fest
    eingetragen war, scheiterte der Bau ueber fuenf Wochen unbemerkt (fA-1446,
    18.10.2026). Faellt die Datei weg, bricht das Skript laut ab, statt zu raten.
    """
    aus_umgebung = os.environ.get("FLOWS_API_BASIS", "").strip()
    if aus_umgebung:
        return aus_umgebung.rstrip("/")
    for home in (Path.home(), *( [Path(__import__("pwd").getpwnam(os.environ["SUDO_USER"]).pw_dir)]
                                 if os.environ.get("SUDO_USER") else [] )):
        datei = home / ".config" / "flows" / "maschine.env"
        if datei.is_file():
            for zeile in datei.read_text(encoding="utf-8").splitlines():
                if zeile.startswith("FLOWS_API_BASIS="):
                    wert = zeile.split("=", 1)[1].strip().strip('"').strip("'")
                    if wert:
                        return wert.rstrip("/")
    raise SystemExit(
        "ERROR: kein FLOWS_API_BASIS — weder in der Umgebung noch in "
        "~/.config/flows/maschine.env. Ohne Wirt wird nicht geraten."
    )


CAREER_API = _api_basis() + "/api/career/device"
SITE_URL = "https://schifferm.de"


def _token_file():
    """Token-Datei der Schiene. Unter sudo zeigt HOME auf /root — dort liegt sie nicht,
    deshalb auf das Home des aufrufenden Users zurückfallen (der Deploy läuft mit sudo,
    weil /srv/Container/.env root-only ist)."""
    candidates = [Path.home()]
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        try:
            import pwd

            candidates.append(Path(pwd.getpwnam(sudo_user).pw_dir))
        except (ImportError, KeyError):
            pass
    for home in candidates:
        path = home / ".config" / "flows" / "tokens" / "VM-30-Web.token"
        if path.is_file():
            return path
    return candidates[0] / ".config" / "flows" / "tokens" / "VM-30-Web.token"


TOKEN_FILE = _token_file()

TABLES = (
    "personal_info", "work_experience", "projects", "education",
    "certifications", "skills", "languages", "driving_licenses",
    "awards", "hobbies", "memberships",
)


# ---------------------------------------------------------------------------
# Data source
# ---------------------------------------------------------------------------

class CareerSource:
    """Alle elf Tabellen im Speicher — Ersatz für die frühere sqlite3-Verbindung."""

    def __init__(self, tables, origin):
        self.tables = tables
        self.origin = origin

    def close(self):
        pass


def read_device_token():
    """Token aus Umgebung oder Schienen-Datei — Wert wird nie ausgegeben."""
    token = os.environ.get("FLOWS_CAREER_TOKEN") or os.environ.get("FLOWS_TICKETS_TOKEN")
    if token and token.strip():
        return token.strip()
    if TOKEN_FILE.is_file():
        return TOKEN_FILE.read_text(encoding="utf-8").strip()
    print(
        f"ERROR: kein Gerätetoken — weder $FLOWS_CAREER_TOKEN noch {TOKEN_FILE}",
        file=sys.stderr,
    )
    sys.exit(1)


def fetch_api():
    """Alle Tabellen über die Device-API holen."""
    token = read_device_token()
    tables = {}
    for table in TABLES:
        req = urllib.request.Request(
            f"{CAREER_API}/{table}",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            print(f"ERROR: {table}: HTTP {exc.code} von der Career-API", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as exc:
            print(f"ERROR: {table}: Career-API nicht erreichbar ({exc.reason})", file=sys.stderr)
            sys.exit(1)
        if isinstance(payload, dict):
            payload = payload.get("rows") or payload.get(table) or []
        tables[table] = payload
    counts = ", ".join(f"{t} {len(tables[t])}" for t in TABLES)
    print(f"  Career-API gelesen: {counts}")
    return CareerSource(tables, "device-api")


def load_json_export(path):
    """Fertigen career_data.json-Export von der Platte lesen."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    tables = {t: data.get(t, []) for t in TABLES}
    print(f"  Export gelesen: {path}")
    return CareerSource(tables, f"json:{path}")


def load_sqlite(path):
    """Altbestand: lokale career.db lesen. Die Nextcloud-DB ist abgeschaltet."""
    import sqlite3

    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    tables = {}
    for table in TABLES:
        rows = conn.execute(f"SELECT * FROM {table}").fetchall()
        tables[table] = [dict(r) for r in rows]
    conn.close()
    print(f"  Lokale DB gelesen: {path}")
    return CareerSource(tables, f"sqlite:{path}")


# Die DB führt das Land als Klartext (country_de/country_en), nicht als ISO-Code.
# Früher stand hier fest "DE" — das war nach dem Umzug schlicht falsch.
COUNTRY_CODES = {
    "germany": "DE", "deutschland": "DE",
    "poland": "PL", "polen": "PL",
    "austria": "AT", "österreich": "AT",
    "switzerland": "CH", "schweiz": "CH",
}


def country_code(personal):
    """ISO-Code zum Land aus der DB. Unbekannt → weglassen statt raten."""
    name = (personal.get("country_en") or personal.get("country_de") or "").strip().lower()
    code = COUNTRY_CODES.get(name)
    if not code and name:
        print(f"  WARNUNG: kein ISO-Code für Land {name!r} — addressCountry bleibt leer", file=sys.stderr)
    return code


def blockquote(text):
    """Mehrabsätzigen Text als Markdown-Zitat — jede Zeile trägt ihr eigenes '>'."""
    paragraphs = [p.strip() for p in (text or "").split("\n\n") if p.strip()]
    return "\n>\n".join(f"> {p}" for p in paragraphs)


def query_all(src, table, order_by=None):
    """Return all rows from a table as list of dicts, sorted like the DB did."""
    rows = [dict(r) for r in src.tables.get(table, [])]
    if not rows:
        return rows
    if order_by is None:
        order_by = "sort_order, id" if "sort_order" in rows[0] else "id"
    keys = [k.strip() for k in order_by.split(",")]

    def sort_key(row):
        out = []
        for k in keys:
            v = row.get(k)
            out.append((v is None, v if v is not None else 0))
        return tuple(out)

    return sorted(rows, key=sort_key)


# ---------------------------------------------------------------------------
# JSON Resume builder (https://jsonresume.org/schema)
# ---------------------------------------------------------------------------

def build_json_resume(conn, lang="en"):
    de = lang == "de"
    personal = query_all(conn, "personal_info")[0]
    work_exp = query_all(conn, "work_experience")
    projects = query_all(conn, "projects")
    education = query_all(conn, "education")
    certs = query_all(conn, "certifications")
    skills_raw = query_all(conn, "skills")
    languages = query_all(conn, "languages")
    awards = query_all(conn, "awards")

    # Map projects to their work_experience
    proj_by_we = {}
    for p in projects:
        proj_by_we.setdefault(p["work_experience_id"], []).append(p)

    # Build work entries
    work_entries = []
    for we in work_exp:
        highlights = []
        desc = we["description_de"] if de else we["description_en"]
        if desc:
            highlights.append(desc)
        # Add project highlights
        for p in proj_by_we.get(we["id"], []):
            p_title = p["title_de"] if de else p["title_en"]
            p_desc = p["description_de"] if de else p["description_en"]
            client = f" ({p['client']})" if p.get("client") else ""
            highlights.append(f"{p_title}{client}: {p_desc}" if p_desc else f"{p_title}{client}")

        work_entries.append({
            "name": we["employer"],
            "position": we["role_de"] if de else we["role_en"],
            "startDate": we["date_from"],
            "endDate": we["date_to"] or "",
            "summary": we["industry_de"] if de else we["industry_en"],
            "highlights": highlights,
        })

    # Group skills by category
    skill_groups = {}
    for s in skills_raw:
        cat = s["category"]
        skill_groups.setdefault(cat, []).append({
            "name": s["name"],
            "level": s["level_de"] if de else s["level_en"],
        })

    skills_out = []
    cat_labels = {
        "llm_infrastructure": "LLM Infrastructure" if not de else "LLM-Infrastruktur",
        "ai_automation": "AI & Automation",
        "programming": "Programming" if not de else "Programmierung",
        "backend": "Backend & DevOps",
        "databases": "Databases" if not de else "Datenbanken",
        "medtech": "Medical Technology" if not de else "Medizintechnik",
        "office": "Office",
        "cad": "CAD",
        "os": "Operating Systems" if not de else "Betriebssysteme",
        "pm_tools": "Project Management Tools",
        "mrp": "ERP/MRP",
        "pdm": "PDM",
    }
    for cat, items in skill_groups.items():
        skills_out.append({
            "name": cat_labels.get(cat, cat),
            "keywords": [f"{i['name']} ({i['level']})" for i in items],
        })

    # Education
    edu_out = []
    for e in education:
        edu_out.append({
            "institution": e["institution"],
            "area": e["field_de"] if de else e["field_en"],
            "studyType": e["degree_de"] if de else e["degree_en"],
            "startDate": e["date_from"],
            "endDate": e["date_to"] or "",
            "score": e.get("grade", ""),
            "courses": [],
        })

    # Certifications
    cert_out = []
    for c in certs:
        cert_out.append({
            "name": c["name_de"] if de else c["name_en"],
            "issuer": c["issuer"],
            "date": c["date_from"],
            "url": "",
        })

    # Awards
    awards_out = []
    for a in awards:
        awards_out.append({
            "title": a["name_de"] if de else a["name_en"],
            "date": str(a["year"]),
            "awarder": "",
        })

    # Languages
    lang_out = []
    for la in languages:
        lang_out.append({
            "language": la["language_de"] if de else la["language_en"],
            "fluency": la["level_de"] if de else la["level_en"],
        })

    return {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
        "basics": {
            "name": personal["title_de"] if de else personal["title_en"],
            "label": personal["summary_de"] if de else personal["summary_en"],
            "email": personal["email"],
            "phone": personal["phone"],
            "url": personal["website"],
            "location": {
                "address": personal["street"],
                "postalCode": personal["zip_code"],
                "city": personal["city"],
                **({"countryCode": country_code(personal)} if country_code(personal) else {}),
            },
            "profiles": [
                {
                    "network": "LinkedIn",
                    "url": personal.get("linkedin_url", ""),
                },
                {
                    "network": "Website",
                    "url": personal["website"],
                },
            ],
        },
        "work": work_entries,
        "education": edu_out,
        "awards": awards_out,
        "certificates": cert_out,
        "skills": skills_out,
        "languages": lang_out,
        "meta": {
            "canonical": f"{SITE_URL}/career/profile.json",
            "version": personal.get("updated_at", ""),
            "lastModified": personal.get("updated_at", ""),
        },
    }


# ---------------------------------------------------------------------------
# Full Markdown builder
# ---------------------------------------------------------------------------

def build_full_markdown(conn, lang="en"):
    de = lang == "de"
    personal = query_all(conn, "personal_info")[0]
    work_exp = query_all(conn, "work_experience")
    projects = query_all(conn, "projects")
    education = query_all(conn, "education")
    certs = query_all(conn, "certifications")
    skills_raw = query_all(conn, "skills")
    languages = query_all(conn, "languages")
    awards = query_all(conn, "awards")
    hobbies = query_all(conn, "hobbies")
    memberships = query_all(conn, "memberships")
    driving = query_all(conn, "driving_licenses")

    proj_by_we = {}
    for p in projects:
        proj_by_we.setdefault(p["work_experience_id"], []).append(p)

    lines = []
    name = personal["title_de"] if de else personal["title_en"]
    summary = personal["summary_de"] if de else personal["summary_en"]

    lines.append(f"# {name}")
    lines.append("")
    lines.append(blockquote(summary))
    lines.append("")
    lines.append(f"- **{'Standort' if de else 'Location'}:** {personal['city']}, {personal['country_de'] if de else personal['country_en']}")
    lines.append(f"- **E-Mail:** {personal['email']}")
    lines.append(f"- **{'Telefon' if de else 'Phone'}:** {personal['phone']}")
    lines.append(f"- **Website:** {personal['website']}")
    if personal.get("linkedin_url"):
        lines.append(f"- **LinkedIn:** {personal['linkedin_url']}")
    lines.append("")

    # Languages
    lines.append(f"## {'Sprachen' if de else 'Languages'}")
    for la in languages:
        lines.append(f"- {la['language_de'] if de else la['language_en']}: {la['level_de'] if de else la['level_en']}")
    lines.append("")

    # Work Experience
    lines.append(f"## {'Berufserfahrung' if de else 'Work Experience'}")
    for we in work_exp:
        end = we["date_to"] or ("heute" if de else "present")
        role = we["role_de"] if de else we["role_en"]
        lines.append(f"### {we['employer']} — {role}")
        lines.append(f"*{we['date_from']} – {end}* | {we.get('location', '')}")
        desc = we["description_de"] if de else we["description_en"]
        if desc:
            lines.append("")
            lines.append(desc)

        we_projects = proj_by_we.get(we["id"], [])
        if we_projects:
            lines.append("")
            lines.append(f"**{'Projekte' if de else 'Projects'}:**")
            for p in we_projects:
                p_title = p["title_de"] if de else p["title_en"]
                p_desc = p["description_de"] if de else p["description_en"]
                client = f" ({p['client']})" if p.get("client") else ""
                p_end = p["date_to"] or ("heute" if de else "present")
                lines.append(f"- **{p_title}{client}** ({p['date_from']} – {p_end}): {p_desc}")
        lines.append("")

    # Education
    lines.append(f"## {'Ausbildung' if de else 'Education'}")
    for e in education:
        degree = e["degree_de"] if de else e["degree_en"]
        field = e["field_de"] if de else e["field_en"]
        end = e["date_to"] or ""
        lines.append(f"### {e['institution']}")
        lines.append(f"*{degree} — {field}* | {e['date_from']} – {end}")
        if e.get("grade"):
            lines.append(f"{'Note' if de else 'Grade'}: {e['grade']}")
        thesis = e["thesis_de"] if de else e["thesis_en"]
        if thesis:
            lines.append(f"{'Thesis' if not de else 'Abschlussarbeit'}: {thesis}")
        lines.append("")

    # Skills
    lines.append(f"## {'Kenntnisse' if de else 'Skills'}")
    skill_groups = {}
    for s in skills_raw:
        skill_groups.setdefault(s["category"], []).append(s)
    cat_labels = {
        "llm_infrastructure": "LLM-Infrastruktur" if de else "LLM Infrastructure",
        "ai_automation": "AI & Automation",
        "programming": "Programmierung" if de else "Programming",
        "backend": "Backend & DevOps",
        "databases": "Datenbanken" if de else "Databases",
        "medtech": "Medizintechnik" if de else "Medical Technology",
        "office": "Office",
        "cad": "CAD",
        "os": "Betriebssysteme" if de else "Operating Systems",
        "pm_tools": "Projektmanagement-Tools" if de else "Project Management Tools",
        "mrp": "ERP/MRP",
        "pdm": "PDM",
    }
    for cat, items in skill_groups.items():
        label = cat_labels.get(cat, cat)
        kw = ", ".join(f"{s['name']} ({s['level_de'] if de else s['level_en']})" for s in items)
        lines.append(f"- **{label}:** {kw}")
    lines.append("")

    # Certifications
    lines.append(f"## {'Zertifikate' if de else 'Certifications'}")
    cat_cert_labels = {
        "ai_data": "AI & Data",
        "ai_healthcare": "AI Healthcare",
        "quality": "Qualität" if de else "Quality",
        "management": "Management",
        "misc": "Sonstige" if de else "Other",
    }
    cert_groups = {}
    for c in certs:
        cert_groups.setdefault(c["category"], []).append(c)
    for cat, items in cert_groups.items():
        label = cat_cert_labels.get(cat, cat)
        lines.append(f"### {label}")
        for c in items:
            cname = c["name_de"] if de else c["name_en"]
            lines.append(f"- **{cname}** — {c['issuer']} ({c['date_from']})")
        lines.append("")

    # Awards
    if awards:
        lines.append(f"## {'Auszeichnungen' if de else 'Awards'}")
        for a in awards:
            lines.append(f"- {a['name_de'] if de else a['name_en']} ({a['year']})")
        lines.append("")

    # Driving licenses
    if driving:
        lines.append(f"## {'Führerscheine' if de else 'Driving Licenses'}")
        for d in driving:
            lines.append(f"- {d['name_de'] if de else d['name_en']}")
        lines.append("")

    # Memberships
    if memberships:
        lines.append(f"## {'Mitgliedschaften' if de else 'Memberships'}")
        for m in memberships:
            lines.append(f"- {m['organization']}: {m['description_de'] if de else m['description_en']}")
        lines.append("")

    # Hobbies
    if hobbies:
        lines.append(f"## {'Interessen' if de else 'Interests'}")
        hobby_list = ", ".join(h["name_de"] if de else h["name_en"] for h in hobbies)
        lines.append(hobby_list)
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"{'Letzte Aktualisierung' if de else 'Last updated'}: {personal.get('updated_at', 'n/a')}")
    lines.append(f"{'Quelle' if de else 'Source'}: {SITE_URL}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# schema.org JSON-LD builder
# ---------------------------------------------------------------------------

def build_schema_jsonld(conn):
    personal = query_all(conn, "personal_info")[0]
    work_exp = query_all(conn, "work_experience")
    education = query_all(conn, "education")
    certs = query_all(conn, "certifications")
    skills_raw = query_all(conn, "skills")
    languages = query_all(conn, "languages")
    awards = query_all(conn, "awards")

    occupations = []
    for we in work_exp:
        occupations.append({
            "@type": "Role",
            "roleName": we["role_en"],
            "startDate": we["date_from"],
            "endDate": we["date_to"] or "",
            "description": we["description_en"] or "",
            "memberOf": {
                "@type": "Organization",
                "name": we["employer"],
            },
        })

    alumni_of = []
    for e in education:
        alumni_of.append({
            "@type": "EducationalOrganization",
            "name": e["institution"],
            "location": e["location"],
        })

    credentials = []
    for c in certs:
        credentials.append({
            "@type": "EducationalOccupationalCredential",
            "name": c["name_en"],
            "credentialCategory": c["category"],
            "recognizedBy": {
                "@type": "Organization",
                "name": c["issuer"],
            },
            "dateCreated": c["date_from"],
        })

    knows_about = list({s["name"] for s in skills_raw})
    knows_language = []
    for la in languages:
        knows_language.append({
            "@type": "Language",
            "name": la["language_en"],
            "alternateName": la["language_de"],
        })

    award_list = []
    for a in awards:
        award_list.append(f"{a['name_en']} ({a['year']})")

    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": personal["title_en"],
        "givenName": personal["first_name"],
        "familyName": personal["last_name"],
        "email": f"mailto:{personal['email']}",
        "telephone": personal["phone"],
        "url": personal["website"],
        "image": f"{SITE_URL}/assets/michael-schiffer.jpg",
        "jobTitle": "Senior Program Manager & Process Optimizer",
        "description": personal["summary_en"],
        "birthDate": personal["birth_date"],
        "birthPlace": {
            "@type": "Place",
            "name": personal["birth_place"],
        },
        "nationality": {
            "@type": "Country",
            "name": "Germany",
        },
        "address": {
            "@type": "PostalAddress",
            "streetAddress": personal["street"],
            "postalCode": personal["zip_code"],
            "addressLocality": personal["city"],
            **({"addressCountry": country_code(personal)} if country_code(personal) else {}),
        },
        "sameAs": [
            personal.get("linkedin_url", ""),
            "https://the-implementers.de",
            "https://x.com/SchifferMichael",
        ],
        "hasOccupation": occupations,
        "alumniOf": alumni_of,
        "hasCredential": credentials,
        "knowsAbout": sorted(knows_about),
        "knowsLanguage": knows_language,
        "award": award_list,
    }


# ---------------------------------------------------------------------------
# llms.txt builder
# ---------------------------------------------------------------------------

def build_llms_txt(conn):
    personal = query_all(conn, "personal_info")[0]
    return f"""# {personal['title_en']}

{blockquote(personal['summary_en'])}

## Contact
- Email: {personal['email']}
- Phone: {personal['phone']}
- Location: {personal['city']}, {personal['country_en']}
- Website: {SITE_URL}
- LinkedIn: {personal.get('linkedin_url', '')}

## Machine-Readable Formats

Full career data (complete work history, projects, certifications, skills):
- Markdown (DE): {SITE_URL}/career/de/profile.md
- Markdown (EN): {SITE_URL}/career/en/profile.md
- JSON Resume (DE): {SITE_URL}/career/de/profile.json
- JSON Resume (EN): {SITE_URL}/career/en/profile.json
- Schema.org JSON-LD: {SITE_URL}/career/schema.jsonld

Curated profile summary:
- JSON: {SITE_URL}/de/machine-readable/profile.json
- Markdown: {SITE_URL}/de/machine-readable/profile.md
- Plain text: {SITE_URL}/de/machine-readable/profile.txt

## About This File
This is an llms.txt file — a standard way to provide LLM-friendly content.
See https://llmstxt.org for more information.
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate career data formats from the career device API")
    parser.add_argument("--json", type=Path, help="Fertigen career_data.json-Export lesen statt der API")
    parser.add_argument("--db", type=Path, help="Altbestand: lokale career.db lesen")
    parser.add_argument("--no-export", action="store_true", help="public/career/career_data.json nicht neu schreiben")
    args = parser.parse_args()

    print("generate-career-formats: starting...")

    # Get data
    if args.json and args.json.exists():
        conn = load_json_export(args.json)
    elif args.db and args.db.exists():
        conn = load_sqlite(args.db)
    else:
        conn = fetch_api()

    # Roh-Export für die Website-UI (src/lib/careerData.js liest genau diese Datei)
    if not args.no_export:
        export_path = PUBLIC_DIR / "career" / "career_data.json"
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export = {t: query_all(conn, t) for t in TABLES}
        export_path.write_text(json.dumps(export, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  Written: {export_path.relative_to(ROOT_DIR)}")

    # Generate outputs
    for lang in ("de", "en"):
        career_dir = PUBLIC_DIR / "career" / lang
        career_dir.mkdir(parents=True, exist_ok=True)

        # JSON Resume
        json_resume = build_json_resume(conn, lang)
        json_path = career_dir / "profile.json"
        json_path.write_text(json.dumps(json_resume, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  Written: {json_path.relative_to(ROOT_DIR)}")

        # Full Markdown
        md = build_full_markdown(conn, lang)
        md_path = career_dir / "profile.md"
        md_path.write_text(md, encoding="utf-8")
        print(f"  Written: {md_path.relative_to(ROOT_DIR)}")

    # Schema.org JSON-LD (language-neutral, English)
    schema = build_schema_jsonld(conn)
    schema_path = PUBLIC_DIR / "career" / "schema.jsonld"
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  Written: {schema_path.relative_to(ROOT_DIR)}")

    # llms.txt (root level)
    llms = build_llms_txt(conn)
    llms_path = PUBLIC_DIR / "llms.txt"
    llms_path.write_text(llms, encoding="utf-8")
    print(f"  Written: {llms_path.relative_to(ROOT_DIR)}")

    conn.close()
    print("generate-career-formats: done.")


if __name__ == "__main__":
    main()
