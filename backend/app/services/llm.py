"""
Centralized LLM access. Provider calls should live behind service modules so
tasks and routes do not depend on a specific AI SDK.
"""
from __future__ import annotations

from loguru import logger

from app.core.config import settings
from app.services.ai_mock import mock_embedding, mock_text_response


def chat(messages: list[dict], model: str | None = None, **kwargs) -> str:
    """
    Return a deterministic mock assistant reply.

    Real provider calls are intentionally not implemented in this foundation task.
    """
    selected_model = model or settings.openai_chat_model
    if settings.ai_mock_mode:
        logger.info("AI mock mode enabled; returning mock chat response for {}", selected_model)
        return mock_text_response(messages[-1]["content"] if messages else "")

    if not settings.openai_api_key and not settings.anthropic_api_key:
        logger.warning("No LLM API key set; returning mock chat response")
        return mock_text_response(messages[-1]["content"] if messages else "")

    logger.warning("Real AI calls are not implemented; returning mock chat response")
    return mock_text_response(messages[-1]["content"] if messages else "")


def embed(texts: list[str], model: str | None = None) -> list[list[float]]:
    """Return deterministic mock embeddings until a real embedding service is added."""
    selected_model = model or settings.openai_embedding_model
    if settings.ai_mock_mode:
        logger.info("AI mock mode enabled; returning mock embeddings for {}", selected_model)
    return mock_embedding(len(texts))
