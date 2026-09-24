"""
Wraps pysigma to parse a Sigma rule and extract useful metadata
(technique tag, title, logsource) for DetectLab's canonical model.
"""

import yaml
from sigma.collection import SigmaCollection
from sigma.exceptions import SigmaError


def parse_sigma_rule(raw_yaml: str) -> dict:
    """
    Returns a dict:
    {
        "status": "PARSED" | "FAILED",
        "technique": "T1059.001" | None,
        "error": str | None
    }
    """
    try:
        # First, validate it's parseable YAML at all
        loaded = yaml.safe_load(raw_yaml)

        # Try parsing with pySigma (this validates Sigma-specific structure)
        SigmaCollection.from_yaml(raw_yaml)

        # Extract ATT&CK technique from tags (e.g. "attack.t1059.001")
        technique = None
        tags = loaded.get("tags", []) if isinstance(loaded, dict) else []
        for tag in tags:
            if isinstance(tag, str) and tag.lower().startswith("attack.t"):
                technique = tag.split(".", 1)[1].upper()
                break

        return {"status": "PARSED", "technique": technique, "error": None}

    except SigmaError as e:
        return {"status": "FAILED", "technique": None, "error": str(e)}
    except Exception as e:
        return {"status": "FAILED", "technique": None, "error": f"Invalid YAML: {e}"}