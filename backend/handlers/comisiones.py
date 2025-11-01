import json
import boto3
import os
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['COMISIONES_TABLE'])

def _dumps(obj):
    # Convierte Decimal/fechas a string para que json.dumps no falle
    return json.dumps(obj, default=str)

def handler(event, context):
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

        # ========= POST: Crear comisión =========
        if method == "POST":
            body = json.loads(event["body"], parse_float=Decimal)

            # Requeridos por el esquema de la tabla:
            #   PK = distribuidor_id (S)
            #   SK = periodo (S)      p.ej. "2025-11"
            distribuidor_id = body.get("distribuidor_id")
            periodo         = body.get("periodo")

            if not distribuidor_id or not periodo:
                return {
                    "statusCode": 400,
                    "body": _dumps({"message": "distribuidor_id y periodo son obligatorios"})
                }

            total_ventas = body.get("total_ventas", Decimal("0"))
            porcentaje   = body.get("porcentaje",  Decimal("0.10"))

            # Si no te mandan comision_calculada, la calculamos
            comision_calculada = body.get("comision_calculada")
            if comision_calculada is None:
                comision_calculada = (total_ventas * porcentaje).quantize(Decimal("0.01"))

            item = {
                "distribuidor_id": distribuidor_id,
                "periodo": periodo,
                "nombre_distribuidor": body.get("nombre_distribuidor"),
                "total_ventas": total_ventas,
                "porcentaje": porcentaje,
                "comision_calculada": comision_calculada,
                "creado_en": datetime.utcnow().isoformat()
            }

            table.put_item(Item=item)

            return {
                "statusCode": 200,
                "body": _dumps({"message": "Comisión registrada", "key": {"distribuidor_id": distribuidor_id, "periodo": periodo}})
            }

        # ========= GET: Consultar por distribuidor y periodo =========
        elif method == "GET":
            path = event.get("pathParameters") or {}
            distribuidor_id = path.get("distribuidor_id")
            periodo         = path.get("periodo")

            if not distribuidor_id or not periodo:
                return {"statusCode": 400, "body": _dumps({"message": "Faltan distribuidor_id o periodo en la ruta"})}

            resp = table.get_item(Key={"distribuidor_id": distribuidor_id, "periodo": periodo})
            item = resp.get("Item")
            if not item:
                return {"statusCode": 404, "body": _dumps({"message": "Comisión no encontrada"})}

            return {"statusCode": 200, "body": _dumps(item)}

        # ========= PATCH: Actualizar (p.ej. total_ventas/porcentaje) =========
        elif method == "PATCH":
            path = event.get("pathParameters") or {}
            distribuidor_id = path.get("distribuidor_id")
            periodo         = path.get("periodo")

            if not distribuidor_id or not periodo:
                return {"statusCode": 400, "body": _dumps({"message": "Faltan distribuidor_id o periodo en la ruta"})}

            body = json.loads(event["body"], parse_float=Decimal)

            # Campos opcionales a actualizar
            updates = {}
            for k in ("nombre_distribuidor", "total_ventas", "porcentaje", "comision_calculada"):
                if k in body and body[k] is not None:
                    updates[k] = body[k]

            # Si mandan total_ventas o porcentaje, y NO mandan comision_calculada,
            # recalculamos comision_calculada.
            if ("total_ventas" in updates or "porcentaje" in updates) and ("comision_calculada" not in updates):
                # Primero leemos el registro actual para obtener valores actuales
                current = table.get_item(Key={"distribuidor_id": distribuidor_id, "periodo": periodo}).get("Item")
                if not current:
                    return {"statusCode": 404, "body": _dumps({"message": "Comisión no encontrada"})}

                total_ventas = updates.get("total_ventas", current.get("total_ventas", Decimal("0")))
                porcentaje   = updates.get("porcentaje",   current.get("porcentaje",   Decimal("0")))
                updates["comision_calculada"] = (Decimal(total_ventas) * Decimal(porcentaje)).quantize(Decimal("0.01"))

            if not updates:
                return {"statusCode": 400, "body": _dumps({"message": "No hay campos para actualizar"})}

            # Construimos UpdateExpression dinámicamente
            expr_parts = []
            expr_vals  = {}
            for i, (k, v) in enumerate(updates.items(), start=1):
                ph = f":v{i}"
                expr_parts.append(f"{k} = {ph}")
                expr_vals[ph] = v

            update_expr = "SET " + ", ".join(expr_parts)

            table.update_item(
                Key={"distribuidor_id": distribuidor_id, "periodo": periodo},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_vals
            )

            return {
                "statusCode": 200,
                "body": _dumps({"message": "Comisión actualizada", "key": {"distribuidor_id": distribuidor_id, "periodo": periodo}})
            }

        else:
            return {"statusCode": 405, "body": _dumps({"message": "Método no permitido"})}

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": _dumps({"message": "Internal Server Error", "error": str(e)})}
