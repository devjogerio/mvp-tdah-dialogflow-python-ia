from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import GoogleAPICallError, AlreadyExists
import os
import sys
import json
import logging
from typing import List, Dict, Any

# Fix for Python 3.14 + Protobuf compatibility issues
# Must be set before importing ANY google library
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")


logger = logging.getLogger(__name__)


class DialogflowManager:
    def __init__(self, project_id: str, credentials_path: str = None):
        """
        Gerenciador de automação para Dialogflow ES.

        Args:
            project_id: ID do projeto GCP.
            credentials_path: Caminho para o JSON de credenciais (opcional se usar env var).
        """
        self.project_id = project_id
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.intents_client = dialogflow.IntentsClient()
        self.entity_types_client = dialogflow.EntityTypesClient()
        self.parent = f"projects/{project_id}/agent"

    def create_entity_type(self, display_name: str, kind: str, entries: List[Dict]):
        """Cria uma entidade customizada."""
        parent = f"projects/{self.project_id}/agent"

        # Check if exists
        # Simplified logic: In prod, list and check names first to avoid errors or duplication

        entity_type = dialogflow.EntityType(
            display_name=display_name,
            kind=getattr(dialogflow.EntityType.Kind, kind,
                         dialogflow.EntityType.Kind.KIND_MAP)
        )

        created_entries = []
        for entry in entries:
            created_entries.append(
                dialogflow.EntityType.Entity(
                    value=entry['value'],
                    synonyms=entry['synonyms']
                )
            )

        # Normalmente cria-se o tipo primeiro e depois batch update das entidades,
        # mas aqui simplificamos a criação.
        try:
            response = self.entity_types_client.create_entity_type(
                parent=parent,
                entity_type=entity_type
            )

            # Add entries
            self.entity_types_client.batch_create_entities(
                parent=response.name,
                entities=created_entries
            )
            logger.info(f"Entidade criada: {display_name}")
            return response

        except AlreadyExists:
            logger.warning(f"Entidade {display_name} já existe.")
        except Exception as e:
            logger.error(f"Erro ao criar entidade {display_name}: {e}")

    def create_intent(self, intent_data: Dict[str, Any]):
        """Cria uma Intent completa."""
        display_name = intent_data.get("display_name")
        training_phrases_raw = intent_data.get("training_phrases", [])
        messages_raw = intent_data.get("messages", [])

        training_phrases = []
        for phrase in training_phrases_raw:
            part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
            training_phrases.append(
                dialogflow.Intent.TrainingPhrase(parts=[part])
            )

        messages = []
        for msg in messages_raw:
            if "text" in msg:
                text_obj = dialogflow.Intent.Message.Text(text=msg["text"])
                messages.append(dialogflow.Intent.Message(text=text_obj))

        intent = dialogflow.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=messages,
            priority=intent_data.get("priority", 500000),
            webhook_state=getattr(dialogflow.Intent.WebhookState,
                                  intent_data.get("webhook_state", "WEBHOOK_STATE_UNSPECIFIED"))
        )

        # Parameters (Entities linkage) would go here

        try:
            response = self.intents_client.create_intent(
                parent=self.parent,
                intent=intent
            )
            logger.info(f"Intent criada: {display_name}")
            return response
        except Exception as e:
            logger.error(f"Erro ao criar intent {display_name}: {e}")

    def sync_from_json(self, json_path: str):
        """Sincroniza a configuração a partir de um JSON."""
        with open(json_path, 'r') as f:
            data = json.load(f)

        # 1. Sync Entities
        for entity in data.get("entities", []):
            self.create_entity_type(
                entity["display_name"],
                entity["kind"],
                entity["entries"]
            )

        # 2. Sync Intents
        for intent in data.get("intents", []):
            self.create_intent(intent)

    def export_to_json(self, output_path: str):
        """Exporta a configuração atual para JSON (Backup)."""
        data = {"intents": [], "entities": []}

        # List Intents
        intents = self.intents_client.list_intents(parent=self.parent)
        for intent in intents:
            intent_dict = {
                "display_name": intent.display_name,
                "priority": intent.priority,
                "training_phrases": [
                    "".join([part.text for part in phrase.parts])
                    for phrase in intent.training_phrases
                ],
                "messages": [
                    {"text": list(msg.text.text)}
                    for msg in intent.messages if msg.text
                ]
            }
            data["intents"].append(intent_dict)

        # List Entity Types (Simplified)
        # ... implementation for entities export ...

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Configuração exportada para {output_path}")


if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Exemplo de Uso
    logging.basicConfig(level=logging.INFO)
    project_id = os.getenv("GCP_PROJECT_ID")

    if not project_id:
        logger.warning(
            "GCP_PROJECT_ID not found in environment variables. Using default/placeholder.")
        project_id = "mvp-tdah-dialogflow-pytho-q9ys"

    manager = DialogflowManager(project_id)
    # manager.sync_from_json("src/dialogflow/data/initial_config.json")
