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

export function getPersonalInfo(lang) {
  const raw = loadRaw().personal_info[0];
  return {
    name: l(raw, "title", lang),
    summary: l(raw, "summary", lang),
    email: raw.email,
    phone: raw.phone,
    website: raw.website,
    linkedinUrl: raw.linkedin_url,
    street: raw.street,
    zip: raw.zip_code,
    city: raw.city,
    country: l(raw, "country", lang),
    birthDate: raw.birth_date,
    birthPlace: raw.birth_place,
    citizenship: l(raw, "citizenship", lang),
    maritalStatus: l(raw, "marital_status", lang),
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
  const order = ["llm_infrastructure", "programming", "ai_automation", "backend", "databases", "office", "cad", "pm_tools", "os", "pdm", "mrp"];
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
