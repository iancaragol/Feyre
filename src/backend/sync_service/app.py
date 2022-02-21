import atexit
import uvicorn

from os import environ
from fastapi import FastAPI

from apscheduler.schedulers.background import BackgroundScheduler
from prometheus_client.core import REGISTRY
from starlette_exporter import PrometheusMiddleware, handle_metrics
from sync_service.api.routers.sync_stats import stats_router, sync_stats
from sync_service.api.routers.sync_user import users_router, sync_users
from sync_service.collectors.collectors import TimeSinceSyncMetricsCollector, CompletedSuccesfullyMetricsCollector

sync_interval_seconds = 7200 # 2 Hours

REGISTRY.register(TimeSinceSyncMetricsCollector())
REGISTRY.register(CompletedSuccesfullyMetricsCollector())

if (not environ.get('DB_BYPASS', None)):
    scheduler = BackgroundScheduler()

    # Add all sync jobs here!
    scheduler.add_job(func=sync_stats, trigger="interval", seconds=sync_interval_seconds)
    scheduler.add_job(func=sync_users, trigger="interval", seconds=sync_interval_seconds)

    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())



def create_app():
    app = FastAPI()
    app.include_router(stats_router)
    app.include_router(users_router)

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

    print("[#] Created new app", flush = True)
    return app
    
def sync_on_start():
    """
    Sync on start up, this way if a new Redis instance has been created it will be synced right away
    """
    if (environ.get('ENV', None) != "development"):
        print("[#] Not dev environment. Syncing!", flush = True)
        sync_stats()
        sync_users()
    else:
        print("[#] Dev environment. Skipping sync...", flush = True)

def main():
    app = create_app()

    print("[#] Checking Redis status...", flush = True)
    sync_on_start()

    print("[#] Starting app...", flush = True)
    uvicorn.run(app, host="0.0.0.0", port=5001)