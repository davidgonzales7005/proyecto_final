import Card from "../components/Card"
import PagoForm from "../components/PagoForm"

export default function Pagos({ onToast }) {
  return (
    <div className="flex justify-center">
      <Card className="max-w-md w-full">
        <PagoForm onToast={onToast} />
      </Card>
    </div>
  )
}
