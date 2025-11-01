# Portal Pedidos

Dashboard SPA en React + Vite + TailwindCSS para gestionar Pedidos, Pagos y Comisiones consumiendo APIs en AWS Lambda.

## Características

- ✅ Navbar con navegación entre tabs (Pedidos, Pagos, Comisiones)
- ✅ Crear y buscar pedidos
- ✅ Registrar y confirmar pagos
- ✅ Consultar comisiones por distribuidor y período
- ✅ Toast notifications (éxito/error)
- ✅ Loading spinners
- ✅ Diseño responsive con Tailwind CSS
- ✅ Sin dependencias pesadas

## Instalación

\`\`\`bash
npm install
\`\`\`

## Configuración

1. Copia `.env.example` a `.env.local`:
\`\`\`bash
cp .env.example .env.local
\`\`\`

2. Reemplaza `<API_GATEWAY_ID>` con tu ID de API Gateway en AWS:
\`\`\`
VITE_API_URL=https://abc123xyz.execute-api.sa-east-1.amazonaws.com/Prod
\`\`\`

## Desarrollo

\`\`\`bash
npm run dev
\`\`\`

La app estará disponible en `http://localhost:5173`

## Build para producción

\`\`\`bash
npm run build
\`\`\`

Genera una carpeta `dist/` lista para publicar.

## Despliegue en S3

1. Ejecuta `npm run build`
2. Sube el contenido de la carpeta `dist/` a tu bucket S3
3. Configura distribución de CloudFront si necesitas HTTPS

## Estructura del Proyecto

\`\`\`
src/
├── components/
│   ├── Badge.jsx           # Estados de pedidos
│   ├── Card.jsx            # Contenedor reutilizable
│   ├── ComisionLookup.jsx  # Búsqueda de comisiones
│   ├── Navbar.jsx          # Navegación principal
│   ├── PagoForm.jsx        # Formulario de pagos
│   ├── PedidoForm.jsx      # Crear pedidos
│   ├── PedidoLookup.jsx    # Buscar pedidos
│   ├── Spinner.jsx         # Loading indicator
│   └── Toast.jsx           # Notificaciones
├── pages/
│   ├── Comisiones.jsx
│   ├── Pagos.jsx
│   └── Pedidos.jsx
├── App.jsx
├── main.jsx
└── index.css

public/                      # Assets estáticos
\`\`\`

## API Endpoints Esperados

- `POST /api/pedidos` - Crear pedido
- `GET /api/pedidos/{id}` - Obtener pedido
- `POST /api/pagos` - Registrar pago
- `GET /api/comisiones/{distribuidor_id}/{periodo}` - Obtener comisión

## Licencia

MIT
