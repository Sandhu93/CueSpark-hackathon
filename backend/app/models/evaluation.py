from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


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
    jd_alignment_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    benchmark_gap_coverage_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    communication_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    overall_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    weaknesses: Mapped[str | None] = mapped_column(Text, nullable=True)
    strict_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    improved_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
