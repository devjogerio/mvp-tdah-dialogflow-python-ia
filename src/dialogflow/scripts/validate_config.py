import json
import sys
import logging
from pathlib import Path

# Configuração de Logs
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ConfigValidator")

CONFIG_PATH = "src/dialogflow/data/initial_config.json"


def validate_config(path):
    logger.info(f"Validando arquivo: {path}")

    if not Path(path).exists():
        logger.error("Arquivo de configuração não encontrado!")
        sys.exit(1)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSON inválido: {e}")
        sys.exit(1)

    # Validação de Schema Básico
    errors = []

    if "intents" not in data:
        errors.append("Chave obrigatória 'intents' ausente.")
    else:
        for idx, intent in enumerate(data["intents"]):
            if "display_name" not in intent:
                errors.append(f"Intent no índice {idx} sem 'display_name'.")
            if "messages" not in intent:
                errors.append(
                    f"Intent '{intent.get('display_name', idx)}' sem 'messages'.")
            if "training_phrases" not in intent:
                logger.warning(
                    f"Intent '{intent.get('display_name', idx)}' sem frases de treinamento (pode ser intencional).")

    if "entities" not in data:
        errors.append("Chave obrigatória 'entities' ausente.")
    else:
        for idx, entity in enumerate(data["entities"]):
            if "display_name" not in entity:
                errors.append(f"Entity no índice {idx} sem 'display_name'.")
            if "entries" not in entity:
                errors.append(
                    f"Entity '{entity.get('display_name', idx)}' sem 'entries'.")

    if errors:
        for err in errors:
            logger.error(err)
        logger.error("Validação falhou com erros.")
        sys.exit(1)

    logger.info("✅ Configuração válida e pronta para deploy!")
    sys.exit(0)


if __name__ == "__main__":
    validate_config(CONFIG_PATH)
