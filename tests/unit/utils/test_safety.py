from src.utils.safety_filters import EMERGENCY_MESSAGE, check_safety


def test_safety_clean_text():
    """Testa texto seguro."""
    safe, msg = check_safety("O que é TDAH?")
    assert safe is True
    assert msg is None


def test_safety_risk_text():
    """Testa detecção de risco."""
    risk_inputs = [
        "eu quero morrer",
        "pensando em suicidio",
        "vou me matar",
        "automutilação",
    ]
    for text in risk_inputs:
        safe, msg = check_safety(text)
        assert safe is False
        assert msg == EMERGENCY_MESSAGE


def test_safety_empty_text():
    """Testa entrada vazia."""
    safe, msg = check_safety("")
    assert safe is True
    assert msg is None
