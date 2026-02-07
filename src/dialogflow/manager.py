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
        # Monta o identificador completo do agente no formato exigido pela API
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
            logger.info(f"Entidade criada: {display_name}")

        except AlreadyExists:
            logger.info(f"Entidade {display_name} já existe. Atualizando...")
            # Recuperar ID da entidade existente para atualizar
            # Listar todas para encontrar o ID (não é o mais eficiente, mas funciona para script de sync)
            all_entities = self.entity_types_client.list_entity_types(
                parent=parent)
            target_name = None
            for ent in all_entities:
                if ent.display_name == display_name:
                    target_name = ent.name
                    break

            if target_name:
                entity_type.name = target_name
                response = self.entity_types_client.update_entity_type(
                    entity_type=entity_type)
                logger.info(f"Entidade atualizada: {display_name}")
            else:
                logger.error(
                    f"Erro: Entidade {display_name} reportada como existente mas não encontrada na lista.")
                return

        except Exception as e:
            logger.error(
                f"Erro ao criar/atualizar entidade {display_name}: {e}")
            return

        # Add/Update entries (Batch Update)
        if hasattr(response, 'name'):
            try:
                self.entity_types_client.batch_update_entities(
                    parent=response.name,
                    entities=created_entries
                )
                logger.info(
                    f"Entradas da entidade {display_name} sincronizadas.")
            except Exception as e:
                logger.error(
                    f"Erro ao atualizar entradas da entidade {display_name}: {e}")

        return response

    def create_intent(self, intent_data: Dict[str, Any]):
        """Cria ou atualiza uma Intent completa."""
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

        except AlreadyExists:
            logger.info(f"Intent {display_name} já existe. Atualizando...")
            # Buscar intent existente para pegar o ID (name)
            # Nota: Listar tudo pode ser lento em agentes grandes. O ideal seria cachear ou usar filtro.
            # Usando list_intents com filtro de view
            intents = self.intents_client.list_intents(
                parent=self.parent, intent_view=dialogflow.IntentView.INTENT_VIEW_FULL)
            target_name = None
            for i in intents:
                if i.display_name == display_name:
                    target_name = i.name
                    break

            if target_name:
                intent.name = target_name
                response = self.intents_client.update_intent(
                    intent=intent, intent_view=dialogflow.IntentView.INTENT_VIEW_FULL)
                logger.info(f"Intent atualizada: {display_name}")
                return response
            else:
                logger.error(
                    f"Intent {display_name} não encontrada para atualização.")

        except Exception as e:
            logger.error(f"Erro ao criar/atualizar intent {display_name}: {e}")

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

    # Executa sincronização se arquivo de config existir
    config_path = os.path.join(os.path.dirname(
        __file__), "data", "initial_config.json")
    if os.path.exists(config_path):
        logger.info(f"Iniciando sincronização a partir de {config_path}")
        manager.sync_from_json(config_path)
    else:
        logger.warning(
            f"Arquivo de configuração não encontrado: {config_path}")
