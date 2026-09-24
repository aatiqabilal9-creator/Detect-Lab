from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.domain.models import TelemetrySource

router = APIRouter(prefix="/telemetry-sources", tags=["telemetry"])


class TelemetrySourceCreate(BaseModel):
    name: str
    is_healthy: int = 1


@router.post("")
def create_telemetry_source(payload: TelemetrySourceCreate, db: Session = Depends(get_db)):
    source = TelemetrySource(name=payload.name, is_healthy=payload.is_healthy)
    db.add(source)
    db.commit()
    db.refresh(source)
    return {"id": source.id, "name": source.name, "is_healthy": source.is_healthy}


@router.get("")
def list_telemetry_sources(db: Session = Depends(get_db)):
    return db.query(TelemetrySource).all()