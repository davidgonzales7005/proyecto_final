"use client"

import { useState } from "react"
import Navbar from "./components/Navbar"
import Toast from "./components/Toast"
import Pedidos from "./pages/Pedidos"
import Pagos from "./pages/Pagos"
import Comisiones from "./pages/Comisiones"

export default function App() {
  const [activeTab, setActiveTab] = useState("pedidos")
  const [toast, setToast] = useState(null)

  const showToast = (message, type = "success") => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="max-w-6xl mx-auto px-4 py-8">
        {activeTab === "pedidos" && <Pedidos onToast={showToast} />}
        {activeTab === "pagos" && <Pagos onToast={showToast} />}
        {activeTab === "comisiones" && <Comisiones onToast={showToast} />}
      </main>

      {toast && <Toast message={toast.message} type={toast.type} />}
    </div>
  )
}
