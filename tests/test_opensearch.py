import pytest
from unittest.mock import MagicMock, patch
from src.core.opensearch_service import OpenSearchService

@pytest.fixture
def mock_opensearch_client():
    with patch("src.core.opensearch_service.OpenSearch") as mock:
        yield mock

def test_opensearch_init_no_creds():
    """Testa inicialização sem credenciais (fallback)."""
    with patch("boto3.Session") as mock_session:
        mock_session.return_value.get_credentials.return_value = None
        service = OpenSearchService("host")
        assert service.host == "host"

def test_search_success(mock_opensearch_client):
    """Testa busca vetorial com sucesso."""
    mock_client_instance = mock_opensearch_client.return_value
    mock_client_instance.search.return_value = {
        'hits': {
            'hits': [
                {'_source': {'text': 'Contexto 1'}},
                {'_source': {'text': 'Contexto 2'}}
            ]
        }
    }

    service = OpenSearchService("host")
    result = service.search([0.1, 0.2])
    
    assert "Contexto 1" in result
    assert "Contexto 2" in result

def test_search_error(mock_opensearch_client):
    """Testa tratamento de erro na busca."""
    mock_client_instance = mock_opensearch_client.return_value
    mock_client_instance.search.side_effect = Exception("Erro de conexão")

    service = OpenSearchService("host")
    result = service.search([0.1])
    
    assert result == ""
