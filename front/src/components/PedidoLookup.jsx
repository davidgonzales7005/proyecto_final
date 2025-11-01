"use client"

import { useState } from "react"
import axios from "axios"
import Card from "./Card"
import Spinner from "./Spinner"
import Badge from "./Badge"

export default function PedidoLookup({ onToast }) {
  const [pedidoId, setPedidoId] = useState("")
  const [pedido, setPedido] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!pedidoId.trim()) {
      onToast("Ingresa un ID de pedido", "error")
      return
    }

    setLoading(true)
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/pedidos/${pedidoId}`)
      setPedido(response.data)
    } catch (error) {
      onToast(error.response?.data?.message || "Pedido no encontrado", "error")
      setPedido(null)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSearch()
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Buscar Pedido</h2>

      <div className="flex gap-2">
        <input
          type="text"
          placeholder="ID Pedido"
          value={pedidoId}
          onChange={(e) => setPedidoId(e.target.value)}
          onKeyPress={handleKeyPress}
          className="flex-1 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          Buscar
        </button>
      </div>

      {loading && <Spinner />}

      {pedido && (
        <Card className="space-y-3">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">ID Pedido</p>
              <p className="text-lg font-semibold text-gray-900">{pedido.id}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Cliente</p>
              <p className="text-lg font-semibold text-gray-900">{pedido.cliente_id}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Total</p>
              <p className="text-lg font-semibold text-gray-900">${Number.parseFloat(pedido.total).toFixed(2)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Estado</p>
              <Badge status={pedido.estado} />
            </div>
            <div className="col-span-2">
              <p className="text-sm text-gray-600">Fecha</p>
              <p className="text-gray-900">{new Date(pedido.fecha).toLocaleDateString("es-AR")}</p>
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}
