import pytest
from unittest.mock import MagicMock, patch
from src.core.assistant_service import AssistantService
from src.core.llm.bedrock import BedrockLLM

@pytest.fixture
def mock_llm_factory():
    with patch("src.core.assistant_service.LLMFactory") as mock:
        # Configura o factory para retornar um mock de BedrockLLM por padrão
        mock_provider = MagicMock(spec=BedrockLLM)
        mock_provider.invoke.return_value = "Resposta gerada"
        mock.create_provider.return_value = mock_provider
        yield mock

def test_assistant_init(mock_llm_factory):
    """Testa inicialização do serviço AssistantService."""
    service = AssistantService()
    mock_llm_factory.create_provider.assert_called_once()
    assert service.llm_provider is not None

def test_retrieve_context(mock_llm_factory):
    """Testa retrieval (mockado por enquanto)."""
    service = AssistantService()
    # Mock do opensearch_service para não precisar de credenciais
    service.opensearch_service = None

    context = service.retrieve_context("query")
    assert "TDAH" in context

def test_invoke_model_success(mock_llm_factory):
    """Testa invocação do modelo com sucesso."""
    service = AssistantService()
    
    response = service.invoke_model("prompt", "context")

    assert response == "Resposta gerada"
    service.llm_provider.invoke.assert_called_once_with("prompt", "context")
