import json, uuid, datetime


def handler(event, context):
    http = event.get('requestContext', {}).get('http', {})
    method = http.get('method', 'GET')
    path = http.get('path', '/')


    try:
        if method == 'POST' and path.endswith('/api/pagos'):
            body = json.loads(event.get('body') or '{}')
            item = {
                'id_pago': str(uuid.uuid4()),
                'pedido_id': str(body.get('pedido_id', '')),
                'monto': float(body.get('monto', 0)),
                'fecha_pago': datetime.datetime.utcnow().isoformat() + 'Z',
                'estado': 'CONFIRMADO'
            }
            return ok(item)


        return bad('Ruta no soportada')
    except Exception as e:
        return err(e)


def ok(x):  return {'statusCode': 200, 'headers': h(), 'body': json.dumps(x)}
def bad(m): return {'statusCode': 400, 'headers': h(), 'body': json.dumps({'error': m})}
def err(e): return {'statusCode': 500, 'headers': h(), 'body': json.dumps({'error': str(e)})}
def h():    return {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
