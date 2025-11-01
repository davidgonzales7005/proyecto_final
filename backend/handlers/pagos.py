import json
CORS = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST,OPTIONS", "Access-Control-Allow-Headers": "Content-Type,Authorization"}
def res(c,b): return {"statusCode": c, "headers": {"Content-Type":"application/json", **CORS}, "body": json.dumps(b)}
def handler(event, context):
    m = event.get("requestContext", {}).get("http", {}).get("method", "")
    if m == "OPTIONS": return {"statusCode":204, "headers": CORS}
    data = json.loads(event.get("body") or "{}")
    # Aquí podrías validar y registrar el pago en otra tabla si lo decides.
    return res(201, {"status":"ok", "pago": data})

