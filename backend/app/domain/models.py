import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class DetectionRule(Base):
    __tablename__ = "detection_rules"

    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    format = Column(String, nullable=False, default="sigma")
    status = Column(String, nullable=False, default="DRAFT")  # DRAFT, REVIEWED, RELEASED
    owner = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    versions = relationship("RuleVersion", back_populates="rule")


class RuleVersion(Base):
    __tablename__ = "rule_versions"

    id = Column(String, primary_key=True, default=gen_uuid)
    rule_id = Column(String, ForeignKey("detection_rules.id"), nullable=False)
    raw_content = Column(Text, nullable=False)          # original Sigma YAML text
    parsed_technique = Column(String, nullable=True)     # e.g. T1059.001
    parse_status = Column(String, default="PENDING")     # PENDING, PARSED, FAILED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    rule = relationship("DetectionRule", back_populates="versions")


class TelemetrySource(Base):
    __tablename__ = "telemetry_sources"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)           # e.g. "windows.powershell"
    is_healthy = Column(Integer, default=1)          # 1 = healthy, 0 = stale/missing
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ValidationRun(Base):
    __tablename__ = "validation_runs"

    id = Column(String, primary_key=True, default=gen_uuid)
    rule_version_id = Column(String, ForeignKey("rule_versions.id"), nullable=False)
    verdict = Column(String, default="PENDING")   # PASS, FAIL, INCONCLUSIVE, UNSUPPORTED
    notes = Column(Text, nullable=True)
    ran_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))