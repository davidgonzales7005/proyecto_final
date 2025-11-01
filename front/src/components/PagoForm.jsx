"use client"

import { useState } from "react"
import axios from "axios"

export default function PagoForm({ onToast }) {
  const [formData, setFormData] = useState({ pedido_id: "", monto: "" })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.pedido_id || !formData.monto) {
      onToast("Completa todos los campos", "error")
      return
    }

    setLoading(true)
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/pagos`, {
        pedido_id: formData.pedido_id,
        monto: Number.parseFloat(formData.monto),
      })
      const type = response.data.estado === "CONFIRMADO" ? "success" : "success"
      onToast(`Pago registrado: ${response.data.estado}`, type)
      setFormData({ pedido_id: "", monto: "" })
    } catch (error) {
      onToast(error.response?.data?.message || "Error al registrar pago", "error")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Registrar Pago</h2>

      <input
        type="text"
        name="pedido_id"
        placeholder="ID Pedido"
        value={formData.pedido_id}
        onChange={handleChange}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        type="number"
        name="monto"
        placeholder="Monto"
        step="0.01"
        value={formData.monto}
        onChange={handleChange}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Procesando..." : "Registrar Pago"}
      </button>
    </form>
  )
}
