import json
from unittest.mock import patch

from src.application.dtos.message_dto import ProcessMessageOutput
from src.presentation.handlers.lambda_handler import lambda_handler


@patch("src.presentation.handlers.lambda_handler.process_message_uc")
def test_lambda_handler_success_dialogflow(mock_use_case):
    # Arrange
    mock_output = ProcessMessageOutput(
        response_text="Resposta processada", risk_detected=False
    )
    mock_use_case.execute.return_value = mock_output

    event = {
        "body": json.dumps(
            {
                "queryResult": {"queryText": "Olá"},
                "session": "projects/foo/agent/sessions/123",
            }
        )
    }

    # Act
    response = lambda_handler(event, None)

    # Assert
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["fulfillmentText"] == "Resposta processada"
    mock_use_case.execute.assert_called_once()


@patch("src.presentation.handlers.lambda_handler.process_message_uc")
def test_lambda_handler_success_api(mock_use_case):
    # Arrange
    mock_output = ProcessMessageOutput(
        response_text="Resposta API", risk_detected=False
    )
    mock_use_case.execute.return_value = mock_output

    event = {"body": json.dumps({"message": "Olá via API", "session": "123"})}

    # Act
    response = lambda_handler(event, None)

    # Assert
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["response"] == "Resposta API"
    assert body["risk_detected"] is False


def test_lambda_handler_empty_message():
    # Arrange
    event = {"body": json.dumps({})}

    # Act
    response = lambda_handler(event, None)

    # Assert
    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "error" in body
