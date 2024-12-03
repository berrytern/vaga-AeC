from prometheus_client import (
    generate_latest,
    Counter,
    CollectorRegistry,
    multiprocess,
    CONTENT_TYPE_LATEST,
)
from fastapi import Response, Request, FastAPI


REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["path", "method", "status"]
)


# track status codes of requests and it can be used to monitor the health of the application
async def track_requests(request: Request, call_next):
    response = await call_next(request)

    if request.url.path != "/metrics":
        REQUEST_COUNT.labels(
            path=request.url.path, method=request.method, status=response.status_code
        ).inc()

    return response


def register_track_middleware(app: FastAPI):
    app.middleware("http")(track_requests)

    @app.get("/metrics")
    def metrics():
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)
        return Response(data, media_type=CONTENT_TYPE_LATEST)
