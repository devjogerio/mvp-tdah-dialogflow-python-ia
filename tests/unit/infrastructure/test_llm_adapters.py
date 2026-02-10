from unittest.mock import MagicMock, patch

from src.infrastructure.llm.bedrock_adapter import BedrockLLM
from src.infrastructure.llm.gemini_adapter import GeminiLLM
from src.infrastructure.llm.openai_adapter import OpenAILLM


class TestBedrockLLM:
    @patch("boto3.client")
    def test_invoke_success(self, mock_boto):
        # Arrange
        mock_client = MagicMock()
        mock_boto.return_value = mock_client

        # Mock da resposta do Bedrock (Claude structure)
        mock_response_body = '{"generation": "Resposta do Bedrock"}'
        mock_client.invoke_model.return_value = {
            "body": MagicMock(read=lambda: mock_response_body.encode())
        }

        adapter = BedrockLLM(region_name="us-east-1")

        # Act
        response = adapter.invoke("Teste", {})

        # Assert
        assert response == "Resposta do Bedrock"
        mock_client.invoke_model.assert_called_once()


class TestOpenAILLM:
    @patch("src.infrastructure.llm.openai_adapter.OpenAI")
    @patch("os.getenv")
    def test_invoke_success(self, mock_getenv, mock_openai_class):
        # Arrange
        mock_getenv.return_value = "fake-key"
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Resposta OpenAI"
        mock_client.chat.completions.create.return_value = mock_completion

        adapter = OpenAILLM()

        # Act
        response = adapter.invoke("Teste")

        # Assert
        assert response == "Resposta OpenAI"


class TestGeminiLLM:
    @patch("src.infrastructure.llm.gemini_adapter.genai")
    @patch("os.getenv")
    def test_invoke_success(self, mock_getenv, mock_genai):
        # Arrange
        mock_getenv.return_value = "fake-key"
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model

        mock_response = MagicMock()
        mock_response.text = "Resposta Gemini"
        mock_model.generate_content.return_value = mock_response

        adapter = GeminiLLM()

        # Act
        response = adapter.invoke("Teste")

        # Assert
        assert response == "Resposta Gemini"
