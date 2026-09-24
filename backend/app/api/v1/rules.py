from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.domain.models import DetectionRule, RuleVersion
from app.schemas.rule import RuleCreate, RuleOut, RuleVersionOut
from app.parsers.sigma_parser import parse_sigma_rule

router = APIRouter(prefix="/rules", tags=["rules"])


@router.post("", response_model=RuleOut)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)):
    # 1. Create the parent rule
    rule = DetectionRule(title=payload.title, owner=payload.owner, format="sigma")
    db.add(rule)
    db.commit()
    db.refresh(rule)

    # 2. Parse the Sigma content
    result = parse_sigma_rule(payload.raw_content)

    # 3. Store the immutable version with parse result
    version = RuleVersion(
        rule_id=rule.id,
        raw_content=payload.raw_content,
        parsed_technique=result["technique"],
        parse_status=result["status"],
    )
    db.add(version)
    db.commit()

    return rule


@router.get("", response_model=List[RuleOut])
def list_rules(db: Session = Depends(get_db)):
    return db.query(DetectionRule).all()


@router.get("/{rule_id}/versions", response_model=List[RuleVersionOut])
def get_rule_versions(rule_id: str, db: Session = Depends(get_db)):
    versions = db.query(RuleVersion).filter(RuleVersion.rule_id == rule_id).all()
    if not versions:
        raise HTTPException(status_code=404, detail="No versions found for this rule")
    return versions