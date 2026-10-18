"use client";

import { useState } from "react";

const copy = {
  de: {
    title: "Projekte",
    present: "heute",
    hint: (n) => `${n} ${n === 1 ? "Projekt" : "Projekte"} – klicken für Details`,
  },
  en: {
    title: "Projects",
    present: "present",
    hint: (n) => `${n} ${n === 1 ? "project" : "projects"} – click for details`,
  },
};

function ProjectItem({ project, t }) {
  const [expanded, setExpanded] = useState(false);
  const hasDetail =
    project.description && project.description !== project.descriptionShort;

  const head = (
    <>
      <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-implementers-blue" />
      <span>
        <span className="font-medium">{project.title}</span>
        {project.client && <span className="text-slate-500"> ({project.client})</span>}
        <span className="text-slate-400 text-xs ml-1">
          {project.dateFrom}–{project.dateTo || t.present}
        </span>
        {hasDetail && (
          <span className="ml-1.5 text-xs text-slate-400">{expanded ? "▲" : "▼"}</span>
        )}
      </span>
    </>
  );

  if (!hasDetail) {
    return <li className="flex gap-2 py-1">{head}</li>;
  }

  return (
    <li>
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        aria-expanded={expanded}
        className="flex w-full gap-2 rounded-lg py-1 text-left transition hover:bg-slate-50"
      >
        {head}
      </button>
      {expanded && (
        <p className="mb-2 ml-3.5 border-l-2 border-slate-200 pl-3 text-sm leading-relaxed text-slate-700 whitespace-pre-line">
          {project.description}
        </p>
      )}
    </li>
  );
}

export default function JobProjects({ projects, lang }) {
  const t = copy[lang] ?? copy.de;
  if (!projects?.length) return null;

  const expandable = projects.filter(
    (p) => p.description && p.description !== p.descriptionShort,
  ).length;

  return (
    <div className="mt-3 border-t border-slate-100 pt-3">
      <div className="mb-2 flex flex-wrap items-baseline gap-2">
        <span className="text-xs font-semibold uppercase tracking-wide text-slate-400">
          {t.title}
        </span>
        {expandable > 0 && (
          <span className="text-xs text-slate-400">{t.hint(expandable)}</span>
        )}
      </div>
      <ul className="space-y-0.5 text-sm text-slate-700">
        {projects.map((p) => (
          <ProjectItem key={p.id} project={p} t={t} />
        ))}
      </ul>
    </div>
  );
}
