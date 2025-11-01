export default function Card({ children, className = "" }) {
  return <div className={`bg-white rounded-2xl shadow-sm p-4 border border-gray-100 ${className}`}>{children}</div>
}
