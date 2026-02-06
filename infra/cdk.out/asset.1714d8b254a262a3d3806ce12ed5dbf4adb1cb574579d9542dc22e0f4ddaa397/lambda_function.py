import json
import logging
from src.utils.safety_filters import check_safety
from src.core.bedrock_integration import BedrockService

"""
Lambda Function Principal.
Orquestra o fluxo de entrada, validação de segurança e geração de resposta (RAG).
"""

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicializa o serviço fora do handler para reutilização de contexto de execução
bedrock_service = BedrockService()

def lambda_handler(event, context):
    """
    Handler principal da AWS Lambda.

    Esperado formato de evento (exemplo via API Gateway/Dialogflow):
    {
        "body": "{\"message\": \"O que é TDAH?\"}"
    }
    """
    try:
        logger.info("Evento recebido: %s", json.dumps(event))
        
        # Extração da mensagem do usuário
        # Adapte conforme a origem do evento (API Gateway Proxy vs Direct Invoke)
        if "body" in event:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
            user_message = body.get("message", "")
        else:
            user_message = event.get("message", "")

        if not user_message:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Mensagem vazia."})
            }

        # 1. Verificação de Segurança (RF02)
        is_safe, emergency_msg = check_safety(user_message)
        
        if not is_safe:
            logger.warning("Conteúdo de risco detectado.")
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "response": emergency_msg,
                    "risk_detected": True
                })
            }

        # 2. Recuperação de Contexto (RAG)
        context_data = bedrock_service.retrieve_context(user_message)

        # 3. Geração de Resposta (LLM)
        response_text = bedrock_service.invoke_model(user_message, context_data)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "response": response_text,
                "risk_detected": False
            })
        }

    except Exception as e:
        logger.error("Erro interno: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro interno do servidor."})
        }
