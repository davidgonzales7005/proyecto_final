import json, os, uuid, boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["PEDIDOS_TABLE"])

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization"
}
def res(code, body):
    return {"statusCode": code, "headers": {"Content-Type": "application/json", **CORS}, "body": json.dumps(body)}

def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path_params = event.get("pathParameters") or {}
    body = json.loads(event.get("body") or "{}")

    if method == "OPTIONS":
        return {"statusCode": 204, "headers": CORS}

    if method == "POST":
        item = {
            "id": body.get("id") or str(uuid.uuid4()),
            "cliente": body.get("cliente", "Alicorp"),
            "fecha": body.get("fecha", ""),
            "productos": body.get("productos", []),
            "total": float(body.get("total", 0)),
            "estado": body.get("estado", "Creado")
        }
        table.put_item(Item=item)
        return res(201, item)

    if method == "GET" and "id" in path_params:
        r = table.get_item(Key={"id": path_params["id"]})
        if "Item" not in r:
            return res(404, {"error": "Pedido no existe"})
        return res(200, r["Item"])

    if method == "PATCH" and "id" in path_params:
        nuevo_estado = body.get("estado", "Creado")
        r = table.update_item(
            Key={"id": path_params["id"]},
            UpdateExpression="SET #e = :e",
            ExpressionAttributeNames={"#e": "estado"},
            ExpressionAttributeValues={":e": nuevo_estado},
            ReturnValues="ALL_NEW"
        )
        return res(200, r["Attributes"])

    return res(400, {"error": "Ruta o método no soportado"})
