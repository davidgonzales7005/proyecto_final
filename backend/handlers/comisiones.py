import json
import boto3
import os
from decimal import Decimal
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['COMISIONES_TABLE'])

def handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path_params = event.get("pathParameters") or {}
    body = json.loads(event.get("body", "{}"), parse_float=Decimal)

    try:
        # POST → crear comisión
        if method == "POST":
            item = {
                "id": str(uuid.uuid4()),
                "distribuidor_id": body.get("distribuidor_id"),
                "periodo": body.get("periodo"),
                "nombre_distribuidor": body.get("nombre_distribuidor"),
                "total_ventas": body.get("total_ventas"),
                "porcentaje": body.get("porcentaje"),
                "comision_calculada": body.get("comision_calculada")
            }
            table.put_item(Item=item)
            return {"statusCode": 200, "body": json.dumps({"message": "Comisión guardada", "id": item["id"]})}

        # GET → obtener comisión
        elif method == "GET":
            distribuidor_id = path_params.get("distribuidor_id")
            periodo = path_params.get("periodo")
            if not distribuidor_id or not periodo:
                return {"statusCode": 400, "body": json.dumps({"message": "Faltan parámetros"})}

            response = table.get_item(Key={"id": f"{distribuidor_id}-{periodo}"})
            item = response.get("Item")
            if not item:
                return {"statusCode": 404, "body": json.dumps({"message": "No encontrada"})}

            return {"statusCode": 200, "body": json.dumps(item)}

        # PATCH → actualizar comisión
        elif method == "PATCH":
            distribuidor_id = path_params.get("distribuidor_id")
            periodo = path_params.get("periodo")
            if not distribuidor_id or not periodo:
                return {"statusCode": 400, "body": json.dumps({"message": "Faltan parámetros"})}

            response = table.update_item(
                Key={"id": f"{distribuidor_id}-{periodo}"},
                UpdateExpression="set comision_calculada = :c",
                ExpressionAttributeValues={":c": body.get("comision_calculada", Decimal("0"))},
                ReturnValues="UPDATED_NEW"
            )

            return {"statusCode": 200, "body": json.dumps({"message": "Comisión actualizada", "updated": response["Attributes"]})}

        else:
            return {"statusCode": 405, "body": json.dumps({"message": "Método no permitido"})}

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": json.dumps({"message": "Internal Server Error", "error": str(e)})}
