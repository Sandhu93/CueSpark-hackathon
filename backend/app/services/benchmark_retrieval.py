"""Benchmark profile embedding and retrieval service.

Embedding: chunks a profile's resume_text and stores vectors in embedding_chunks
           with chunk_type / owner_type = 'benchmark_profile'.

Retrieval: given a role_key and query text (typically the JD), returns the top_k
           most relevant benchmark profiles.  Role-key filtering is applied first,
           then vector similarity.  In mock mode profiles are ranked by
           quality_score so the service works without an OpenAI API key.
"""
from __future__ import annotations

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.benchmark_profile import BenchmarkProfile
from app.models.embedding_chunk import ChunkType, EmbeddingChunk
from app.services import llm
from app.services.embeddings import embed_and_store


def embed_benchmark_profile(
    profile: BenchmarkProfile,
    db: Session,
    *,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[EmbeddingChunk]:
    """Chunk and embed a benchmark profile's resume_text.

    Stores EmbeddingChunk rows with:
        chunk_type  = benchmark_profile
        owner_type  = benchmark_profile
        owner_id    = profile.id
        session_id  = None  (global; not tied to any interview session)

    Caller is responsible for committing the session.
    Returns the stored rows (empty list when resume_text is blank).
    """
    if not profile.resume_text or not profile.resume_text.strip():
        logger.debug(
            "benchmark_retrieval: no resume_text for profile_id={} — skipping",
            profile.id,
        )
        return []

    rows = embed_and_store(
        text=profile.resume_text,
        chunk_type=ChunkType.BENCHMARK_PROFILE.value,
        session_id=None,
        owner_type="benchmark_profile",
        owner_id=profile.id,
        db=db,
        chunk_size=chunk_size,
        overlap=overlap,
    )
    logger.info(
        "benchmark_retrieval: embedded {} chunk(s) for profile_id={}",
        len(rows),
        profile.id,
    )
    return rows


def retrieve_benchmark_profiles(
    role_key: str | None,
    query_text: str,
    db: Session,
    *,
    top_k: int = 5,
) -> list[BenchmarkProfile]:
    """Return the top_k benchmark profiles most relevant to role_key and query_text.

    Strategy:
      1. Filter benchmark_profiles by role_key when provided.
      2. Mock mode or blank query → rank candidates by quality_score (no DB
         vector query; no OpenAI call needed).
      3. Real mode → embed query_text, rank by cosine distance to the nearest
         benchmark chunk.  Falls back to quality_score if no chunks exist yet.
    """
    # ── Step 1: candidate profiles (role-key filter) ──────────────────────────
    stmt = select(BenchmarkProfile)
    if role_key:
        stmt = stmt.where(BenchmarkProfile.role_key == role_key)
    candidates: list[BenchmarkProfile] = list(db.execute(stmt).scalars().all())

    if not candidates:
        logger.info(
            "benchmark_retrieval: no profiles found for role_key={}",
            role_key,
        )
        return []

    # ── Step 2: mock mode — quality_score ranking ─────────────────────────────
    if settings.ai_mock_mode or not query_text.strip():
        ranked = sorted(candidates, key=lambda p: p.quality_score or 0.0, reverse=True)
        logger.info(
            "benchmark_retrieval: mock mode — returning {} of {} candidate(s) by quality_score",
            min(top_k, len(ranked)),
            len(ranked),
        )
        return ranked[:top_k]

    # ── Step 3: real mode — vector similarity ─────────────────────────────────
    candidate_ids = [p.id for p in candidates]
    query_vector = llm.embed([query_text])[0]

    chunk_stmt = (
        select(EmbeddingChunk.owner_id)
        .where(
            EmbeddingChunk.chunk_type == ChunkType.BENCHMARK_PROFILE.value,
            EmbeddingChunk.owner_id.in_(candidate_ids),
        )
        .order_by(EmbeddingChunk.embedding.cosine_distance(query_vector))
        .limit(top_k * 10)  # extra rows to allow deduplication by profile
    )
    chunk_rows = db.execute(chunk_stmt).all()

    seen: set[str] = set()
    top_ids: list[str] = []
    for (owner_id,) in chunk_rows:
        if owner_id and owner_id not in seen:
            seen.add(owner_id)
            top_ids.append(owner_id)
            if len(top_ids) >= top_k:
                break

    if not top_ids:
        # Profiles exist but haven't been embedded yet — fall back gracefully
        logger.warning(
            "benchmark_retrieval: no embedding chunks found for role_key={} "
            "— falling back to quality_score ranking",
            role_key,
        )
        ranked = sorted(candidates, key=lambda p: p.quality_score or 0.0, reverse=True)
        return ranked[:top_k]

    profile_map = {p.id: p for p in candidates}
    result = [profile_map[pid] for pid in top_ids if pid in profile_map]
    logger.info(
        "benchmark_retrieval: returning {} profile(s) by vector similarity for role_key={}",
        len(result),
        role_key,
    )
    return result
