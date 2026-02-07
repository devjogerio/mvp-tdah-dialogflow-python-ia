import pytest
import json
from unittest.mock import patch, MagicMock
from src.lambda_function import lambda_handler

@patch("src.lambda_function.assistant_service")
def test_lambda_handler_success(mock_assistant):
    """Testa fluxo normal do Lambda."""
    # Mock do comportamento do AssistantService
    mock_assistant.retrieve_context.return_value = "Contexto"
    mock_assistant.invoke_model.return_value = "Resposta do Modelo"

    event = {"body": json.dumps({"message": "Olá"})}
    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["response"] == "Resposta do Modelo"
    assert body["risk_detected"] is False

@patch("src.lambda_function.check_safety")
def test_lambda_handler_risk(mock_check_safety):
    """Testa fluxo de risco detectado."""
    mock_check_safety.return_value = (False, "Mensagem de Emergência")

    event = {"body": json.dumps({"message": "Quero morrer"})}
    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["response"] == "Mensagem de Emergência"
    assert body["risk_detected"] is True
