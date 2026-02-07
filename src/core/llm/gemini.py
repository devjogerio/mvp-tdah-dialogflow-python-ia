import google.generativeai as genai
import os
import logging
from .base import LLMProvider

logger = logging.getLogger(__name__)

class GeminiLLM(LLMProvider):
    """
    Implementação do provedor Google Gemini.
    """

    def __init__(self):
        """
        Inicializa o cliente Gemini.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY não configurada.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def invoke(self, prompt: str, context: str = "") -> str:
        """
        Invoca o modelo Google Gemini.
        """
        try:
            # Construção do Prompt
            formatted_prompt = f"""
Você é um assistente de saúde mental empático, especializado em TDAH, ansiedade e depressão.
Sua missão é fornecer apoio psicoeducativo com base APENAS no contexto fornecido abaixo.

Contexto de Referência:
{context}

Regras de Resposta:
- Use linguagem simples, direta e acolhedora.
- Formate a resposta com bullet points para facilitar a leitura.
- Use negrito em palavras-chave importantes.
- Limite sua resposta a no máximo 3 parágrafos curtos.
- Se a informação não estiver no contexto, diga que não sabe, não invente.

Pergunta do Usuário:
{prompt}
"""
            
            response = self.model.generate_content(formatted_prompt)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Erro ao invocar Gemini: {str(e)}")
            return "Desculpe, estou tendo dificuldades para processar sua solicitação no momento (Erro Gemini)."
