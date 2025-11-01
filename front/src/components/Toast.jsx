export default function Toast({ message, type }) {
  const bgColor = type === "success" ? "bg-green-50" : "bg-red-50"
  const textColor = type === "success" ? "text-green-800" : "text-red-800"
  const borderColor = type === "success" ? "border-green-200" : "border-red-200"

  return (
    <div
      className={`fixed bottom-4 right-4 ${bgColor} border ${borderColor} ${textColor} px-4 py-3 rounded-lg shadow-lg max-w-sm`}
    >
      {message}
    </div>
  )
}
