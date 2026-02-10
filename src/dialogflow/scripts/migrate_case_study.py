import json
import logging
import os

from src.dialogflow.parsers.markdown_parser import CaseStudyParser

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("MigrationScript")

CONFIG_PATH = "src/dialogflow/data/initial_config.json"
MARKDOWN_PATH = "docs/esudo-de-caso.md"


def load_config(path):
    if not os.path.exists(path):
        return {"intents": [], "entities": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Configuração salva em {path}")


def validate_schema(data):
    """Validação simples do schema esperado."""
    required_keys = ["intents", "entities"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Schema inválido: chave '{key}' ausente.")
        if not isinstance(data[key], list):
            raise ValueError(f"Schema inválido: '{key}' deve ser uma lista.")
    logger.info("Validação de schema OK.")


def merge_data(existing, new_data):
    """
    Realiza o merge (upsert) de intents e entities.
    Usa 'display_name' como chave única.
    """
    # Merge Intents
    existing_intents = {i["display_name"]: i for i in existing.get("intents", [])}
    for intent in new_data.get("intents", []):
        name = intent["display_name"]
        if name in existing_intents:
            logger.info(f"Atualizando Intent: {name}")
            existing_intents[name].update(intent)
        else:
            logger.info(f"Criando Intent: {name}")
            existing_intents[name] = intent

    # Merge Entities
    existing_entities = {e["display_name"]: e for e in existing.get("entities", [])}
    for entity in new_data.get("entities", []):
        name = entity["display_name"]
        if name in existing_entities:
            logger.info(f"Atualizando Entity: {name}")
            # Merge entries for entities
            current_entries = {
                entry["value"]: entry for entry in existing_entities[name]["entries"]
            }
            for entry in entity["entries"]:
                current_entries[entry["value"]] = entry
            existing_entities[name]["entries"] = list(current_entries.values())
        else:
            logger.info(f"Criando Entity: {name}")
            existing_entities[name] = entity

    return {
        "intents": list(existing_intents.values()),
        "entities": list(existing_entities.values()),
    }


def main():
    logger.info("Iniciando migração...")

    # 1. Parse do Markdown
    parser = CaseStudyParser()
    logger.info(f"Lendo arquivo {MARKDOWN_PATH}...")
    extracted_data = parser.parse(MARKDOWN_PATH)

    # 2. Carregar config atual
    current_config = load_config(CONFIG_PATH)

    # 3. Merge
    merged_config = merge_data(current_config, extracted_data)

    # 4. Validação
    try:
        validate_schema(merged_config)
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        return

    # 5. Salvar
    save_config(CONFIG_PATH, merged_config)
    logger.info("Migração concluída com sucesso!")


if __name__ == "__main__":
    main()
