import { useEffect, useState } from 'react'
import FileUpload from '../components/FileUpload'
import HistoryPanel from '../components/HistoryPanel'
import InvoiceResults from '../components/InvoiceResults'
import Loader from '../components/Loader'
import { fetchHistory, processInvoice, uploadInvoice } from '../services/api'

export default function Dashboard() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [error, setError] = useState('')

  const loadHistory = async () => {
    try {
      const data = await fetchHistory()
      setHistory(data)
    } catch {
      setHistory([])
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  const handleFileSelect = async (file) => {
    setLoading(true)
    setError('')
    try {
      const upload = await uploadInvoice(file)
      const processed = await processInvoice(upload)
      setResult(processed)
      await loadHistory()
    } catch (err) {
      setError(err.response?.data?.detail || 'Invoice processing failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(37,99,235,0.22),_transparent_30%),linear-gradient(180deg,_#020617_0%,_#0f172a_100%)]">
      <div className="mx-auto max-w-7xl px-6 py-10 lg:px-8">
        <header className="mb-10 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <span className="inline-flex rounded-full border border-brand-500/30 bg-brand-500/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.3em] text-brand-500">
              SaaS-ready • Invoice-only AI
            </span>
            <h1 className="mt-4 text-4xl font-semibold tracking-tight text-white lg:text-5xl">
              Invoice AI Assistant
            </h1>
            <p className="mt-4 max-w-3xl text-base leading-7 text-slate-300">
              Upload invoice PDFs or images, run strict Groq-powered extraction, validate totals, flag missing GST or number issues, and export structured JSON.
              Different invoice layouts are handled through OCR + LLM normalization, while missing values remain null instead of guessed.
            </p>
          </div>
        </header>

        <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
          <div className="space-y-6">
            <FileUpload onFileSelect={handleFileSelect} loading={loading} />
            {loading && <Loader />}
            {error && <div className="card border-red-500/30 bg-red-500/10 p-4 text-red-200">{error}</div>}
            <InvoiceResults result={result} />
          </div>
          <div className="space-y-6">
            <div className="card p-6">
              <h2 className="text-lg font-semibold text-white">Why this is production-oriented</h2>
              <ul className="mt-4 space-y-3 text-sm text-slate-300">
                <li>• Restricted to invoice PDF/JPG/PNG workflows only.</li>
                <li>• Strict JSON schema with nulls for missing values.</li>
                <li>• Modular OCR service for future Tesseract replacement.</li>
                <li>• SQLite-backed history for auditability.</li>
                <li>• Validation checks for invoice number and total mismatch warnings.</li>
                <li>• Raw-text snippets and confidence scores for review.</li>
              </ul>
            </div>
            <HistoryPanel history={history} />
          </div>
        </div>
      </div>
    </div>
  )
}
