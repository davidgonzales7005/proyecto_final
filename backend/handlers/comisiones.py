import json, os, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["COMISIONES_TABLE"])

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization"
}
def res(code, body): return {"statusCode": code, "headers": {"Content-Type": "application/json", **CORS}, "body": json.dumps(body)}

def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path = event.get("pathParameters") or {}
    body = json.loads(event.get("body") or "{}")

    if method == "OPTIONS":
        return {"statusCode": 204, "headers": CORS}

    # Crear/actualizar registro de comisión (upsert)
    if method == "POST":
        item = {
            "distribuidor_id": body["distribuidor_id"],
            "periodo": body["periodo"],             # ej. "2025-11"
            "porcentaje": float(body.get("porcentaje", 0.15))
        }
        table.put_item(Item=item)
        return res(201, item)

    # Obtener comisión por distribuidor y periodo
    if method == "GET" and "distribuidor_id" in path and "periodo" in path:
        r = table.get_item(Key={"distribuidor_id": path["distribuidor_id"], "periodo": path["periodo"]})
        if "Item" not in r: return res(404, {"error": "No existe"})
        return res(200, r["Item"])

    # Actualizar porcentaje
    if method == "PATCH" and "distribuidor_id" in path and "periodo" in path:
        nuevo = float(body.get("porcentaje", 0.15))
        r = table.update_item(
            Key={"distribuidor_id": path["distribuidor_id"], "periodo": path["periodo"]},
            UpdateExpression="SET porcentaje = :p",
            ExpressionAttributeValues={":p": nuevo},
            ReturnValues="ALL_NEW"
        )
        return res(200, r["Attributes"])

    return res(400, {"error": "Ruta o método no soportado"})
