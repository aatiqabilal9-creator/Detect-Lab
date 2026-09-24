"""
Calculates mapped vs telemetry-ready coverage, and identifies coverage gaps.
"""

from sqlalchemy.orm import Session

from app.domain.models import RuleVersion, TelemetrySource
from app.attack.catalog import ATTACK_CATALOG, get_technique_info


def calculate_coverage(db: Session) -> dict:
    parsed_versions = (
        db.query(RuleVersion)
        .filter(RuleVersion.parse_status == "PARSED")
        .filter(RuleVersion.parsed_technique.isnot(None))
        .all()
    )

    mapped_techniques = {v.parsed_technique for v in parsed_versions}

    healthy_sources = {
        s.name for s in db.query(TelemetrySource).filter(TelemetrySource.is_healthy == 1).all()
    }

    total_known_techniques = len(ATTACK_CATALOG)
    mapped_count = len(mapped_techniques)

    telemetry_ready_count = 0
    technique_details = []
    gaps = []

    for tech_id in mapped_techniques:
        info = get_technique_info(tech_id)
        if not info:
            continue

        required = set(info["required_telemetry"])
        missing_telemetry = required - healthy_sources
        is_telemetry_ready = len(missing_telemetry) == 0

        if is_telemetry_ready:
            telemetry_ready_count += 1
        else:
            # This technique is mapped but NOT telemetry-ready -> it's a gap
            gaps.append({
                "technique_id": tech_id,
                "name": info["name"],
                "tactic": info["tactic"],
                "missing_telemetry": sorted(missing_telemetry),
                "priority": "HIGH" if info["tactic"] in ["Execution", "Lateral Movement", "Credential Access"] else "MEDIUM",
                "recommendation": f"Connect the following telemetry source(s) to close this gap: {', '.join(sorted(missing_telemetry))}",
            })

        technique_details.append({
            "technique_id": tech_id,
            "name": info["name"],
            "tactic": info["tactic"],
            "required_telemetry": info["required_telemetry"],
            "telemetry_ready": is_telemetry_ready,
        })

    # Also flag techniques that aren't mapped at all yet (not in any uploaded rule)
    unmapped_techniques = set(ATTACK_CATALOG.keys()) - mapped_techniques
    for tech_id in unmapped_techniques:
        info = get_technique_info(tech_id)
        gaps.append({
            "technique_id": tech_id,
            "name": info["name"],
            "tactic": info["tactic"],
            "missing_telemetry": [],
            "priority": "LOW",
            "recommendation": "No detection rule exists yet for this technique. Author a Sigma rule to close this gap.",
        })

    mapped_coverage_pct = round((mapped_count / total_known_techniques) * 100, 1) if total_known_techniques else 0.0
    telemetry_ready_pct = round((telemetry_ready_count / total_known_techniques) * 100, 1) if total_known_techniques else 0.0

    # Sort gaps: HIGH priority first
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    gaps.sort(key=lambda g: priority_order.get(g["priority"], 3))

    return {
        "total_known_techniques": total_known_techniques,
        "mapped_coverage_percent": mapped_coverage_pct,
        "telemetry_ready_coverage_percent": telemetry_ready_pct,
        "techniques": technique_details,
        "gaps": gaps,
        "gap_count": len(gaps),
    }