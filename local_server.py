import json
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.lambda_function import lambda_handler

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LocalServer")

app = FastAPI(
    title="Chatbot TDAH - Local Dev Server",
    description="Servidor local para testar a lógica da função Lambda via FastAPI",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Simula a invocação da Lambda via API Gateway
    """
    # Simula estrutura do evento API Gateway
    event = {"body": json.dumps({"message": request.message})}
    context = {}  # Contexto vazio para simulação

    logger.info(f"Recebendo mensagem: {request.message}")

    # Chama o handler original
    response = lambda_handler(event, context)

    # Processa resposta
    if response["statusCode"] != 200:
        raise HTTPException(
            status_code=response["statusCode"], detail=response.get("body")
        )

    try:
        body = json.loads(response["body"])
        return body
    except (json.JSONDecodeError, TypeError):
        return response["body"]


@app.get("/health")
async def health():
    return {"status": "ok", "environment": "local_docker"}
