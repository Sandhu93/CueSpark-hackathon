"""
Centralized LLM access. Put your provider calls here so tasks/services
stay clean and you can swap providers in one place.
"""
from __future__ import annotations

from loguru import logger

from app.core.config import settings


def chat(messages: list[dict], model: str = "gpt-4o-mini", **kwargs) -> str:
    """
    Returns the assistant's text reply.

    Replace this stub with a real call when you wire up your provider.
    Example with the OpenAI SDK:

        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        resp = client.chat.completions.create(model=model, messages=messages, **kwargs)
        return resp.choices[0].message.content or ""
    """
    if not settings.openai_api_key and not settings.anthropic_api_key:
        logger.warning("No LLM API key set — returning stub response")
    return "[stub] " + (messages[-1]["content"] if messages else "")


def embed(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    """Stub for embeddings. Wire up once you need retrieval."""
    return [[0.0] * 8 for _ in texts]
