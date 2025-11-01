export default function Badge({ status }) {
  const statusConfig = {
    pendiente: { bg: "bg-yellow-100", text: "text-yellow-800" },
    enviado: { bg: "bg-blue-100", text: "text-blue-800" },
    entregado: { bg: "bg-green-100", text: "text-green-800" },
    error: { bg: "bg-red-100", text: "text-red-800" },
    confirmado: { bg: "bg-green-100", text: "text-green-800" },
    rechazado: { bg: "bg-red-100", text: "text-red-800" },
  }

  const config = statusConfig[status] || { bg: "bg-gray-100", text: "text-gray-800" }

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${config.bg} ${config.text}`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  )
}
