from pydantic import BaseModel
from typing import Dict, Any


class ValidationRequest(BaseModel):
    rule_version_id: str
    synthetic_event: Dict[str, Any]