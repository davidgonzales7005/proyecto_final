"use client"

export default function Navbar({ activeTab, setActiveTab }) {
  const tabs = [
    { id: "pedidos", label: "Pedidos" },
    { id: "pagos", label: "Pagos" },
    { id: "comisiones", label: "Comisiones" },
  ]

  return (
    <nav className="sticky top-0 bg-white shadow-md border-b-2 border-red-600 z-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-20">
          <div className="flex items-center gap-3">
            <img src="/alicorp-logo.png" alt="Alicorp" className="h-12 object-contain" />
            <span className="text-gray-300 text-sm font-light">|</span>
            <h1 className="text-lg font-bold text-gray-900">Portal Pedidos</h1>
          </div>

          <div className="flex gap-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-2 font-medium rounded-md transition-all ${
                  activeTab === tab.id ? "bg-red-600 text-white shadow-md" : "text-gray-600 hover:bg-gray-100"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
