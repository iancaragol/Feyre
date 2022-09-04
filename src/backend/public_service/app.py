import uvicorn

from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics
from public_service.api.router.public_stats_router import public_stats_router
from common.logger import logger_setup, LoggerNames

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

def create_app():
    app = FastAPI()

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

    limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    app.include_router(public_stats_router)

    print("[#] Created new app", flush = True)
    return app
        
def main():
    logger_setup(LoggerNames.public_logger, "public_service.log")
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=5002)