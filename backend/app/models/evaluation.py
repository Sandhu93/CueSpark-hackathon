from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.core.time import utc_now


class AnswerEvaluation(Base):
    __tablename__ = "answer_evaluations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    answer_id: Mapped[str] = mapped_column(
        ForeignKey("candidate_answers.id", ondelete="CASCADE"), index=True
    )
    relevance_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    role_depth_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    evidence_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    clarity_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    structure_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    jd_alignment_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    benchmark_gap_coverage_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    communication_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    communication_signal_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    code_quality_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    written_answer_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    visual_signal_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    overall_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    weaknesses: Mapped[str | None] = mapped_column(Text, nullable=True)
    strict_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    improved_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    red_flags: Mapped[list] = mapped_column(JSONB, default=list)
    modality_breakdown: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)
