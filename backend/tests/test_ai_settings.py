from app.core.config import Settings
from app.services.ai_mock import mock_embedding, mock_text_response


def test_ai_settings_default_to_safe_mock_mode():
    settings = Settings(_env_file=None)

    assert settings.ai_provider == "openai"
    assert settings.ai_mock_mode is True
    assert settings.openai_chat_model == "gpt-4o-mini"
    assert settings.openai_tts_model == "gpt-4o-mini-tts"
    assert settings.openai_tts_voice == "marin"
    assert settings.openai_transcribe_model == "gpt-4o-transcribe"
    assert settings.openai_embedding_model == "text-embedding-3-small"


def test_ai_mock_helpers_are_deterministic():
    assert mock_text_response("hello") == "[mock] hello"
    assert mock_embedding(2) == [[0.0] * 1536, [0.0] * 1536]
