import os
import logging
from src.core.opensearch_service import OpenSearchService
from src.core.llm.factory import LLMFactory

"""
Módulo de Serviço do Assistente.
Orquestra a recuperação de contexto (RAG) e a geração de resposta via LLM.
Substitui o antigo bedrock_integration.py para suportar múltiplos modelos.
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AssistantService:
    def __init__(self, region_name: str = "us-east-1"):
        """
        Inicializa o serviço do assistente, configurando RAG e LLM.

        Args:
            region_name (str): Região AWS (usada para OpenSearch/Bedrock se necessário).
        """
        # 1. Inicializa o Provedor de LLM via Factory
        self.llm_provider = LLMFactory.create_provider()

        # 2. Inicializa o Serviço de RAG (OpenSearch)
        opensearch_host = os.getenv("OPENSEARCH_HOST", "")
        if opensearch_host:
            self.opensearch_service = OpenSearchService(
                opensearch_host, region_name)
        else:
            self.opensearch_service = None
            logger.warning(
                "OPENSEARCH_HOST não definido. RAG funcionará em modo mock.")

    def retrieve_context(self, query: str) -> str:
        """
        Busca vetorial (RAG) no OpenSearch Serverless.

        Args:
            query (str): A busca do usuário.

        Returns:
            str: Contexto relevante recuperado.
        """
        if self.opensearch_service:
            # 1. Gerar embedding da query (Idealmente, usaríamos um serviço de embedding agnóstico aqui também)
            # Por enquanto, mantemos o placeholder ou lógica do OpenSearchService
            # Em produção real, isso deveria chamar o provider de embedding correspondente
            query_vector = [0.1] * 1536  # Placeholder

            context = self.opensearch_service.search(query_vector)
            if context:
                return context

        # Fallback Mock
        logger.info(f"Buscando contexto (Mock) para: {query}")
        return "O TDAH (Transtorno de Déficit de Atenção e Hiperatividade) é um transtorno neurobiológico caracterizado por desatenção, hiperatividade e impulsividade..."

    def invoke_model(self, prompt: str, context: str = "") -> str:
        """
        Invoca o modelo LLM configurado.

        Args:
            prompt (str): Pergunta do usuário.
            context (str): Contexto recuperado do Knowledge Base (RAG).

        Returns:
            str: Resposta gerada pelo modelo.
        """
        return self.llm_provider.invoke(prompt, context)
