import logging

from src.domain.interfaces.repositories import ContextRepository


class MockOpenSearchRepository(ContextRepository):
    def retrieve_context(self, query: str) -> str:
        logging.info(f"Mock retrieving context for: {query}")
        return "Este é um contexto simulado sobre TDAH para testes."
