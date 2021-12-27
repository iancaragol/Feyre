from os import environ, truncate
import sentry_sdk

import uvicorn
from fastapi import FastAPI

from flask import Flask
from starlette_exporter import PrometheusMiddleware, handle_metrics
from sentry_sdk.integrations.flask import FlaskIntegration
from backend_service.api.router.roll_router import roll_router
from backend_service.api.router.stats_router import stats_router
from backend_service.api.router.healthcheck_router import healthcheck_router
from backend_service.api.router.help_router import help_router
from backend_service.api.router.sentry_router import sentry_router

# metrics = PrometheusMetrics.for_app_factory()

def create_app():
    app = FastAPI()
    app.include_router(roll_router)
    app.include_router(stats_router)
    app.include_router(help_router)
    app.include_router(help_router)
    app.include_router(healthcheck_router)
    app.include_router(sentry_router)

    # dsn = environ.get("SENTRY_DSN")
    # sentry_sdk.init(
    #     dsn=dsn,
    #     integrations=[FlaskIntegration()],

    #     # Set traces_sample_rate to 1.0 to capture 100%
    #     # of transactions for performance monitoring.
    #     # We recommend adjusting this value in production.
    #     traces_sample_rate=1.0
    # )

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

    print("[#] Created new app", flush = True)
    return app

def main():
    app = create_app()
    print("[#] Starting app...", flush = True)
    uvicorn.run(app, host="0.0.0.0", port=5000)