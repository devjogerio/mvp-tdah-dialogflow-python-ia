import pytest
from unittest.mock import patch, MagicMock
from src.core.llm.factory import LLMFactory
from src.core.llm.bedrock import BedrockLLM
from src.core.llm.gemini import GeminiLLM
from src.core.llm.openai import OpenAILLM

class TestLLMFactory:

    @patch("os.getenv")
    def test_create_provider_default(self, mock_getenv):
        """Testa se o factory retorna BedrockLLM por padrão."""
        mock_getenv.return_value = "bedrock"
        provider = LLMFactory.create_provider()
        assert isinstance(provider, BedrockLLM)

    @patch("os.getenv")
    def test_create_provider_gemini(self, mock_getenv):
        """Testa se o factory retorna GeminiLLM quando configurado."""
        mock_getenv.return_value = "gemini"
        with patch("src.core.llm.gemini.genai"): # Mock dependência externa
            provider = LLMFactory.create_provider()
            assert isinstance(provider, GeminiLLM)

    @patch("os.getenv")
    def test_create_provider_openai(self, mock_getenv):
        """Testa se o factory retorna OpenAILLM quando configurado."""
        mock_getenv.return_value = "openai"
        with patch("src.core.llm.openai.OpenAI"): # Mock dependência externa
            provider = LLMFactory.create_provider()
            assert isinstance(provider, OpenAILLM)

    @patch("os.getenv")
    def test_create_provider_invalid(self, mock_getenv):
        """Testa fallback para BedrockLLM com provider inválido."""
        mock_getenv.return_value = "invalid_provider"
        provider = LLMFactory.create_provider()
        assert isinstance(provider, BedrockLLM)
