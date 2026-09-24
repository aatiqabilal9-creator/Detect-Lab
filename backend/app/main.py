from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.domain import models  # noqa: F401 (import so tables are registered)
from app.api.v1.rules import router as rules_router
from app.api.v1.coverage import router as coverage_router
from app.api.v1.telemetry import router as telemetry_router
from app.api.v1.validation import router as validation_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DetectLab API",
    version=settings.app_version,
    root_path="/api/v1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(rules_router)
app.include_router(coverage_router)
app.include_router(telemetry_router)
app.include_router(validation_router)


@app.get("/health/live")
def health_live():
    return {"status": "alive", "app_env": settings.app_env}


@app.get("/health/ready")
def health_ready():
    return {"status": "ready"}


@app.get("/")
def root():
    return {"message": "DetectLab API is running", "version": settings.app_version}