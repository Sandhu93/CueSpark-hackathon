from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base

EMBEDDING_DIMENSIONS = 1536


class ChunkType(str, Enum):
    JD = "jd"
    RESUME = "resume"
    BENCHMARK_PROFILE = "benchmark_profile"
    ANSWER = "answer"
    RUBRIC = "rubric"
    QUESTION_BANK = "question_bank"


class EmbeddingChunk(Base):
    __tablename__ = "embedding_chunks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # Nullable: benchmark profile chunks are not tied to a session
    session_id: Mapped[str | None] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=True, index=True
    )
    owner_type: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    owner_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    chunk_type: Mapped[str] = mapped_column(String, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIMENSIONS))
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
