from __future__ import annotations

from loguru import logger
from sqlalchemy.orm import Session

from app.models.embedding_chunk import EmbeddingChunk
from app.services import llm
from app.services.chunking import chunk_text


def embed_and_store(
    *,
    text: str,
    chunk_type: str,
    db: Session,
    session_id: str | None = None,
    owner_type: str | None = None,
    owner_id: str | None = None,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[EmbeddingChunk]:
    """
    Chunk text, generate embeddings, and persist EmbeddingChunk rows.

    Accepts any chunk_type defined in the data contract (jd, resume,
    benchmark_profile, answer, rubric, question_bank).  Benchmark profile
    chunks pass session_id=None and supply owner_type/owner_id instead.

    Returns the list of unsaved ORM objects (caller must commit).
    """
    chunks = chunk_text(text, chunk_type, chunk_size=chunk_size, overlap=overlap)
    if not chunks:
        logger.debug("embed_and_store: no chunks produced for chunk_type={}", chunk_type)
        return []

    contents = [c.content for c in chunks]
    vectors = llm.embed(contents)

    rows: list[EmbeddingChunk] = []
    for chunk, vector in zip(chunks, vectors):
        row = EmbeddingChunk(
            session_id=session_id,
            owner_type=owner_type,
            owner_id=owner_id,
            chunk_type=chunk_type,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            embedding=vector,
        )
        db.add(row)
        rows.append(row)

    logger.info(
        "embed_and_store: stored {} chunk(s) for chunk_type={} session_id={}",
        len(rows),
        chunk_type,
        session_id,
    )
    return rows
