import Card from "../components/Card"
import ComisionLookup from "../components/ComisionLookup"

export default function Comisiones({ onToast }) {
  return (
    <div className="flex justify-center">
      <Card className="max-w-lg w-full">
        <ComisionLookup onToast={onToast} />
      </Card>
    </div>
  )
}
