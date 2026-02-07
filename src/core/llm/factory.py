import os
import logging
from .base import LLMProvider
from .bedrock import BedrockLLM
from .gemini import GeminiLLM
from .openai import OpenAILLM

logger = logging.getLogger(__name__)

class LLMFactory:
    """
    Factory para criar instâncias de provedores LLM baseados na configuração.
    """

    @staticmethod
    def create_provider() -> LLMProvider:
        """
        Cria e retorna o provedor de LLM configurado via variável de ambiente LLM_PROVIDER.
        Valores aceitos: 'bedrock', 'gemini', 'openai'.
        Default: 'bedrock'.
        """
        provider_name = os.getenv("LLM_PROVIDER", "bedrock").lower()
        
        logger.info(f"Inicializando provedor de LLM: {provider_name}")

        if provider_name == "gemini":
            return GeminiLLM()
        elif provider_name == "openai":
            return OpenAILLM()
        elif provider_name == "bedrock":
            return BedrockLLM()
        else:
            logger.warning(f"Provedor '{provider_name}' desconhecido. Usando fallback para Bedrock.")
            return BedrockLLM()
