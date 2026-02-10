import logging
from typing import Any, Dict

from src.presentation.handlers.lambda_handler import (
    lambda_handler as presentation_handler,
)

# Configuração de Logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Entrypoint (Legacy Wrapper).
    Delegates to Presentation Layer Handler.
    """
    return presentation_handler(event, context)
