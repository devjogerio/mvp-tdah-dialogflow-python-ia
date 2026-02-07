#!/bin/bash

# ==============================================================================
# Script de Automação de Upload de Intents para Dialogflow
# ==============================================================================
# Este script configura o ambiente e executa a sincronização de intents e entidades
# definidas em src/dialogflow/data/initial_config.json para o projeto GCP.
#
# Pré-requisitos:
# - Python 3.9+ instalado
# - Dependências instaladas (pip install -r requirements.txt)
# - Chave de Conta de Serviço válida em key-json/
# ==============================================================================

# Configurações do Projeto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KEY_JSON_DIR="${PROJECT_ROOT}/key-json"
KEY_FILE_NAME="mvp-tdah-dialogflow-pytho-q9ys-4e593eb54acb.json"
CREDENTIALS_PATH="${KEY_JSON_DIR}/${KEY_FILE_NAME}"
PYTHON_SCRIPT="${PROJECT_ROOT}/src/dialogflow/manager.py"

# Cores para logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função de Log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARN: $1${NC}"
}

# 1. Validação de Pré-condições
log "Iniciando verificação de pré-condições..."

if [ ! -f "$CREDENTIALS_PATH" ]; then
    error "Arquivo de credenciais não encontrado em: $CREDENTIALS_PATH"
    error "Por favor, coloque o arquivo JSON da chave de serviço no diretório key-json."
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    error "Script Python de automação não encontrado em: $PYTHON_SCRIPT"
    exit 1
fi

# 2. Configuração de Variáveis de Ambiente
log "Configurando variáveis de ambiente..."

export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_PATH"
log "GOOGLE_APPLICATION_CREDENTIALS definido para: $CREDENTIALS_PATH"

# Fix para Python 3.14+ (se necessário) e compatibilidade Protobuf
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
log "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION definido para: python"

# Carrega variáveis do .env se existir (para GCP_PROJECT_ID)
if [ -f "${PROJECT_ROOT}/.env" ]; then
    log "Lendo configurações do arquivo .env..."
    # Tenta extrair o ID do projeto manualmente para validação no shell
    ENV_PROJECT_ID=$(grep "^GCP_PROJECT_ID=" "${PROJECT_ROOT}/.env" | cut -d '=' -f2)
    if [ ! -z "$ENV_PROJECT_ID" ]; then
        export GCP_PROJECT_ID=$ENV_PROJECT_ID
    fi
fi

if [ -z "$GCP_PROJECT_ID" ]; then
    error "GCP_PROJECT_ID não está definido. Verifique seu arquivo .env."
    exit 1
fi

log "Projeto GCP Alvo: $GCP_PROJECT_ID"

# 3. Execução da Automação com Retry Simples no Nível do Shell
# O script Python já possui retries internos robustos, mas adicionamos uma camada extra aqui.

MAX_RETRIES=3
RETRY_COUNT=0
SUCCESS=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    log "Iniciando sincronização com Dialogflow (Tentativa $((RETRY_COUNT+1))/$MAX_RETRIES)..."
    
    # Executa o script Python
    # Adiciona PROJECT_ROOT ao PYTHONPATH para garantir imports corretos
    export PYTHONPATH="${PROJECT_ROOT}:$PYTHONPATH"
    
    python3 "$PYTHON_SCRIPT"
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        log "✅ Sincronização concluída com sucesso!"
        SUCCESS=1
        break
    else
        warn "❌ Falha na execução (Código de Saída: $EXIT_CODE)."
        RETRY_COUNT=$((RETRY_COUNT+1))
        
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            WAIT_TIME=$((RETRY_COUNT * 5))
            log "Aguardando $WAIT_TIME segundos antes da próxima tentativa..."
            sleep $WAIT_TIME
        fi
    fi
done

# 4. Validação Pós-Execução e Relatório
if [ $SUCCESS -eq 1 ]; then
    log "========================================================"
    log "RELATÓRIO DE IMPLANTAÇÃO"
    log "========================================================"
    log "Status: SUCESSO"
    log "Logs detalhados disponíveis em: automation_report.log"
    log "Verifique o console do Dialogflow para confirmar visualmente:"
    log "https://dialogflow.cloud.google.com/#/agent/$GCP_PROJECT_ID/intents"
    exit 0
else
    error "========================================================"
    error "RELATÓRIO DE IMPLANTAÇÃO"
    error "========================================================"
    error "Status: FALHA CRÍTICA após $MAX_RETRIES tentativas."
    error "Verifique os logs acima e o arquivo automation_report.log para depuração."
    exit 1
fi
