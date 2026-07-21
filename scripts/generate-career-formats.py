#!/usr/bin/env python3
"""
Generate machine-readable career data formats from career.db (Nextcloud).

Outputs (into public/):
  - llms.txt                   — LLM discovery file (root)
  - career/profile.json        — JSON Resume format (DE+EN)
  - career/profile.md          — Full markdown (DE+EN)
  - career/schema.jsonld       — schema.org Person JSON-LD

Usage:
  python scripts/generate-career-formats.py [--db /path/to/career.db]

If --db is not given, downloads from Nextcloud WebDAV.
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
PUBLIC_DIR = ROOT_DIR / "public"

WEBDAV_URL = "https://nc.ki-oe.de/remote.php/dav/files/claude/Bewerbung/career.db"
DAVFS_SECRETS = "/etc/davfs2/secrets"
SITE_URL = "https://schifferm.de"


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def get_nc_credentials():
    """Read Nextcloud credentials from davfs2 secrets file."""
    try:
        with open(DAVFS_SECRETS) as f:
            for line in f:
                if "nc.ki-oe.de" in line:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        return parts[1], parts[2]  # user, token
    except PermissionError:
        result = subprocess.run(
            ["sudo", "awk", "/nc.ki-oe.de/ {print $2, $3}", DAVFS_SECRETS],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) >= 2:
                return parts[0], parts[1]
    return None, None


def download_db(target_path):
    """Download career.db from Nextcloud WebDAV."""
    user, token = get_nc_credentials()
    if not user or not token:
        print("ERROR: Could not read Nextcloud credentials", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(
        ["curl", "-sf", "-u", f"{user}:{token}", WEBDAV_URL, "-o", str(target_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: Failed to download career.db: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  Downloaded career.db ({target_path.stat().st_size:,} bytes)")


def query_all(conn, table, order_by=None):
    """Return all rows from a table as list of dicts."""
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if order_by is None:
        cols = [r[1] for r in c.execute(f"PRAGMA table_info({table})")]
        order_by = "sort_order, id" if "sort_order" in cols else "id"
    rows = c.execute(f"SELECT * FROM {table} ORDER BY {order_by}").fetchall()
    return [dict(r) for r in rows]


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
                "countryCode": "DE",
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
    lines.append(f"> {summary}")
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
            "addressCountry": "DE",
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

> {personal['summary_en']}

## Contact
- Email: {personal['email']}
- Phone: {personal['phone']}
- Location: {personal['city']}, Germany
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
    parser = argparse.ArgumentParser(description="Generate career data formats from career.db")
    parser.add_argument("--db", type=Path, help="Path to local career.db (default: download from Nextcloud)")
    args = parser.parse_args()

    print("generate-career-formats: starting...")

    # Get database
    if args.db and args.db.exists():
        db_path = args.db
        print(f"  Using local DB: {db_path}")
    else:
        db_path = Path(tempfile.mkdtemp()) / "career.db"
        download_db(db_path)

    conn = sqlite3.connect(str(db_path))

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
