"use client"

import { useState } from "react"
import axios from "axios"

export default function PedidoForm({ onToast }) {
  const [formData, setFormData] = useState({ cliente_id: "", total: "" })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.cliente_id || !formData.total) {
      onToast("Completa todos los campos", "error")
      return
    }

    setLoading(true)
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/pedidos`, {
        cliente_id: formData.cliente_id,
        total: Number.parseFloat(formData.total),
      })
      onToast(`Pedido #${response.data.id} creado exitosamente`)
      setFormData({ cliente_id: "", total: "" })
    } catch (error) {
      onToast(error.response?.data?.message || "Error al crear pedido", "error")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Crear Pedido</h2>

      <input
        type="text"
        name="cliente_id"
        placeholder="ID Cliente"
        value={formData.cliente_id}
        onChange={handleChange}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        type="number"
        name="total"
        placeholder="Total"
        step="0.01"
        value={formData.total}
        onChange={handleChange}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Creando..." : "Crear Pedido"}
      </button>
    </form>
  )
}
