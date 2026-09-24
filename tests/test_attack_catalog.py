from app.attack.catalog import get_technique_info, ATTACK_CATALOG


def test_known_technique_returns_info():
    info = get_technique_info("T1059.001")
    assert info is not None
    assert info["tactic"] == "Execution"


def test_unknown_technique_returns_none():
    info = get_technique_info("T9999.999")
    assert info is None


def test_catalog_is_not_empty():
    assert len(ATTACK_CATALOG) > 0