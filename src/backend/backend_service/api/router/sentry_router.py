from fastapi import APIRouter

sentry_router = APIRouter()

@sentry_router.get('/api/backendservice/sentry/debug')
async def trigger_error():
    division_by_zero = 1 / 0