"""
Minimal local ATT&CK catalog (subset) for DetectLab MVP.
"""

ATTACK_CATALOG_VERSION = "vCurrent-mvp"

ATTACK_CATALOG = {
    "T1059.001": {
        "tactic": "Execution",
        "name": "Command and Scripting Interpreter: PowerShell",
        "required_telemetry": ["windows.powershell", "windows.process_creation"],
    },
    "T1059.003": {
        "tactic": "Execution",
        "name": "Command and Scripting Interpreter: Windows Command Shell",
        "required_telemetry": ["windows.process_creation"],
    },
    "T1078": {
        "tactic": "Defense Evasion / Persistence",
        "name": "Valid Accounts",
        "required_telemetry": ["windows.authentication"],
    },
    "T1021": {
        "tactic": "Lateral Movement",
        "name": "Remote Services",
        "required_telemetry": ["windows.network", "windows.rdp"],
    },
    "T1021.001": {
        "tactic": "Lateral Movement",
        "name": "Remote Desktop Protocol",
        "required_telemetry": ["windows.rdp"],
    },
    "T1041": {
        "tactic": "Exfiltration",
        "name": "Exfiltration Over C2 Channel",
        "required_telemetry": ["network.netflow"],
    },
    "T1562": {
        "tactic": "Defense Evasion",
        "name": "Impair Defenses",
        "required_telemetry": ["windows.security_log", "windows.process_creation"],
    },
    "T1562.001": {
        "tactic": "Defense Evasion",
        "name": "Disable or Modify Tools",
        "required_telemetry": ["windows.security_log"],
    },
    "T1003": {
        "tactic": "Credential Access",
        "name": "OS Credential Dumping",
        "required_telemetry": ["windows.process_creation", "windows.security_log"],
    },
    "T1047": {
        "tactic": "Execution",
        "name": "Windows Management Instrumentation",
        "required_telemetry": ["windows.wmi"],
    },
    "T1105": {
        "tactic": "Command and Control",
        "name": "Ingress Tool Transfer",
        "required_telemetry": ["network.netflow", "windows.process_creation"],
    },
    "T1190": {
        "tactic": "Initial Access",
        "name": "Exploit Public-Facing Application",
        "required_telemetry": ["web.access_log", "network.netflow"],
    },
}


def get_technique_info(technique_id: str) -> dict | None:
    return ATTACK_CATALOG.get(technique_id)