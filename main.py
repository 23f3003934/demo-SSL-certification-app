import time
import uuid
from fastapi import FastAPI, Request, Response, Query

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-zwonsy.example.com"

@app.middleware("http")
async def strict_cors_and_metrics_middleware(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    origin = request.headers.get("origin")

    # 1. Handle CORS Preflight (OPTIONS)
    if request.method == "OPTIONS":
        response = Response()
        if origin == ALLOWED_ORIGIN:
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            # Note: Explicitly rejecting other origins by NOT adding the ACAO header.
    else:
        # 2. Process Actual Request
        response = await call_next(request)
        if origin == ALLOWED_ORIGIN:
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    # 3. Inject Required Middleware Headers on EVERY response (including preflights)
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    return response

@app.get("/stats")
def get_stats(values: str = Query(...)):
    try:
        # Parse comma-separated integers
        parsed_values = [int(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError:
        return Response(content="Invalid input", status_code=400)

    count = len(parsed_values)
    if count == 0:
        return Response(content="No values provided", status_code=400)

    total_sum = sum(parsed_values)
    minimum = min(parsed_values)
    maximum = max(parsed_values)
    mean = total_sum / count

    return {
        "email": "23f3003934@ds.study.iitm.ac.in",  # UPDATE THIS LINE
        "count": count,
        "sum": total_sum,
        "min": minimum,
        "max": maximum,
        "mean": mean
    }