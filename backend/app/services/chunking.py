from __future__ import annotations

from dataclasses import dataclass

_DEFAULT_CHUNK_SIZE = 500
_DEFAULT_OVERLAP = 50


@dataclass
class ChunkResult:
    chunk_index: int
    chunk_type: str
    content: str


def chunk_text(
    text: str,
    chunk_type: str,
    *,
    chunk_size: int = _DEFAULT_CHUNK_SIZE,
    overlap: int = _DEFAULT_OVERLAP,
) -> list[ChunkResult]:
    """
    Split text into overlapping chunks of approximately chunk_size characters.

    Works on whole words so boundaries never fall inside a word.
    Every word appears in at least one chunk (no text loss).
    Returns an empty list for blank input.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    words = text.split()
    if not words:
        return []

    chunks: list[ChunkResult] = []
    chunk_index = 0
    word_start = 0

    while word_start < len(words):
        # Accumulate words until adding the next word would exceed chunk_size
        chunk_words: list[str] = []
        char_count = 0
        i = word_start

        while i < len(words):
            word = words[i]
            sep = 1 if chunk_words else 0
            if char_count + sep + len(word) > chunk_size and chunk_words:
                break
            chunk_words.append(word)
            char_count += sep + len(word)
            i += 1

        chunks.append(
            ChunkResult(
                chunk_index=chunk_index,
                chunk_type=chunk_type,
                content=" ".join(chunk_words),
            )
        )
        chunk_index += 1

        if i >= len(words):
            break  # all words consumed

        # Advance word_start: skip words until we have consumed (chunk_size - overlap) chars
        skip_target = chunk_size - overlap
        consumed = 0
        j = word_start
        while j < i and consumed < skip_target:
            sep = 1 if j > word_start else 0
            consumed += sep + len(words[j])
            j += 1

        word_start = max(j, word_start + 1)  # always make forward progress

    return chunks
