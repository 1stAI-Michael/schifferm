"use client";

import { useState } from "react";
import CertGroup from "./CertGroup";

const copy = {
  de: {
    label: (n) => `Weitere Qualifikationen (${n})`,
    hint: "Fort- und Weiterbildungen, überwiegend 1993–2001",
  },
  en: {
    label: (n) => `Further qualifications (${n})`,
    hint: "Training and further education, mostly 1993–2001",
  },
};

export default function ArchivedCertifications({ groups, count, lang }) {
  const [open, setOpen] = useState(false);
  const t = copy[lang] ?? copy.de;

  if (!groups.length) return null;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-3 px-6 py-4 text-left transition hover:bg-slate-50"
      >
        <span>
          <span className="text-sm font-bold uppercase tracking-wider text-slate-600">
            {t.label(count)}
          </span>
          <span className="mt-0.5 block text-xs text-slate-400">{t.hint}</span>
        </span>
        <span className="text-xs text-slate-400">{open ? "▲" : "▼"}</span>
      </button>

      {open && (
        <div className="border-t border-slate-100 bg-slate-50/60 px-4 pt-4">
          {groups.map((group) => (
            <CertGroup key={group.category} group={group} />
          ))}
        </div>
      )}
    </div>
  );
}
