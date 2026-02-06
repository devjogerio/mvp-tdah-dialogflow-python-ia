import boto3
import json
import os
import logging
from typing import Dict, Any
from src.core.opensearch_service import OpenSearchService

"""
Módulo de integração com Amazon Bedrock (RF01).
Gerencia a chamada ao LLM (Llama 3) e RAG.
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BedrockService:
    def __init__(self, region_name: str = "us-east-1"):
        """
        Inicializa o cliente Bedrock e OpenSearch.

        Args:
            region_name (str): Região AWS.
        """
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )
        self.model_id = os.getenv(
            "BEDROCK_MODEL_ID", "meta.llama3-8b-instruct-v1:0")

        # Inicialização do OpenSearch
        opensearch_host = os.getenv("OPENSEARCH_HOST", "")
        if opensearch_host:
            self.opensearch_service = OpenSearchService(
                opensearch_host, region_name)
        else:
            self.opensearch_service = None
            logger.warning(
                "OPENSEARCH_HOST não definido. RAG funcionará em modo mock.")

    def invoke_model(self, prompt: str, context: str = "") -> str:
        """
        Invoca o modelo Llama 3 com o prompt e contexto (RAG).

        Args:
            prompt (str): Pergunta do usuário.
            context (str): Contexto recuperado do Knowledge Base (RAG).

        Returns:
            str: Resposta gerada pelo modelo.
        """
        try:
            # Construção do Prompt seguindo boas práticas para Llama 3
            # System Prompt para persona e formatação (RF03)
            formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Você é um assistente de saúde mental empático, especializado em TDAH, ansiedade e depressão.
Sua missão é fornecer apoio psicoeducativo com base APENAS no contexto fornecido.

Regras de Resposta (RF03):
- Use linguagem simples, direta e acolhedora.
- Formate a resposta com bullet points para facilitar a leitura.
- Use negrito em palavras-chave importantes.
- Limite sua resposta a no máximo 3 parágrafos curtos.
- Se a informação não estiver no contexto, diga que não sabe, não invente.

Contexto de Referência:
{context}

<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

            body = json.dumps({
                "prompt": formatted_prompt,
                "max_gen_len": 512,
                "temperature": 0.2,
                "top_p": 0.9,
            })

            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body
            )

            response_body = json.loads(response.get("body").read())
            generation = response_body.get("generation", "")

            return generation.strip()

        except Exception as e:
            logger.error(f"Erro ao invocar Bedrock: {str(e)}")
            # Em caso de erro, retornar uma mensagem genérica de falha segura
            return "Desculpe, estou tendo dificuldades para processar sua solicitação no momento. Tente novamente em alguns instantes."

    def retrieve_context(self, query: str) -> str:
        """
        Busca vetorial (RAG) no OpenSearch Serverless.

        Args:
            query (str): A busca do usuário.

        Returns:
            str: Contexto relevante recuperado.
        """
        if self.opensearch_service:
            # 1. Gerar embedding da query (usando Bedrock Titan Embedding, por exemplo)
            # Aqui simplificamos assumindo um vetor dummy ou chamada mockada
            # Em prod, chamaríamos bedrock-runtime.invoke_model("amazon.titan-embed-text-v1")
            query_vector = [0.1] * 1536  # Placeholder

            context = self.opensearch_service.search(query_vector)
            if context:
                return context

        # Fallback Mock
        logger.info(f"Buscando contexto (Mock) para: {query}")
        return "O TDAH (Transtorno de Déficit de Atenção e Hiperatividade) é um transtorno neurobiológico caracterizado por desatenção, hiperatividade e impulsividade..."
