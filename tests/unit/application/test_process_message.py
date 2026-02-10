from unittest.mock import Mock

import pytest

from src.application.dtos.message_dto import ProcessMessageInput
from src.application.use_cases.process_message import ProcessUserMessage
from src.domain.interfaces.repositories import ContextRepository, LLMProvider


class TestProcessUserMessage:
    @pytest.fixture
    def mock_llm_provider(self):
        return Mock(spec=LLMProvider)

    @pytest.fixture
    def mock_context_repo(self):
        return Mock(spec=ContextRepository)

    @pytest.fixture
    def use_case(self, mock_llm_provider, mock_context_repo):
        return ProcessUserMessage(mock_llm_provider, mock_context_repo)

    def test_execute_safe_message(self, use_case, mock_llm_provider, mock_context_repo):
        # Arrange
        input_dto = ProcessMessageInput(
            user_id="123", session_id="abc", message="Olá, como vai?", platform="api"
        )
        mock_context_repo.retrieve_context.return_value = "Contexto relevante"
        mock_llm_provider.invoke.return_value = "Estou bem!"

        # Act
        result = use_case.execute(input_dto)

        # Assert
        assert result.response_text == "Estou bem!"
        assert result.risk_detected is False
        mock_context_repo.retrieve_context.assert_called_once_with("Olá, como vai?")
        mock_llm_provider.invoke.assert_called_once_with(
            prompt="Olá, como vai?", context={"rag_content": "Contexto relevante"}
        )

    def test_execute_unsafe_message(
        self, use_case, mock_llm_provider, mock_context_repo
    ):
        # Arrange
        input_dto = ProcessMessageInput(
            user_id="123", session_id="abc", message="Quero morrer", platform="api"
        )

        # Act
        result = use_case.execute(input_dto)

        # Assert
        assert result.risk_detected is True
        # Verifica se retornou mensagem de emergência (conteúdo exato depende do safety_filters)
        assert len(result.response_text) > 0
        mock_llm_provider.invoke.assert_not_called()
