import json, datetime, boto3

dynamo = boto3.resource('dynamodb')

comisiones = dynamo.Table('ComisionesTable')


def handler(event, context):
    http = event.get('requestContext', {}).get('http', {})
    method = http.get('method', 'GET')
    path = http.get('path', '/')
    params = event.get('pathParameters') or {}


    try:
        if method == 'POST' and path.endswith('/api/comisiones'):
            body = json.loads(event.get('body') or '{}')
            distribuidor_id = str(body['distribuidor_id'])
            periodo = str(body['periodo'])          # YYYY-MM
            ventas_total = float(body['ventas_total'])
            tasa = float(body['tasa'])              # 0..1
            monto = round(ventas_total * tasa, 2)

            item = {
                'id': f'{distribuidor_id}#{periodo}',
                'distribuidor_id': distribuidor_id,
                'periodo': periodo,
                'ventas_total': ventas_total,
                'tasa': tasa,
                'monto': monto,
                'fecha_calculo': datetime.datetime.utcnow().isoformat()+'Z'
            }
            comisiones.put_item(Item=item)
            return ok(item)


        if method == 'GET' and 'distribuidor_id' in params and 'periodo' in params:
            key = {'id': f"{params['distribuidor_id']}#{params['periodo']}"}
            res = comisiones.get_item(Key=key)
            if 'Item' not in res:
                return not_found()
            return ok(res['Item'])


        if method == 'PATCH' and 'distribuidor_id' in params and 'periodo' in params:
            body = json.loads(event.get('body') or '{}')
            res = comisiones.update_item(
                Key={'id': f"{params['distribuidor_id']}#{params['periodo']}"},
                UpdateExpression='SET ventas_total=:v, tasa=:t, monto=:m',
                ExpressionAttributeValues={
                    ':v': float(body['ventas_total']),
                    ':t': float(body['tasa']),
                    ':m': float(body['monto'])
                },
                ReturnValues='ALL_NEW'
            )
            return ok(res['Attributes'])


        return bad('Ruta no soportada')
    except Exception as e:
        return err(e)


def ok(x):        return {'statusCode':200,'headers':h(),'body':json.dumps(x)}
def not_found():  return {'statusCode':404,'headers':h(),'body':json.dumps({'error':'not found'})}
def bad(m):       return {'statusCode':400,'headers':h(),'body':json.dumps({'error':m})}
def err(e):       return {'statusCode':500,'headers':h(),'body':json.dumps({'error':str(e)})}
def h():          return {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
