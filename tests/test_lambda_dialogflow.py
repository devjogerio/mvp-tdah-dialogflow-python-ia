import json
import pytest
from unittest.mock import MagicMock, patch
from src.lambda_function import lambda_handler

@pytest.fixture
def dialogflow_event():
    return {
        "body": json.dumps({
            "responseId": "response-id",
            "session": "projects/project-id/agent/sessions/session-id",
            "queryResult": {
                "queryText": "O que é TDAH?",
                "parameters": {
                    "param1": "value1"
                },
                "allRequiredParamsPresent": True,
                "fulfillmentText": "",
                "fulfillmentMessages": [],
                "outputContexts": [],
                "intent": {
                    "name": "projects/project-id/agent/intents/intent-id",
                    "displayName": "TDAH Help"
                },
                "intentDetectionConfidence": 1.0,
                "languageCode": "pt-br"
            },
            "originalDetectIntentRequest": {
                "source": "google",
                "version": "2.0",
                "payload": {}
            }
        })
    }

@pytest.fixture
def api_gateway_event():
    return {
        "body": json.dumps({
            "message": "O que é TDAH?"
        })
    }

@patch("src.lambda_function.assistant_service")
def test_lambda_handler_dialogflow(mock_assistant, dialogflow_event):
    """Testa se a Lambda responde corretamente ao formato Dialogflow"""
    mock_assistant.retrieve_context.return_value = "Contexto sobre TDAH"
    mock_assistant.invoke_model.return_value = "TDAH é um transtorno..."
    
    response = lambda_handler(dialogflow_event, {})
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    
    # Verifica formato Dialogflow
    assert "fulfillmentText" in body
    assert body["fulfillmentText"] == "TDAH é um transtorno..."
    assert "fulfillmentMessages" in body

@patch("src.lambda_function.assistant_service")
def test_lambda_handler_api_gateway(mock_assistant, api_gateway_event):
    """Testa se a Lambda mantém compatibilidade com API Gateway simples"""
    mock_assistant.retrieve_context.return_value = "Contexto sobre TDAH"
    mock_assistant.invoke_model.return_value = "TDAH é um transtorno..."
    
    response = lambda_handler(api_gateway_event, {})
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    
    # Verifica formato API simples
    assert "response" in body
    assert body["response"] == "TDAH é um transtorno..."
    assert body["risk_detected"] is False
