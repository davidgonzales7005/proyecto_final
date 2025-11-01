import Card from "../components/Card"
import PedidoForm from "../components/PedidoForm"
import PedidoLookup from "../components/PedidoLookup"

export default function Pedidos({ onToast }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card>
        <PedidoForm onToast={onToast} />
      </Card>
      <Card>
        <PedidoLookup onToast={onToast} />
      </Card>
    </div>
  )
}
