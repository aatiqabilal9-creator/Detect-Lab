"""
Tests for the Sigma rule parser.
These confirm the parser correctly identifies valid rules, extracts the
ATT&CK technique, and safely rejects malformed rules.
"""

from app.parsers.sigma_parser import parse_sigma_rule


VALID_RULE = """
title: Suspicious PowerShell Download
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\\powershell.exe'
        CommandLine|contains: 'DownloadString'
    condition: selection
tags:
    - attack.t1059.001
level: high
"""

MALFORMED_RULE = """
this is not: valid: yaml: at: all: [broken
"""

RULE_WITHOUT_TAGS = """
title: No Technique Tag
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\\cmd.exe'
    condition: selection
level: medium
"""


def test_valid_rule_parses_successfully():
    result = parse_sigma_rule(VALID_RULE)
    assert result["status"] == "PARSED"


def test_valid_rule_extracts_correct_technique():
    result = parse_sigma_rule(VALID_RULE)
    assert result["technique"] == "T1059.001"


def test_malformed_rule_fails_safely():
    result = parse_sigma_rule(MALFORMED_RULE)
    assert result["status"] == "FAILED"
    assert result["error"] is not None


def test_rule_without_attack_tag_has_no_technique():
    result = parse_sigma_rule(RULE_WITHOUT_TAGS)
    assert result["status"] == "PARSED"
    assert result["technique"] is None