from time import sleep
import sentry_sdk

import uvicorn
import requests
from fastapi import FastAPI
from os import environ, truncate

from starlette_exporter import PrometheusMiddleware, handle_metrics
from prometheus_client.core import REGISTRY

from backend_service.api.router.roll_router import roll_router
from backend_service.api.router.stats_router import stats_router
from backend_service.api.router.healthcheck_router import healthcheck_router
from backend_service.api.router.help_router import help_router
from backend_service.api.router.sentry_router import sentry_router

from backend_service.collectors.collectors import StatsMetricsCollector

# Register any custom collectors here
REGISTRY.register(StatsMetricsCollector())

def create_app():
    app = FastAPI()
    app.include_router(roll_router)
    app.include_router(stats_router)
    app.include_router(help_router)
    app.include_router(help_router)
    app.include_router(healthcheck_router)
    app.include_router(sentry_router)

    # Remove sentry for now, Feyre generates too many exceptions!
    
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

def check_sync_state():
    """
    Checks to make sure sync service is up and running, and that it synced as part of start up.
    """
    print("[#] Checking sync service to make sure it is ready...", flush = True)

    if (environ.get('ENV', None) == "development"):
        print("[#] This is a dev environment. Skipping!", flush = True)
        return

    has_synced = False
    i = 0
    while (not has_synced):
        try:
            user_sync = requests.get('http://datasync:5001/api/syncservice/users/sync').json()
            stats_sync = requests.get('http://datasync:5001/api/syncservice/stats/sync').json()

            if (bool(user_sync["completed_successfully"]) and bool(stats_sync["completed_successfully"])):
                has_synced = True
                print("[#] Sync complete!", flush = True)
            else:
                print(f"[#] Sync service has not finished syncing yet... This is iteration {i}", flush = True)
                sleep(10)

        except ConnectionRefusedError:
            print("[#] Sync service is not serving requests yet!", flush = True)
        i+=1
        
def main():
    check_sync_state()
    app = create_app()
    print("[#] Starting app...", flush = True)
    uvicorn.run(app, host="0.0.0.0", port=5000)