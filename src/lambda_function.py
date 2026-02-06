import json
import logging
from src.utils.safety_filters import check_safety
from src.core.bedrock_integration import BedrockService
from src.dialogflow.adapter import DialogflowAdapter

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
    Suporta payload do Dialogflow (WebhookRequest) e API Gateway padrão.
    """
    try:
        logger.info("Evento recebido: %s", json.dumps(event))
        
        # 1. Parsing e Adaptação de Entrada
        user_message, session_id, params = DialogflowAdapter.parse_event(event)
        
        # Detecta se é requisição Dialogflow pela presença de session_id com formato de projeto ou params
        # (Lógica simplificada, o adapter já trata a maior parte)
        is_dialogflow = "queryResult" in (json.loads(event.get("body", "{}")) if isinstance(event.get("body"), str) else event.get("body", {}))

        if not user_message:
            error_msg = "Mensagem vazia ou formato inválido."
            logger.warning(error_msg)
            response_body = DialogflowAdapter.format_response(error_msg, is_dialogflow)
            return {
                "statusCode": 400,
                "body": json.dumps(response_body)
            }

        logger.info(f"Processando mensagem: '{user_message}' [Sessão: {session_id}]")

        # 2. Verificação de Segurança (RF02)
        is_safe, emergency_msg = check_safety(user_message)
        
        if not is_safe:
            logger.warning(f"Conteúdo de risco detectado na sessão {session_id}.")
            response_body = DialogflowAdapter.format_response(emergency_msg, is_dialogflow)
            # Adiciona flag extra apenas para API direta (Dialogflow ignora campos extras no root)
            if not is_dialogflow:
                response_body["risk_detected"] = True
                
            return {
                "statusCode": 200,
                "body": json.dumps(response_body)
            }

        # 3. Recuperação de Contexto (RAG)
        # TODO: Passar session_id para o retrieve_context se implementar histórico no futuro
        context_data = bedrock_service.retrieve_context(user_message)

        # 4. Geração de Resposta (LLM)
        response_text = bedrock_service.invoke_model(user_message, context_data)

        # 5. Formatação de Saída
        response_body = DialogflowAdapter.format_response(response_text, is_dialogflow)
        if not is_dialogflow:
            response_body["risk_detected"] = False

        return {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }

    except Exception as e:
        logger.error("Erro interno no Lambda: %s", str(e), exc_info=True)
        
        # Tenta determinar formato de erro seguro
        try:
            is_dialogflow_error = "queryResult" in (json.loads(event.get("body", "{}")) if isinstance(event.get("body"), str) else event.get("body", {}))
        except:
            is_dialogflow_error = False

        error_text = "Desculpe, estou enfrentando dificuldades técnicas no momento. Tente novamente em alguns segundos."
        response_body = DialogflowAdapter.format_response(error_text, is_dialogflow_error)
        
        return {
            "statusCode": 200 if is_dialogflow_error else 500, # Dialogflow precisa de 200 com texto de erro
            "body": json.dumps(response_body)
        }
