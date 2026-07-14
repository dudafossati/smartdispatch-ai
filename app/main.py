from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.jobs import router as jobs_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(jobs_router, prefix="/api/v1", tags=["jobs"])


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.environment}
