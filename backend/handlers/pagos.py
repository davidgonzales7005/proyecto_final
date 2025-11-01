import json

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization"
}
def res(c,b): 
    return {"statusCode": c, "headers": {"Content-Type":"application/json", **CORS}, "body": json.dumps(b)}

def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    if method == "OPTIONS":
        return {"statusCode": 204, "headers": CORS}
    data = json.loads(event.get("body") or "{}")
    # placeholder: aquí registrarías el pago (otra tabla / integración)
    return res(201, {"status": "ok", "pago": data})
