export default function CertGroup({ group }) {
  return (
    <div className="mb-4 rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      <div className="flex items-center justify-between px-6 py-3 bg-slate-50">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-600">{group.label}</h3>
        <span className="rounded-full bg-slate-200 px-2.5 py-0.5 text-xs font-semibold text-slate-600">
          {group.items.length}
        </span>
      </div>
      <ul className="px-6 divide-y divide-slate-100">
        {group.items.map((cert) => (
          <li key={cert.id} className="flex flex-wrap items-baseline justify-between gap-2 py-2.5">
            <div>
              <span className="text-sm font-medium text-slate-900">{cert.name}</span>
              {cert.issuer && <span className="ml-2 text-sm text-slate-500">— {cert.issuer}</span>}
            </div>
            <span className="text-xs font-mono text-slate-400">{cert.dateFrom}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
