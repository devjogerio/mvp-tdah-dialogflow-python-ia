from unittest.mock import MagicMock, patch

import pytest
from google.api_core.exceptions import AlreadyExists

from src.dialogflow.manager import DialogflowManager


@pytest.fixture
def manager():
    with patch("src.dialogflow.manager.dialogflow"):
        mgr = DialogflowManager("test-project")
        mgr.intents_client = MagicMock()
        mgr.entity_types_client = MagicMock()
        return mgr


def test_create_intent_new(manager):
    """Testa criação de nova intent"""
    intent_data = {
        "display_name": "TestIntent",
        "training_phrases": ["oi"],
        "messages": [{"text": "olá"}],
    }

    manager.create_intent(intent_data)

    manager.intents_client.create_intent.assert_called_once()
    manager.intents_client.update_intent.assert_not_called()


def test_create_intent_exists_update(manager):
    """Testa atualização de intent existente (Upsert)"""
    intent_data = {
        "display_name": "TestIntent",
        "training_phrases": ["oi"],
        "messages": [{"text": "olá"}],
    }

    # Simula erro AlreadyExists na criação
    manager.intents_client.create_intent.side_effect = AlreadyExists("Exists")

    # Mock da lista de intents para encontrar o ID
    mock_intent = MagicMock()
    mock_intent.display_name = "TestIntent"
    mock_intent.name = "projects/test-project/agent/intents/123"
    manager.intents_client.list_intents.return_value = [mock_intent]

    manager.create_intent(intent_data)

    # Verifica se tentou criar, falhou, listou e atualizou
    manager.intents_client.create_intent.assert_called_once()
    manager.intents_client.list_intents.assert_called_once()
    manager.intents_client.update_intent.assert_called_once()


def test_create_entity_exists_update(manager):
    """Testa atualização de entidade existente (Upsert)"""
    entity_data = [{"value": "val", "synonyms": ["s"]}]

    # Simula erro AlreadyExists
    manager.entity_types_client.create_entity_type.side_effect = AlreadyExists("Exists")

    # Mock da lista
    mock_ent = MagicMock()
    mock_ent.display_name = "TestEntity"
    mock_ent.name = "projects/test-project/agent/entityTypes/456"
    manager.entity_types_client.list_entity_types.return_value = [mock_ent]

    # Mock da resposta do update para ter .name
    manager.entity_types_client.update_entity_type.return_value = mock_ent

    manager.create_entity_type("TestEntity", "KIND_MAP", entity_data)

    manager.entity_types_client.update_entity_type.assert_called_once()
    manager.entity_types_client.batch_update_entities.assert_called_once()
