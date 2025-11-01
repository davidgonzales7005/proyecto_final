import json, uuid, datetime, boto3

dynamo = boto3.resource('dynamodb')

pedidos = dynamo.Table('PedidosTable')


def handler(event, context):
    http = event.get('requestContext', {}).get('http', {})
    method = http.get('method', 'GET')
    path = http.get('path', '/')
    params = event.get('pathParameters') or {}

    try:
        if method == 'POST' and path.endswith('/api/pedidos'):
            body = json.loads(event.get('body') or '{}')
            item = {
                'id': str(uuid.uuid4()),
                'cliente_id': str(body.get('cliente_id', 'anon')),
                'total': float(body.get('total', 0)),
                'estado': 'pendiente',
                'fecha': datetime.datetime.utcnow().isoformat() + 'Z'
            }
            pedidos.put_item(Item=item)
            return ok(item)


        if method == 'GET' and 'id' in params:
            res = pedidos.get_item(Key={'id': params['id']})
            if 'Item' not in res:
                return not_found()
            return ok(res['Item'])


        if method == 'PATCH' and path.endswith('/estado') and 'id' in params:
            body = json.loads(event.get('body') or '{}')
            nuevo_estado = body.get('estado', 'pendiente')
            pedidos.update_item(
                Key={'id': params['id']},
                UpdateExpression='SET #e = :e',
                ExpressionAttributeNames={'#e': 'estado'},
                ExpressionAttributeValues={':e': nuevo_estado}
            )
            return ok({'id': params['id'], 'estado': nuevo_estado})


        return bad('Ruta no soportada')
    except Exception as e:
        return err(e)


def ok(x):        return {'statusCode': 200, 'headers': h(), 'body': json.dumps(x)}
def not_found():  return {'statusCode': 404, 'headers': h(), 'body': json.dumps({'error': 'not found'})}
def bad(m):       return {'statusCode': 400, 'headers': h(), 'body': json.dumps({'error': m})}
def err(e):       return {'statusCode': 500, 'headers': h(), 'body': json.dumps({'error': str(e)})}
def h():          return {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
