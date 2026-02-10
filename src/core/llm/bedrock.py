import boto3
import json
import os
import logging
from .base import LLMProvider

logger = logging.getLogger(__name__)

class BedrockLLM(LLMProvider):
    """
    Implementação do provedor AWS Bedrock (Llama 3).
    """

    def __init__(self, region_name: str = "us-east-1"):
        """
        Inicializa o cliente Bedrock.
        """
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "meta.llama3-8b-instruct-v1:0")

    def invoke(self, prompt: str, context: str = "") -> str:
        """
        Invoca o modelo Llama 3 no AWS Bedrock.
        """
        try:
            # Construção do Prompt seguindo boas práticas para Llama 3
            formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Você é um assistente de saúde mental empático, especializado em TDAH, ansiedade e depressão.
Sua missão é fornecer apoio psicoeducativo com base APENAS no contexto fornecido.

Regras de Resposta:
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
            return "Desculpe, estou tendo dificuldades para processar sua solicitação no momento (Erro Bedrock)."
