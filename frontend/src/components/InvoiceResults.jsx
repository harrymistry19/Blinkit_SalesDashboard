import { Download, AlertTriangle, ShieldCheck } from 'lucide-react'
import SectionCard from './SectionCard'

const renderValue = (value) => value ?? 'null'

function KeyValueGrid({ data }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {Object.entries(data).map(([key, value]) => (
        <div key={key} className="rounded-xl border border-slate-800 bg-slate-950/60 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{key.replaceAll('_', ' ')}</p>
          <p className="mt-2 break-words text-sm text-slate-200">{renderValue(value)}</p>
        </div>
      ))}
    </div>
  )
}

export default function InvoiceResults({ result }) {
  if (!result) return null

  const downloadJson = () => {
    const blob = new Blob([JSON.stringify(result.extracted_data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${result.filename.replace(/\.[^.]+$/, '') || 'invoice'}-report.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const data = result.extracted_data
  const warnings = data.warnings || []

  return (
    <div className="space-y-6">
      <SectionCard
        title="Structured Invoice Report"
        action={
          <button
            onClick={downloadJson}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800"
          >
            <Download size={16} /> Download JSON
          </button>
        }
      >
        <div className="grid gap-4 lg:grid-cols-3">
          <div className="rounded-2xl bg-emerald-500/10 p-4 text-emerald-300">
            <ShieldCheck className="mb-2" size={18} />
            <p className="text-xs uppercase tracking-[0.2em]">Scope</p>
            <p className="mt-2 text-sm">Invoice-only extraction with null-safe output and validation.</p>
          </div>
          <div className="rounded-2xl bg-sky-500/10 p-4 text-sky-300">
            <p className="text-xs uppercase tracking-[0.2em]">Invoice file</p>
            <p className="mt-2 text-sm">{result.filename}</p>
          </div>
          <div className="rounded-2xl bg-amber-500/10 p-4 text-amber-300">
            <p className="text-xs uppercase tracking-[0.2em]">Warnings</p>
            <p className="mt-2 text-sm">{warnings.length}</p>
          </div>
        </div>
      </SectionCard>

      {warnings.length > 0 && (
        <SectionCard title="Validation warnings">
          <div className="space-y-3">
            {warnings.map((warning) => (
              <div key={warning} className="flex items-start gap-3 rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 text-amber-200">
                <AlertTriangle size={18} className="mt-0.5" />
                <span>{warning}</span>
              </div>
            ))}
          </div>
        </SectionCard>
      )}

      <SectionCard title="Company details">
        <KeyValueGrid data={data.company_details} />
      </SectionCard>

      <SectionCard title="Invoice details">
        <KeyValueGrid data={data.invoice_details} />
      </SectionCard>

      <SectionCard title="Customer details">
        <KeyValueGrid data={data.customer_details} />
      </SectionCard>

      <SectionCard title="Items">
        <div className="overflow-hidden rounded-2xl border border-slate-800">
          <table className="min-w-full divide-y divide-slate-800 text-left text-sm text-slate-200">
            <thead className="bg-slate-950/80 text-slate-400">
              <tr>
                <th className="px-4 py-3">Description</th>
                <th className="px-4 py-3">Quantity</th>
                <th className="px-4 py-3">Rate</th>
                <th className="px-4 py-3">Amount</th>
                <th className="px-4 py-3">Confidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {(data.items?.length ? data.items : [{ description: null, quantity: null, rate: null, amount: null, confidence: null }]).map((item, index) => (
                <tr key={`${item.description}-${index}`} className="bg-slate-900/60">
                  <td className="px-4 py-3">{renderValue(item.description)}</td>
                  <td className="px-4 py-3">{renderValue(item.quantity)}</td>
                  <td className="px-4 py-3">{renderValue(item.rate)}</td>
                  <td className="px-4 py-3">{renderValue(item.amount)}</td>
                  <td className="px-4 py-3">{item.confidence ?? 'null'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>

      <div className="grid gap-6 lg:grid-cols-2">
        <SectionCard title="Tax details">
          <KeyValueGrid data={data.tax_details} />
        </SectionCard>
        <SectionCard title="Payment details">
          <KeyValueGrid data={data.payment_details} />
        </SectionCard>
      </div>

      <SectionCard title="Total amount">
        <p className="text-3xl font-semibold text-white">{renderValue(data.total_amount)}</p>
      </SectionCard>

      <SectionCard title="Raw text preview and field source highlights">
        <div className="grid gap-6 lg:grid-cols-2">
          <pre className="max-h-96 overflow-auto rounded-2xl bg-slate-950/70 p-4 text-xs text-slate-300 whitespace-pre-wrap">{data.raw_text_preview}</pre>
          <div className="space-y-3">
            {Object.entries(data.field_sources || {}).slice(0, 12).map(([field, source]) => (
              <div key={field} className="rounded-xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{field}</p>
                <p className="mt-2 text-sm text-slate-200">{source || 'No direct text snippet available.'}</p>
              </div>
            ))}
          </div>
        </div>
      </SectionCard>
    </div>
  )
}
