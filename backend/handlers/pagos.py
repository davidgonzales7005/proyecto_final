import json
import boto3
import os
from decimal import Decimal
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PEDIDOS_TABLE'])

def handler(event, context):
    try:
        body = json.loads(event['body'], parse_float=Decimal)
        pedido_id = body.get('pedido_id')

        if not pedido_id:
            return {"statusCode": 400, "body": json.dumps({"message": "Falta el campo pedido_id"})}

        # Actualiza el estado del pedido
        response = table.update_item(
            Key={'id': pedido_id},
            UpdateExpression="set estado = :estado_pago, pago_fecha = :fecha",
            ExpressionAttributeValues={
                ':estado_pago': 'Pagado',
                ':fecha': str(datetime.now())
            },
            ReturnValues="UPDATED_NEW"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Pago registrado correctamente",
                "pedido_id": pedido_id,
                "updated": response.get("Attributes", {})
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": json.dumps({"message": "Internal Server Error", "error": str(e)})}
