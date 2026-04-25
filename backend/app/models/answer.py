from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class CandidateAnswer(Base):
    __tablename__ = "candidate_answers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True
    )
    question_id: Mapped[str] = mapped_column(
        ForeignKey("interview_questions.id", ondelete="CASCADE"), index=True
    )
    audio_object_key: Mapped[str | None] = mapped_column(String, nullable=True)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    words_per_minute: Mapped[float | None] = mapped_column(Float, nullable=True)
    filler_word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    communication_metrics: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
