import { buildMetadata } from "../../../lib/seo";
import { profileContent } from "../../../content/profile";
import { getLocale } from "../../../lib/content";
import { siteConfig } from "../../../lib/site";
import {
  getPersonalInfo,
  getWorkExperienceGrouped,
  getEducation,
  getSkillsGrouped,
  getCertificationsSplit,
  getLanguages,
  getAwards,
  getDrivingLicenses,
  getHobbies,
  getMemberships,
} from "../../../lib/careerData";
import LevelDots from "../../../components/LevelDots";
import JobProjects from "../../../components/career/JobProjects";
import CertGroup from "../../../components/career/CertGroup";
import ArchivedCertifications from "../../../components/career/ArchivedCertifications";

export const dynamicParams = false;

export function generateStaticParams() {
  return siteConfig.locales.map((lang) => ({ lang }));
}

const copy = {
  de: {
    pageTitle: "Vollständiger Lebenslauf",
    summary: "Zusammenfassung",
    contact: "Kontakt",
    experience: "Berufserfahrung",
    education: "Ausbildung",
    skills: "Kenntnisse",
    certifications: "Zertifikate",
    languages: "Sprachen",
    awards: "Auszeichnungen",
    drivingLicenses: "Führerscheine",
    hobbies: "Interessen",
    memberships: "Mitgliedschaften",
    present: "heute",
    download: "Maschinenlesbare Formate",
    downloadHint: "Diese Daten sind auch in maschinenlesbaren Formaten verfügbar:",
    projects: "Projekte",
    thesis: "Abschlussarbeit",
    grade: "Note",
    stations: (n) => `${n} Stationen`,
  },
  en: {
    pageTitle: "Full Curriculum Vitae",
    summary: "Summary",
    contact: "Contact",
    experience: "Work Experience",
    education: "Education",
    skills: "Skills",
    certifications: "Certifications",
    languages: "Languages",
    awards: "Awards",
    drivingLicenses: "Driving Licenses",
    hobbies: "Interests",
    memberships: "Memberships",
    present: "present",
    download: "Machine-Readable Formats",
    downloadHint: "This data is also available in machine-readable formats:",
    projects: "Projects",
    thesis: "Thesis",
    grade: "Grade",
    stations: (n) => `${n} positions`,
  },
};

export async function generateMetadata({ params }) {
  const resolvedParams = await params;
  const lang = getLocale(resolvedParams?.lang);
  const title = `${copy[lang].pageTitle} | ${profileContent.site.fullName}`;
  const description = lang === "de"
    ? "Vollständiger Lebenslauf mit allen Positionen, Projekten, Zertifikaten und Kenntnissen."
    : "Full CV with all positions, projects, certifications and skills.";
  return buildMetadata({ lang, title, description, path: `/${lang}/career` });
}

export default async function CareerPage({ params }) {
  const resolvedParams = await params;
  const lang = getLocale(resolvedParams?.lang);
  const t = copy[lang];
  const info = getPersonalInfo(lang);
  const workGroups = getWorkExperienceGrouped(lang);
  const education = getEducation(lang);
  const skillGroups = getSkillsGrouped(lang);
  const certs = getCertificationsSplit(lang);
  const languages = getLanguages(lang);
  const awards = getAwards(lang);
  const drivingLicenses = getDrivingLicenses(lang);
  const hobbies = getHobbies(lang);
  const memberships = getMemberships(lang);

  return (
    <section className="mx-auto max-w-4xl px-4 py-16">
      {/* Header */}
      <div className="mb-10">
        <p className="text-xs font-semibold uppercase tracking-wide text-implementers-blue">
          {t.pageTitle}
        </p>
        <h1 className="mt-2 font-heading text-3xl text-slate-900">{info.name}</h1>
        <div className="mt-3 space-y-3 text-base text-slate-700">
          {info.summaryParagraphs.map((paragraph, i) => (
            <p key={i}>{paragraph}</p>
          ))}
        </div>
      </div>

      {/* Contact */}
      <div className="mb-10 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">{t.contact}</h2>
        <div className="mt-3 grid gap-2 text-sm text-slate-700 sm:grid-cols-2">
          <div>
            <a href={`mailto:${info.email}`} className="text-implementers-blue hover:underline">
              {info.email}
            </a>
          </div>
          <div>{info.city}, {info.country}</div>
          <div>
            <a href={info.website} className="text-implementers-blue hover:underline">
              {info.website}
            </a>
          </div>
          {info.linkedinUrl && (
            <div>
              <a href={info.linkedinUrl} className="text-implementers-blue hover:underline" target="_blank" rel="noopener noreferrer">
                LinkedIn
              </a>
            </div>
          )}
        </div>
      </div>

      {/* Languages */}
      {languages.length > 0 && (
        <div className="mb-10 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">{t.languages}</h2>
          <div className="mt-3 flex flex-wrap gap-3">
            {languages.map((la) => (
              <span key={la.language} className="rounded-full border border-slate-200 px-3 py-1 text-sm text-slate-700">
                {la.language}: <span className="font-medium">{la.level}</span>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Work Experience */}
      <div className="mb-10">
        <h2 className="mb-6 text-xl font-semibold text-slate-900">{t.experience}</h2>
        <div className="space-y-6">
          {workGroups.map((group) => (
            <div key={group.id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h3 className="text-base font-semibold text-slate-900">{group.employer}</h3>
                <span className="text-xs font-mono font-medium text-slate-400">
                  {group.dateFrom} – {group.dateTo || t.present}
                </span>
              </div>
              {group.isGrouped && (
                <div className="mt-1 text-xs text-slate-500">{t.stations(group.stations.length)}</div>
              )}

              <div className={group.isGrouped ? "mt-5 space-y-6 border-l-2 border-slate-100 pl-5" : ""}>
                {group.stations.map((job) => (
                  <div key={job.id} className={group.isGrouped ? "relative" : ""}>
                    {group.isGrouped && (
                      <>
                        <span className="absolute -left-[26px] top-1.5 h-2.5 w-2.5 rounded-full border-2 border-white bg-implementers-blue" />
                        <div className="text-xs font-mono text-slate-400">
                          {job.dateFrom} – {job.dateTo || t.present}
                        </div>
                      </>
                    )}
                    <div className="mt-1 text-sm font-medium text-implementers-blue">{job.role}</div>
                    {(job.level || job.department) && (
                      <div className="mt-1 flex flex-wrap gap-2">
                        {job.level && (
                          <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600">{job.level}</span>
                        )}
                        {job.department && (
                          <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600">{job.department}</span>
                        )}
                      </div>
                    )}
                    {job.description && (
                      <p className="mt-2 text-sm text-slate-600">{job.description}</p>
                    )}
                    <JobProjects projects={job.projects} lang={lang} />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Education */}
      <div className="mb-10">
        <h2 className="mb-6 text-xl font-semibold text-slate-900">{t.education}</h2>
        <div className="space-y-4">
          {education.map((edu) => (
            <div key={edu.id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h3 className="text-base font-semibold text-slate-900">{edu.institution}</h3>
                <span className="text-xs font-mono font-medium text-slate-400">
                  {edu.dateFrom} – {edu.dateTo}
                </span>
              </div>
              <div className="mt-1 text-sm font-medium text-implementers-blue">
                {edu.degree} — {edu.field}
              </div>
              {edu.grade && (
                <div className="mt-1 text-xs text-slate-500">{t.grade}: {edu.grade}</div>
              )}
              {edu.thesis && (
                <div className="mt-1 text-xs text-slate-500">{t.thesis}: {edu.thesis}</div>
              )}
              {edu.description && (
                <div className="mt-1 text-xs text-slate-500">{edu.description}</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Skills */}
      <div className="mb-10">
        <h2 className="mb-6 text-xl font-semibold text-slate-900">{t.skills}</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {skillGroups.map((group) => (
            <div key={group.category} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <h3 className="text-sm font-bold uppercase tracking-wider text-implementers-blue mb-3">
                {group.label}
              </h3>
              <div className="space-y-2">
                {group.items.map((skill) => (
                  <div key={skill.id} className="flex items-center justify-between gap-2">
                    <span className="text-sm text-slate-900">{skill.name}</span>
                    <LevelDots level={skill.level} />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Certifications */}
      <div className="mb-10">
        <h2 className="mb-6 text-xl font-semibold text-slate-900">{t.certifications}</h2>
        {certs.current.map((group) => (
          <CertGroup key={group.category} group={group} />
        ))}
        <ArchivedCertifications
          groups={certs.archived}
          count={certs.archivedCount}
          lang={lang}
        />
      </div>

      {/* Awards */}
      {awards.length > 0 && (
        <div className="mb-10">
          <h2 className="mb-6 text-xl font-semibold text-slate-900">{t.awards}</h2>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <ul className="space-y-2 text-sm text-slate-700">
              {awards.map((a) => (
                <li key={a.name}>
                  <span className="font-medium text-slate-900">{a.name}</span>
                  <span className="ml-2 text-xs text-slate-400">({a.year})</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Driving Licenses */}
      {drivingLicenses.length > 0 && (
        <div className="mb-10">
          <h2 className="mb-6 text-xl font-semibold text-slate-900">{t.drivingLicenses}</h2>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-wrap gap-2">
              {drivingLicenses.map((d) => (
                <span key={d.name} className="rounded-full border border-slate-200 px-3 py-1 text-sm text-slate-700">
                  {d.name}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Memberships */}
      {memberships.length > 0 && (
        <div className="mb-10">
          <h2 className="mb-6 text-xl font-semibold text-slate-900">{t.memberships}</h2>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <ul className="space-y-2 text-sm text-slate-700">
              {memberships.map((m) => (
                <li key={m.organization}>
                  <span className="font-medium text-slate-900">{m.organization}</span>
                  {m.description && <span className="ml-2 text-slate-500">— {m.description}</span>}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Hobbies */}
      {hobbies.length > 0 && (
        <div className="mb-10">
          <h2 className="mb-6 text-xl font-semibold text-slate-900">{t.hobbies}</h2>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-wrap gap-2">
              {hobbies.map((h) => (
                <span key={h.name} className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">
                  {h.name}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Machine-readable formats */}
      <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6">
        <h2 className="text-lg font-semibold text-slate-900">{t.download}</h2>
        <p className="mt-2 text-sm text-slate-600">{t.downloadHint}</p>
        <div className="mt-4 flex flex-wrap gap-3">
          <a href={`/career/${lang}/profile.json`} className="rounded-full border border-implementers-blue px-4 py-1.5 text-sm font-medium text-implementers-blue transition hover:bg-implementers-blue hover:text-white">
            JSON Resume
          </a>
          <a href={`/career/${lang}/profile.md`} className="rounded-full border border-implementers-blue px-4 py-1.5 text-sm font-medium text-implementers-blue transition hover:bg-implementers-blue hover:text-white">
            Markdown
          </a>
          <a href="/career/schema.jsonld" className="rounded-full border border-implementers-blue px-4 py-1.5 text-sm font-medium text-implementers-blue transition hover:bg-implementers-blue hover:text-white">
            Schema.org JSON-LD
          </a>
          <a href="/llms.txt" className="rounded-full border border-implementers-blue px-4 py-1.5 text-sm font-medium text-implementers-blue transition hover:bg-implementers-blue hover:text-white">
            llms.txt
          </a>
        </div>
      </div>
    </section>
  );
}
