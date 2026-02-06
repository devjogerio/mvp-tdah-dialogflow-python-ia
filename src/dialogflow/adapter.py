from typing import Dict, Any, Tuple, Optional
import json
import logging

logger = logging.getLogger(__name__)

class DialogflowAdapter:
    """
    Adaptador para normalizar a comunicação entre AWS Lambda e Google Dialogflow.
    Responsável por fazer o parse do WebhookRequest e formatar o WebhookResponse.
    """

    @staticmethod
    def parse_event(event: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        """
        Analisa o evento de entrada e extrai a mensagem do usuário e metadados.
        Suporta tanto API Gateway Proxy (REST padrão) quanto Dialogflow Webhook.

        Returns:
            user_message (str): Texto enviado pelo usuário.
            session_id (str): Identificador da sessão.
            parameters (dict): Parâmetros extraídos pelo Dialogflow (slots).
        """
        try:
            body = event
            
            # Se vier via API Gateway Proxy, o body é uma string dentro de 'body'
            if "body" in event and isinstance(event["body"], str):
                body = json.loads(event["body"])
            elif "body" in event:
                body = event["body"]

            # 1. Detecção de Payload Dialogflow (WebhookRequest)
            if "queryResult" in body:
                logger.info("Payload Dialogflow detectado.")
                query_result = body.get("queryResult", {})
                user_message = query_result.get("queryText", "")
                parameters = query_result.get("parameters", {})
                
                # Session path ex: projects/project-id/agent/sessions/SESSION_ID
                full_session = body.get("session", "")
                session_id = full_session.split("/")[-1] if "/" in full_session else full_session
                
                return user_message, session_id, parameters

            # 2. Detecção de Payload Genérico (Teste Local / API Direta)
            logger.info("Payload Genérico/API detectado.")
            user_message = body.get("message", "")
            session_id = body.get("session_id", "default-session")
            return user_message, session_id, {}

        except Exception as e:
            logger.error(f"Erro ao fazer parse do evento: {e}")
            return "", "", {}

    @staticmethod
    def format_response(text: str, is_dialogflow: bool = False) -> Dict[str, Any]:
        """
        Formata a resposta para o cliente adequado.

        Args:
            text: O texto da resposta gerada.
            is_dialogflow: Se True, retorna formato WebhookResponse. Caso contrário, JSON simples.
        """
        if is_dialogflow:
            # Formato padrão Dialogflow WebhookResponse
            return {
                "fulfillmentText": text,
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [text]
                        }
                    }
                ]
            }
        else:
            # Formato API padrão
            return {
                "response": text
            }
