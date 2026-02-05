import pytest
from unittest.mock import MagicMock, patch
from src.core.bedrock_integration import BedrockService

@pytest.fixture
def mock_boto3():
    with patch("boto3.client") as mock:
        yield mock

def test_bedrock_init(mock_boto3):
    """Testa inicialização do serviço."""
    service = BedrockService()
    assert service.model_id == "meta.llama3-8b-instruct-v1:0"
    mock_boto3.assert_called_once_with(service_name="bedrock-runtime", region_name="us-east-1")

def test_retrieve_context():
    """Testa retrieval (mockado por enquanto)."""
    service = BedrockService()
    context = service.retrieve_context("query")
    assert "TDAH" in context

def test_invoke_model_success(mock_boto3):
    """Testa invocação do modelo com sucesso."""
    # Setup do mock de resposta do Boto3
    mock_client = mock_boto3.return_value
    mock_response_body = MagicMock()
    mock_response_body.read.return_value = b'{"generation": "Resposta gerada"}'
    mock_client.invoke_model.return_value = {"body": mock_response_body}

    service = BedrockService()
    response = service.invoke_model("prompt", "context")
    
    assert response == "Resposta gerada"
    mock_client.invoke_model.assert_called_once()
