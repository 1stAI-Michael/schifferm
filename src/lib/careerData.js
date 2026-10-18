import fs from "fs";
import path from "path";

let _cache = null;

function loadRaw() {
  if (_cache) return _cache;
  const jsonPath = path.join(process.cwd(), "public", "career", "career_data.json");
  _cache = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
  return _cache;
}

function l(obj, field, lang) {
  return obj[`${field}_${lang}`] ?? obj[`${field}_de`] ?? null;
}

// ---------------------------------------------------------------------------
// Category metadata (colors map to Tailwind classes in components)
// ---------------------------------------------------------------------------

export const categoryMeta = {
  ai:            { de: "KI & GenAI",       en: "AI & GenAI",       color: "emerald" },
  manufacturing: { de: "Industrie",        en: "Manufacturing",    color: "amber" },
  healthcare:    { de: "Healthcare",       en: "Healthcare",       color: "cyan" },
  consulting:    { de: "Beratung",         en: "Consulting",       color: "teal" },
};

export const certCategoryMeta = {
  ai_data:       { de: "AI & Data",          en: "AI & Data",          color: "emerald" },
  ai_healthcare: { de: "AI Healthcare",      en: "AI Healthcare",      color: "cyan" },
  quality:       { de: "Qualität",           en: "Quality",            color: "amber" },
  management:    { de: "Management",         en: "Management",         color: "violet" },
  misc:          { de: "Sonstige",           en: "Other",              color: "slate" },
};

export const skillCategoryMeta = {
  llm_infrastructure: { de: "LLM-Infrastruktur",   en: "LLM Infrastructure" },
  programming:   { de: "Programmierung",           en: "Programming" },
  ai_automation: { de: "KI & Automatisierung",     en: "AI & Automation" },
  backend:       { de: "Backend & DevOps",         en: "Backend & DevOps" },
  databases:     { de: "Datenbanken",              en: "Databases" },
  medtech:       { de: "Medizintechnik",           en: "Medical Technology" },
  office:        { de: "Office",                   en: "Office" },
  cad:           { de: "CAD",                      en: "CAD" },
  pm_tools:      { de: "Projektmanagement-Tools",  en: "Project Management Tools" },
  os:            { de: "Betriebssysteme",          en: "Operating Systems" },
  pdm:           { de: "PDM",                      en: "PDM" },
  mrp:           { de: "ERP / MRP",                en: "ERP / MRP" },
};

// ---------------------------------------------------------------------------
// Data accessors
// ---------------------------------------------------------------------------

// Felder aus personal_info, die auf der öffentlichen Seite nicht gerendert werden
// (fA-497, Punkt 4): street, zip_code, phone, birth_date, birth_place,
// marital_status_de, marital_status_en. Sie bleiben absichtlich in
// career_data.json — die Auswahl passiert hier beim Lesen, nicht in den Daten.
export function getPersonalInfo(lang) {
  const raw = loadRaw().personal_info[0];
  const summary = l(raw, "summary", lang) ?? "";
  return {
    name: l(raw, "title", lang),
    summary,
    summaryParagraphs: summary
      .split("\n\n")
      .map((p) => p.trim())
      .filter(Boolean),
    email: raw.email,
    website: raw.website,
    linkedinUrl: raw.linkedin_url,
    city: raw.city,
    country: l(raw, "country", lang),
    citizenship: l(raw, "citizenship", lang),
  };
}

export function getWorkExperience(lang) {
  const raw = loadRaw().work_experience;
  const projects = loadRaw().projects;
  return raw.map((we) => ({
    id: we.id,
    employer: we.employer,
    role: l(we, "role", lang),
    description: l(we, "description", lang),
    level: l(we, "level", lang),
    department: l(we, "department", lang),
    industry: l(we, "industry", lang),
    location: we.location,
    dateFrom: we.date_from,
    dateTo: we.date_to,
    isCurrent: we.is_current === 1,
    projects: projects
      .filter((p) => p.work_experience_id === we.id)
      .map((p) => formatProject(p, lang)),
  }));
}

// Aufeinanderfolgende Stationen desselben Arbeitgebers zu einem Block bündeln
// (fA-497, Punkt 2 — reine Darstellung, jede Station behält ihre eigene Zeile).
export function getWorkExperienceGrouped(lang) {
  const groups = [];
  for (const job of getWorkExperience(lang)) {
    const last = groups[groups.length - 1];
    if (last && last.employer === job.employer) {
      last.stations.push(job);
    } else {
      groups.push({ employer: job.employer, stations: [job] });
    }
  }
  return groups.map((g) => {
    const from = g.stations.map((s) => s.dateFrom).filter(Boolean).sort();
    const to = g.stations.map((s) => s.dateTo).filter(Boolean).sort();
    const isCurrent = g.stations.some((s) => s.isCurrent || !s.dateTo);
    return {
      ...g,
      id: g.stations[0].id,
      isGrouped: g.stations.length > 1,
      dateFrom: from[0] ?? null,
      dateTo: isCurrent ? null : to[to.length - 1] ?? null,
      isCurrent,
    };
  });
}

function formatProject(p, lang) {
  return {
    id: p.id,
    title: l(p, "title", lang),
    description: l(p, "description", lang),
    descriptionShort: l(p, "description_short", lang),
    client: p.client,
    category: p.category,
    dateFrom: p.date_from,
    dateTo: p.date_to,
  };
}

export function getProjects(lang) {
  const raw = loadRaw().projects;
  return raw.map((p) => formatProject(p, lang));
}

export function getSkills(lang) {
  const raw = loadRaw().skills;
  return raw.map((s) => ({
    id: s.id,
    name: s.name,
    category: s.category,
    level: l(s, "level", lang),
  }));
}

export function getSkillsGrouped(lang) {
  const skills = getSkills(lang);
  const order = ["llm_infrastructure", "programming", "ai_automation", "backend", "databases", "medtech", "office", "cad", "pm_tools", "os", "pdm", "mrp"];
  const grouped = {};
  for (const s of skills) {
    if (!grouped[s.category]) grouped[s.category] = [];
    grouped[s.category].push(s);
  }
  return order.filter((k) => grouped[k]).map((k) => ({
    category: k,
    label: skillCategoryMeta[k]?.[lang] ?? k,
    items: grouped[k],
  }));
}

export function getCertifications(lang) {
  const raw = loadRaw().certifications;
  return raw.map((c) => ({
    id: c.id,
    name: l(c, "name", lang),
    issuer: c.issuer,
    category: c.category,
    dateFrom: c.date_from,
    description: l(c, "description", lang),
    pdfPath: c.pdf_path,
  }));
}

export function getCertificationsGrouped(lang) {
  const certs = getCertifications(lang);
  const order = ["ai_data", "ai_healthcare", "quality", "management", "misc"];
  const grouped = {};
  for (const c of certs) {
    const cat = c.category || "misc";
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(c);
  }
  return order.filter((k) => grouped[k]).map((k) => ({
    category: k,
    label: certCategoryMeta[k]?.[lang] ?? k,
    color: certCategoryMeta[k]?.color ?? "slate",
    items: grouped[k],
  }));
}

// Zertifikate in „aktuell" und „Altbestand" trennen (fA-497, Punkt 3).
// Der Altbestand — quality + misc, überwiegend 1993–2001 — bleibt vollständig
// erhalten, wandert aber hinter einen Aufklapper.
const ARCHIVED_CERT_CATEGORIES = ["quality", "misc"];

export function getCertificationsSplit(lang) {
  const groups = getCertificationsGrouped(lang);
  const archived = groups.filter((g) => ARCHIVED_CERT_CATEGORIES.includes(g.category));
  return {
    current: groups.filter((g) => !ARCHIVED_CERT_CATEGORIES.includes(g.category)),
    archived,
    archivedCount: archived.reduce((n, g) => n + g.items.length, 0),
  };
}

export function getEducation(lang) {
  const raw = loadRaw().education;
  return raw.map((e) => ({
    id: e.id,
    institution: e.institution,
    location: e.location,
    degree: l(e, "degree", lang),
    field: l(e, "field", lang),
    grade: e.grade,
    thesis: l(e, "thesis", lang),
    description: l(e, "description", lang),
    dateFrom: e.date_from,
    dateTo: e.date_to,
  }));
}

export function getLanguages(lang) {
  const raw = loadRaw().languages;
  return raw.map((la) => ({
    language: l(la, "language", lang),
    level: l(la, "level", lang),
  }));
}

export function getAwards(lang) {
  const raw = loadRaw().awards;
  return raw.map((a) => ({
    name: l(a, "name", lang),
    year: a.year,
    pdfPath: a.pdf_path,
  }));
}

export function getDrivingLicenses(lang) {
  const raw = loadRaw().driving_licenses;
  return raw.map((d) => ({
    name: l(d, "name", lang),
  }));
}

export function getHobbies(lang) {
  const raw = loadRaw().hobbies;
  return raw.map((h) => ({
    name: l(h, "name", lang),
  }));
}

export function getMemberships(lang) {
  const raw = loadRaw().memberships;
  return raw.map((m) => ({
    organization: m.organization,
    description: l(m, "description", lang),
  }));
}
