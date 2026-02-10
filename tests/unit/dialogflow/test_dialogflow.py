from unittest.mock import patch

import pytest

from src.dialogflow.manager import DialogflowManager


@pytest.fixture
def mock_dialogflow():
    with patch("src.dialogflow.manager.dialogflow") as mock:
        # Configure the mock to behave like the real module structure
        mock.EntityType.Kind.KIND_MAP = 1
        mock.Intent.WebhookState.WEBHOOK_STATE_UNSPECIFIED = 0
        yield mock


def test_manager_init(mock_dialogflow):
    manager = DialogflowManager("test-project")
    assert manager.project_id == "test-project"
    mock_dialogflow.IntentsClient.assert_called_once()


def test_create_intent(mock_dialogflow):
    manager = DialogflowManager("test-project")

    # We need to access the client instance that was created during init
    mock_intents_client = manager.intents_client

    intent_data = {
        "display_name": "Test Intent",
        "training_phrases": ["Hello"],
        "messages": [{"text": ["Hi"]}],
    }

    manager.create_intent(intent_data)

    # Verify Intent constructor was called correctly
    mock_dialogflow.Intent.assert_called_once()
    intent_ctor_args = mock_dialogflow.Intent.call_args
    assert intent_ctor_args[1]["display_name"] == "Test Intent"

    # Verify client create call
    mock_intents_client.create_intent.assert_called_once()
    call_args = mock_intents_client.create_intent.call_args
    assert call_args[1]["parent"] == "projects/test-project/agent"
    # The intent passed to create_intent should be the return value of the constructor
    assert call_args[1]["intent"] == mock_dialogflow.Intent.return_value


def test_create_entity(mock_dialogflow):
    manager = DialogflowManager("test-project")
    mock_entity_client = manager.entity_types_client

    # Mock response with name for batch_create calls
    mock_entity_client.create_entity_type.return_value.name = (
        "projects/test/agent/entityTypes/123"
    )

    manager.create_entity_type(
        "Emotion", "KIND_MAP", [{"value": "happy", "synonyms": ["joy"]}]
    )

    mock_entity_client.create_entity_type.assert_called_once()
    mock_entity_client.batch_update_entities.assert_called_once()
