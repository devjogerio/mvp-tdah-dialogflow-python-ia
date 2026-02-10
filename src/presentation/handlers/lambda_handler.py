import json
import logging
from typing import Any, Dict

from src.application.dtos.message_dto import ProcessMessageInput
from src.application.use_cases.process_message import ProcessUserMessage
from src.infrastructure.llm.bedrock_adapter import BedrockLLM
from src.infrastructure.repositories.opensearch_repository import (
    MockOpenSearchRepository,
)

# Configuração de Logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Injeção de Dependência Manual (Composition Root)
# Em produção, isso poderia ser feito com um container (Dependency Injector)
llm_provider = BedrockLLM()
context_repo = MockOpenSearchRepository()
process_message_uc = ProcessUserMessage(llm_provider, context_repo)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Entrypoint (Presentation Layer).
    Recebe o evento JSON, converte para DTO, chama a Application Layer e retorna JSON.
    """
    try:
        logger.info(f"Evento recebido: {json.dumps(event)}")

        # 1. Parse Input (Adaptação Básica)
        body = (
            json.loads(event.get("body", "{}"))
            if isinstance(event.get("body"), str)
            else event.get("body", {})
        )

        # Detecta se é Dialogflow (simplificado para este exemplo)
        is_dialogflow = "queryResult" in body
        user_message = (
            body.get("queryResult", {}).get("queryText")
            if is_dialogflow
            else body.get("message")
        )
        session_id = body.get("session", "unknown_session")

        if not user_message:
            return {"statusCode": 400, "body": json.dumps({"error": "Mensagem vazia"})}

        # 2. Criação do DTO
        input_dto = ProcessMessageInput(
            user_id="anonymous",  # TODO: Extrair do evento
            session_id=session_id,
            message=user_message,
            platform="dialogflow" if is_dialogflow else "api",
        )

        # 3. Execução do Use Case
        output_dto = process_message_uc.execute(input_dto)

        # 4. Formatação da Resposta
        response_body = (
            {"fulfillmentText": output_dto.response_text}
            if is_dialogflow
            else {
                "response": output_dto.response_text,
                "risk_detected": output_dto.risk_detected,
            }
        )

        return {"statusCode": 200, "body": json.dumps(response_body)}

    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro interno do servidor"}),
        }
