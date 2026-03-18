export default function SectionCard({ title, children, action }) {
  return (
    <section className="card p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        {action}
      </div>
      {children}
    </section>
  )
}
