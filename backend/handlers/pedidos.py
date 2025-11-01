import json
import boto3
import os
from decimal import Decimal
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PEDIDOS_TABLE'])

def handler(event, context):
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

        # --- Crear Pedido (POST) ---
        if method == "POST":
            body = json.loads(event['body'], parse_float=Decimal)

            item = {
                'id': str(uuid.uuid4()),
                'cliente': body.get('cliente'),
                'fecha': body.get('fecha', str(datetime.now())),
                'productos': body.get('productos', []),
                'total': body.get('total', Decimal("0")),
                'estado': body.get('estado', 'Creado')
            }

            table.put_item(Item=item)

            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Pedido guardado exitosamente", "id": item['id']})
            }

        # --- Consultar Pedido por ID (GET) ---
        elif method == "GET":
            pedido_id = event["pathParameters"]["id"]

            response = table.get_item(Key={"id": pedido_id})
            item = response.get("Item")

            if item:
                return {
                    "statusCode": 200,
                    "body": json.dumps(item, default=str)
                }
            else:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"message": "Pedido no encontrado"})
                }

        # --- Actualizar estado del pedido (PATCH) ---
        elif method == "PATCH":
            pedido_id = event["pathParameters"]["id"]
            body = json.loads(event['body'])
            nuevo_estado = body.get('estado')

            if not nuevo_estado:
                return {"statusCode": 400, "body": json.dumps({"message": "Debe incluir un estado"})}

            table.update_item(
                Key={'id': pedido_id},
                UpdateExpression='SET estado = :estado',
                ExpressionAttributeValues={':estado': nuevo_estado}
            )

            return {
                "statusCode": 200,
                "body": json.dumps({"message": f"Estado del pedido {pedido_id} actualizado a {nuevo_estado}"})
            }

        else:
            return {"statusCode": 405, "body": json.dumps({"message": "Método no permitido"})}

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }


