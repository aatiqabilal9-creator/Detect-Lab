"""
Safe validation engine.
Simulates whether a rule's logic would match a synthetic (fake) event,
WITHOUT executing any real attack or malicious activity.
"""

import yaml


def run_safe_validation(rule_raw_content: str, synthetic_event: dict) -> dict:
    try:
        parsed = yaml.safe_load(rule_raw_content)
    except Exception:
        return {"verdict": "UNSUPPORTED", "reason": "Could not parse rule content"}

    detection = parsed.get("detection", {})
    selection = detection.get("selection", {})

    if not selection:
        return {"verdict": "INCONCLUSIVE", "reason": "No selection criteria found in rule"}

    matched_fields = []
    unmatched_fields = []   # field WAS present, but value didn't match
    absent_fields = []      # field was NOT present in the synthetic event at all

    for field_expr, expected_value in selection.items():
        field_name = field_expr.split("|")[0]
        operator = field_expr.split("|")[1] if "|" in field_expr else "equals"

        actual_value = synthetic_event.get(field_name)

        if actual_value is None:
            absent_fields.append(field_name)
            continue

        matched = False
        if operator == "endswith" and str(actual_value).endswith(str(expected_value)):
            matched = True
        elif operator == "contains" and str(expected_value) in str(actual_value):
            matched = True
        elif operator == "equals" and str(actual_value) == str(expected_value):
            matched = True

        if matched:
            matched_fields.append(field_name)
        else:
            unmatched_fields.append(field_name)

    total_fields = len(selection)

    # Case 1: none of the required fields were even present -> not enough data to judge
    if len(absent_fields) == total_fields:
        return {
            "verdict": "INCONCLUSIVE",
            "reason": "Synthetic event did not contain any relevant fields to test against",
            "absent_fields": absent_fields,
        }

    # Case 2: all fields present and all matched -> PASS
    if not unmatched_fields and not absent_fields:
        return {
            "verdict": "PASS",
            "reason": "All expected fields matched the synthetic event",
            "matched_fields": matched_fields,
        }

    # Case 3: at least one field was present but the condition failed -> FAIL
    return {
        "verdict": "FAIL",
        "reason": "One or more fields did not satisfy the rule's detection logic",
        "matched_fields": matched_fields,
        "unmatched_fields": unmatched_fields,
        "absent_fields": absent_fields,
    }