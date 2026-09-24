from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RuleCreate(BaseModel):
    title: str
    raw_content: str  # the Sigma YAML text
    owner: Optional[str] = None


class RuleVersionOut(BaseModel):
    id: str
    parsed_technique: Optional[str]
    parse_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class RuleOut(BaseModel):
    id: str
    title: str
    format: str
    status: str
    owner: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True