import json, os, boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["COMISIONES_TABLE"])

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization"
}
def res(code, body):
    return {"statusCode": code, "headers": {"Content-Type":"application/json", **CORS}, "body": json.dumps(body)}

def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path = event.get("pathParameters") or {}
    body = json.loads(event.get("body") or "{}")

    if method == "OPTIONS":
        return {"statusCode": 204, "headers": CORS}

    if method == "POST":
        item = {
            "distribuidor_id": body["distribuidor_id"],
            "periodo": body["periodo"],  # ej "2025-11"
            "nombre_distribuidor": body.get("nombre_distribuidor", ""),
            "total_ventas": float(body.get("total_ventas", 0)),
            "porcentaje": float(body.get("porcentaje", 0.15)),
            "comision_calculada": float(body.get("comision_calculada", 0))
        }
        table.put_item(Item=item)
        return res(201, item)

    if method == "GET" and "distribuidor_id" in path and "periodo" in path:
        r = table.get_item(Key={"distribuidor_id": path["distribuidor_id"], "periodo": path["periodo"]})
        if "Item" not in r:
            return res(404, {"error": "Comisión no existe"})
        return res(200, r["Item"])

    if method == "PATCH" and "distribuidor_id" in path and "periodo" in path:
        exp, names, vals = [], {}, {}
        if "porcentaje" in body:
            exp.append("#p = :p"); names["#p"] = "porcentaje"; vals[":p"] = float(body["porcentaje"])
        if "total_ventas" in body:
            exp.append("#t = :t"); names["#t"] = "total_ventas"; vals[":t"] = float(body["total_ventas"])
        if "comision_calculada" in body:
            exp.append("#c = :c"); names["#c"] = "comision_calculada"; vals[":c"] = float(body["comision_calculada"])
        if not exp:
            return res(400, {"error": "Nada para actualizar"})
        r = table.update_item(
            Key={"distribuidor_id": path["distribuidor_id"], "periodo": path["periodo"]},
            UpdateExpression="SET " + ", ".join(exp),
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=vals,
            ReturnValues="ALL_NEW"
        )
        return res(200, r["Attributes"])

    return res(400, {"error": "Ruta o método no soportado"})
