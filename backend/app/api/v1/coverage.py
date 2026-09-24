from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.scoring.coverage import calculate_coverage

router = APIRouter(prefix="/coverage", tags=["coverage"])


@router.get("")
def get_coverage(db: Session = Depends(get_db)):
    return calculate_coverage(db)