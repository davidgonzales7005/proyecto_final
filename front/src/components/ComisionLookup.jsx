"use client"

import { useState } from "react"
import axios from "axios"
import Card from "./Card"
import Spinner from "./Spinner"

export default function ComisionLookup({ onToast }) {
  const [formData, setFormData] = useState({ distribuidor_id: "", periodo: "" })
  const [comision, setComision] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSearch = async () => {
    if (!formData.distribuidor_id || !formData.periodo) {
      onToast("Completa todos los campos", "error")
      return
    }

    setLoading(true)
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/comisiones/${formData.distribuidor_id}/${formData.periodo}`,
      )
      setComision(response.data)
    } catch (error) {
      onToast(error.response?.data?.message || "Comisión no encontrada", "error")
      setComision(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Consultar Comisión</h2>

      <div className="grid grid-cols-2 gap-2">
        <input
          type="text"
          name="distribuidor_id"
          placeholder="ID Distribuidor"
          value={formData.distribuidor_id}
          onChange={handleChange}
          className="rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <input
          type="text"
          name="periodo"
          placeholder="Período (YYYY-MM)"
          value={formData.periodo}
          onChange={handleChange}
          className="rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        onClick={handleSearch}
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        Buscar
      </button>

      {loading && <Spinner />}

      {comision && (
        <Card className="space-y-3">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Distribuidor</p>
              <p className="text-lg font-semibold text-gray-900">{comision.distribuidor_id}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Período</p>
              <p className="text-lg font-semibold text-gray-900">{comision.periodo}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Ventas Total</p>
              <p className="text-lg font-semibold text-gray-900">
                ${Number.parseFloat(comision.ventas_total).toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Tasa</p>
              <p className="text-lg font-semibold text-gray-900">{comision.tasa}%</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Monto Comisión</p>
              <p className="text-lg font-semibold text-green-600">${Number.parseFloat(comision.monto).toFixed(2)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Fecha Cálculo</p>
              <p className="text-gray-900">{new Date(comision.fecha_calculo).toLocaleDateString("es-AR")}</p>
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}
