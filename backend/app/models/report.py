from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class HiringRecommendation(str, Enum):
    STRONG_YES = "strong_yes"
    YES = "yes"
    MAYBE = "maybe"
    NO = "no"


class InterviewReport(Base):
    __tablename__ = "interview_reports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True
    )
    readiness_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hiring_recommendation: Mapped[str | None] = mapped_column(String, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    benchmark_similarity_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    resume_competitiveness_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    evidence_strength_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    skill_gaps: Mapped[list] = mapped_column(JSONB, default=list)
    benchmark_gaps: Mapped[list] = mapped_column(JSONB, default=list)
    interview_risk_areas: Mapped[list] = mapped_column(JSONB, default=list)
    answer_feedback: Mapped[list] = mapped_column(JSONB, default=list)
    resume_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    improvement_plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
