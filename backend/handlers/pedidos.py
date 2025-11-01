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
        body = json.loads(event['body'], parse_float=Decimal)  # <— ESTA LÍNEA es clave

        item = {
            'id': str(uuid.uuid4()),
            'cliente': body.get('cliente'),
            'fecha': body.get('fecha', str(datetime.now())),
            'productos': body.get('productos'),
            'total': body.get('total'),
            'estado': body.get('estado', 'Creado')
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Pedido guardado exitosamente", "id": item['id']})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }
