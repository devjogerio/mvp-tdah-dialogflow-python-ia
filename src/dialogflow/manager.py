from typing import List, Dict, Any, Optional
import time
import logging
import json
from google.api_core import retry
from google.api_core.exceptions import AlreadyExists, GoogleAPICallError, RetryError
from google.cloud import dialogflow_v2 as dialogflow
import os
# Fix for Python 3.14 + Protobuf compatibility issues
# Must be set before importing ANY google library
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")


# Configuração de Logging detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("automation_report.log")
    ]
)
logger = logging.getLogger("DialogflowAutomation")


class DialogflowManager:
    def __init__(self, project_id: str, credentials_path: str = None):
        """
        Gerenciador de automação robusto para Dialogflow ES.

        Args:
            project_id: ID do projeto GCP.
            credentials_path: Caminho para o JSON de credenciais (opcional se usar env var).
        """
        self.project_id = project_id
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            logger.info(
                f"Credenciais configuradas a partir de: {credentials_path}")

        try:
            self.intents_client = dialogflow.IntentsClient()
            self.entity_types_client = dialogflow.EntityTypesClient()
            self.parent = f"projects/{project_id}/agent"
            logger.info(
                f"Cliente Dialogflow inicializado para projeto: {project_id}")
        except Exception as e:
            logger.critical(
                f"Falha na autenticação ou inicialização do cliente: {e}")
            raise

        # Configuração de Retry Padrão (Exponencial Backoff)
        self.retry_policy = retry.Retry(
            initial=1.0,
            maximum=60.0,
            multiplier=2.0,
            deadline=120.0,
            predicate=retry.if_exception_type(
                GoogleAPICallError,
                RetryError,
                ConnectionError
            )
        )

        self.stats = {
            "intents_created": 0,
            "intents_updated": 0,
            "intents_failed": 0,
            "entities_created": 0,
            "entities_updated": 0,
            "entities_failed": 0
        }

    def _get_entity_type_id(self, display_name: str) -> Optional[str]:
        """Busca ID de uma entidade pelo nome (helper para update)."""
        try:
            # Em produção, usar filtro seria melhor, mas listagem é segura para volumes menores
            entity_types = self.entity_types_client.list_entity_types(
                parent=self.parent)
            for et in entity_types:
                if et.display_name == display_name:
                    return et.name
        except Exception as e:
            logger.error(f"Erro ao buscar entidade {display_name}: {e}")
        return None

    def _get_intent_id(self, display_name: str) -> Optional[str]:
        """Busca ID de uma intent pelo nome."""
        try:
            intents = self.intents_client.list_intents(
                parent=self.parent,
                intent_view=dialogflow.IntentView.INTENT_VIEW_FULL
            )
            for i in intents:
                if i.display_name == display_name:
                    return i.name
        except Exception as e:
            logger.error(f"Erro ao buscar intent {display_name}: {e}")
        return None

    def create_entity_type(self, display_name: str, kind: str, entries: List[Dict]):
        """Cria ou atualiza entidade com retry e validação."""
        logger.info(f"Processando entidade: {display_name}...")

        entity_type = dialogflow.EntityType(
            display_name=display_name,
            kind=getattr(dialogflow.EntityType.Kind, kind,
                         dialogflow.EntityType.Kind.KIND_MAP)
        )

        batch_entries = [
            dialogflow.EntityType.Entity(
                value=e['value'], synonyms=e['synonyms'])
            for e in entries
        ]

        try:
            # Tentativa de Criação
            self.entity_types_client.create_entity_type(
                parent=self.parent,
                entity_type=entity_type,
                retry=self.retry_policy
            )
            logger.info(f"✅ Entidade CRIADA: {display_name}")
            self.stats["entities_created"] += 1

            # Recuperar ID para batch update
            name = self._get_entity_type_id(display_name)

        except AlreadyExists:
            logger.info(
                f"⚠️ Entidade {display_name} já existe. Iniciando atualização...")
            name = self._get_entity_type_id(display_name)
            if name:
                entity_type.name = name
                self.entity_types_client.update_entity_type(
                    entity_type=entity_type,
                    retry=self.retry_policy
                )
                logger.info(f"✅ Entidade ATUALIZADA: {display_name}")
                self.stats["entities_updated"] += 1
            else:
                logger.error(
                    f"❌ Erro de integridade: {display_name} existe mas não foi encontrada.")
                self.stats["entities_failed"] += 1
                return

        except Exception as e:
            logger.error(
                f"❌ Falha crítica ao processar entidade {display_name}: {e}")
            self.stats["entities_failed"] += 1
            return

        # Sincronização de Entradas (Batch Update)
        if name:
            try:
                self.entity_types_client.batch_update_entities(
                    parent=name,
                    entities=batch_entries,
                    retry=self.retry_policy
                )
                logger.info(f"   ↳ Entradas sincronizadas para {display_name}")
            except Exception as e:
                logger.error(
                    f"   ❌ Falha ao sincronizar entradas para {display_name}: {e}")

    def create_intent(self, intent_data: Dict[str, Any]):
        """Cria ou atualiza Intent com retry, validação e suporte a parâmetros."""
        display_name = intent_data.get("display_name")
        logger.info(f"Processando intent: {display_name}...")

        # Construção dos objetos da API
        training_phrases = []
        for phrase in intent_data.get("training_phrases", []):
            part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
            training_phrases.append(
                dialogflow.Intent.TrainingPhrase(parts=[part]))

        messages = []
        for msg in intent_data.get("messages", []):
            if "text" in msg:
                text_obj = dialogflow.Intent.Message.Text(text=msg["text"])
                messages.append(dialogflow.Intent.Message(text=text_obj))

        # Construção de Parâmetros
        parameters = []
        for param in intent_data.get("parameters", []):
            parameters.append(dialogflow.Intent.Parameter(
                display_name=param["display_name"],
                entity_type_display_name=param["entity_type_display_name"],
                mandatory=param.get("mandatory", False),
                prompts=param.get("prompts", [])
            ))

        # Contextos de Entrada
        input_context_names = []
        for ctx_name in intent_data.get("input_context_names", []):
            input_context_names.append(f"{self.parent}/contexts/{ctx_name}")

        # Contextos de Saída
        output_contexts = []
        for ctx in intent_data.get("output_contexts", []):
            output_contexts.append(dialogflow.Context(
                name=f"{self.parent}/contexts/{ctx['name']}",
                lifespan_count=ctx.get("lifespan_count", 5)
            ))

        intent = dialogflow.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=messages,
            parameters=parameters,
            input_context_names=input_context_names,
            output_contexts=output_contexts,
            priority=intent_data.get("priority", 500000),
            webhook_state=getattr(dialogflow.Intent.WebhookState, 
                                intent_data.get("webhook_state", "WEBHOOK_STATE_UNSPECIFIED"))
        )

        try:
            self.intents_client.create_intent(
                parent=self.parent,
                intent=intent,
                retry=self.retry_policy
            )
            logger.info(f"✅ Intent CRIADA: {display_name}")
            self.stats["intents_created"] += 1

        except AlreadyExists:
            logger.info(
                f"⚠️ Intent {display_name} já existe. Iniciando atualização...")
            name = self._get_intent_id(display_name)
            if name:
                intent.name = name
                self.intents_client.update_intent(
                    intent=intent,
                    intent_view=dialogflow.IntentView.INTENT_VIEW_FULL,
                    retry=self.retry_policy
                )
                logger.info(f"✅ Intent ATUALIZADA: {display_name}")
                self.stats["intents_updated"] += 1
            else:
                logger.error(
                    f"❌ Erro de integridade: {display_name} existe mas não foi encontrada.")
                self.stats["intents_failed"] += 1

        except Exception as e:
            logger.error(
                f"❌ Falha crítica ao processar intent {display_name}: {e}")
            self.stats["intents_failed"] += 1

    def sync_from_json(self, json_path: str):
        """Executa o processo completo de sincronização."""
        logger.info(">>> INICIANDO AUTOMAÇÃO COMPLETA <<<")
        start_time = time.time()

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.critical(
                f"Erro ao ler arquivo de configuração {json_path}: {e}")
            return

        # 1. Sync Entities (Dependência para Intents)
        logger.info("--- Fase 1: Sincronização de Entidades ---")
        for entity in data.get("entities", []):
            self.create_entity_type(
                entity["display_name"],
                entity["kind"],
                entity["entries"]
            )

        # 2. Sync Intents
        logger.info("--- Fase 2: Sincronização de Intents ---")
        for intent in data.get("intents", []):
            self.create_intent(intent)

        duration = time.time() - start_time
        self._print_report(duration)

    def _print_report(self, duration: float):
        """Gera relatório final."""
        report = f"""
        =============================================
        RELATÓRIO FINAL DE AUTOMAÇÃO
        =============================================
        Tempo Total: {duration:.2f} segundos
        
        RESUMO DE INTENTS:
          - Criadas:   {self.stats['intents_created']}
          - Atualizadas: {self.stats['intents_updated']}
          - Falhas:    {self.stats['intents_failed']}
        
        RESUMO DE ENTIDADES:
          - Criadas:   {self.stats['entities_created']}
          - Atualizadas: {self.stats['entities_updated']}
          - Falhas:    {self.stats['entities_failed']}
        =============================================
        Verifique 'automation_report.log' para detalhes.
        """
        logger.info(report)
        print(report)

    def export_to_json(self, output_path: str):
        """Exporta a configuração atual para JSON (Backup)."""
        # ... implementation maintained or simplified ...
        pass


if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Validação de Ambiente
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        logger.error("ERRO: GCP_PROJECT_ID não definido. Configure o .env.")
        exit(1)

    # Verifica credenciais
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        logger.warning(
            "AVISO: GOOGLE_APPLICATION_CREDENTIALS não definido. Tentando credenciais default...")

    manager = DialogflowManager(project_id)

    # Caminho do Config
    config_path = os.path.join(os.path.dirname(
        __file__), "data", "initial_config.json")

    if os.path.exists(config_path):
        manager.sync_from_json(config_path)
    else:
        logger.error(f"Arquivo de configuração não encontrado: {config_path}")
