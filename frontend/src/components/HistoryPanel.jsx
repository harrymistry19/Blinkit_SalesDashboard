import SectionCard from './SectionCard'

export default function HistoryPanel({ history }) {
  return (
    <SectionCard title="Processing history">
      <div className="space-y-3">
        {history.length === 0 ? (
          <p className="text-sm text-slate-400">No processed invoices yet.</p>
        ) : (
          history.map((entry) => (
            <div key={entry.id} className="rounded-xl border border-slate-800 bg-slate-950/60 p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <p className="font-medium text-white">{entry.filename}</p>
                  <p className="text-xs text-slate-500">{new Date(entry.created_at).toLocaleString()}</p>
                </div>
                <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">{entry.content_type}</span>
              </div>
              <p className="mt-3 text-sm text-slate-400">
                Invoice #: {entry.extracted_data?.invoice_details?.invoice_number ?? 'null'} · Total: {entry.extracted_data?.total_amount ?? 'null'}
              </p>
            </div>
          ))
        )}
      </div>
    </SectionCard>
  )
}
