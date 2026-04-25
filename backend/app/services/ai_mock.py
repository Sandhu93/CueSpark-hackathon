from __future__ import annotations


MOCK_EMBEDDING_DIMENSIONS = 1536


def mock_text_response(prompt: str, *, prefix: str = "[mock]") -> str:
    return f"{prefix} {prompt}".strip()


def mock_embedding(count: int, *, dimensions: int = MOCK_EMBEDDING_DIMENSIONS) -> list[list[float]]:
    return [[0.0] * dimensions for _ in range(count)]
