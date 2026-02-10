from src.infrastructure.repositories.opensearch_repository import (
    MockOpenSearchRepository,
)


def test_mock_repository_retrieve():
    repo = MockOpenSearchRepository()
    context = repo.retrieve_context("qualquer coisa")
    assert context == "Este é um contexto simulado sobre TDAH para testes."
