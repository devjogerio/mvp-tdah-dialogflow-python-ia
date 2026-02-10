import os
import logging
from openai import OpenAI
from .base import LLMProvider

logger = logging.getLogger(__name__)

class OpenAILLM(LLMProvider):
    """
    Implementação do provedor OpenAI (GPT).
    """

    def __init__(self):
        """
        Inicializa o cliente OpenAI.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY não configurada.")
            
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    def invoke(self, prompt: str, context: str = "") -> str:
        """
        Invoca o modelo GPT da OpenAI.
        """
        try:
            system_prompt = f"""
Você é um assistente de saúde mental empático, especializado em TDAH, ansiedade e depressão.
Sua missão é fornecer apoio psicoeducativo com base APENAS no contexto fornecido.

Contexto de Referência:
{context}

Regras de Resposta:
- Use linguagem simples, direta e acolhedora.
- Formate a resposta com bullet points para facilitar a leitura.
- Use negrito em palavras-chave importantes.
- Limite sua resposta a no máximo 3 parágrafos curtos.
- Se a informação não estiver no contexto, diga que não sabe, não invente.
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=512
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Erro ao invocar OpenAI: {str(e)}")
            return "Desculpe, estou tendo dificuldades para processar sua solicitação no momento (Erro OpenAI)."
