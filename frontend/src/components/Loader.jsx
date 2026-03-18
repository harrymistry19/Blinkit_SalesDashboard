export default function Loader() {
  return (
    <div className="card flex items-center gap-4 p-6">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-brand-500/30 border-t-brand-500" />
      <div>
        <p className="font-semibold text-white">Analyzing invoice...</p>
        <p className="text-sm text-slate-400">Running modular OCR, Groq extraction, and validation checks.</p>
      </div>
    </div>
  )
}
