import { UploadCloud, FileText } from 'lucide-react'
import { useRef, useState } from 'react'

const acceptedTypes = ['application/pdf', 'image/png', 'image/jpeg']

export default function FileUpload({ onFileSelect, loading }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)

  const handleFile = (file) => {
    if (!file) return
    if (!acceptedTypes.includes(file.type)) {
      alert('Only invoice PDF, JPG, and PNG files are supported.')
      return
    }
    onFileSelect(file)
  }

  return (
    <div
      className={`card p-8 transition ${dragging ? 'border-brand-500 ring-2 ring-brand-500/50' : ''}`}
      onDragOver={(e) => {
        e.preventDefault()
        setDragging(true)
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault()
        setDragging(false)
        handleFile(e.dataTransfer.files?.[0])
      }}
    >
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept=".pdf,.png,.jpg,.jpeg"
        onChange={(e) => handleFile(e.target.files?.[0])}
      />
      <div className="flex flex-col items-center gap-4 text-center">
        <div className="rounded-full bg-brand-500/10 p-4 text-brand-500">
          <UploadCloud size={36} />
        </div>
        <div>
          <h2 className="text-2xl font-semibold text-white">Upload invoice</h2>
          <p className="mt-2 max-w-xl text-sm text-slate-400">
            Drag and drop an invoice PDF, JPG, or PNG. This assistant is invoice-only and will return null for fields not found.
          </p>
        </div>
        <button
          type="button"
          disabled={loading}
          onClick={() => inputRef.current?.click()}
          className="inline-flex items-center gap-2 rounded-xl bg-brand-500 px-5 py-3 font-medium text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <FileText size={18} />
          {loading ? 'Processing...' : 'Choose invoice file'}
        </button>
      </div>
    </div>
  )
}
