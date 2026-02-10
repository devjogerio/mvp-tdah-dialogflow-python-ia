from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """
    Interface abstrata para provedores de LLM.
    Define o contrato que todos os provedores (Bedrock, Gemini, OpenAI) devem seguir.
    """

    @abstractmethod
    def invoke(self, prompt: str, context: str = "") -> str:
        """
        Invoca o modelo LLM com o prompt e contexto fornecidos.

        Args:
            prompt (str): A pergunta ou instrução do usuário.
            context (str): Contexto adicional recuperado (RAG) ou histórico.

        Returns:
            str: A resposta gerada pelo modelo.
        """
        pass
