from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.models import RuleVersion, ValidationRun
from app.schemas.validation import ValidationRequest
from app.validation.engine import run_safe_validation

router = APIRouter(prefix="/validation-runs", tags=["validation"])


@router.post("")
def create_validation_run(payload: ValidationRequest, db: Session = Depends(get_db)):
    version = db.query(RuleVersion).filter(RuleVersion.id == payload.rule_version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Rule version not found")

    result = run_safe_validation(version.raw_content, payload.synthetic_event)

    run = ValidationRun(
        rule_version_id=version.id,
        verdict=result["verdict"],
        notes=result.get("reason", ""),
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    return {
        "validation_run_id": run.id,
        "verdict": run.verdict,
        "details": result,
    }


@router.get("/{rule_version_id}")
def get_validation_history(rule_version_id: str, db: Session = Depends(get_db)):
    runs = db.query(ValidationRun).filter(ValidationRun.rule_version_id == rule_version_id).all()
    return runs