from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.domain.entities.session import Session


class LLMProvider(ABC):
    @abstractmethod
    def invoke(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Invokes the LLM to generate a response."""
        pass


class SessionRepository(ABC):
    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Session]:
        pass

    @abstractmethod
    def save_session(self, session: Session) -> None:
        pass


class ContextRepository(ABC):
    @abstractmethod
    def retrieve_context(self, query: str) -> str:
        pass
