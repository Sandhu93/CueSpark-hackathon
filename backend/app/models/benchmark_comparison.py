from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class BenchmarkComparison(Base):
    __tablename__ = "benchmark_comparisons"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True
    )
    role_key: Mapped[str] = mapped_column(String, index=True)
    benchmark_profile_ids: Mapped[list] = mapped_column(JSONB, default=list)
    benchmark_similarity_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    resume_competitiveness_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    evidence_strength_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    missing_skills: Mapped[list] = mapped_column(JSONB, default=list)
    weak_skills: Mapped[list] = mapped_column(JSONB, default=list)
    missing_metrics: Mapped[list] = mapped_column(JSONB, default=list)
    weak_ownership_signals: Mapped[list] = mapped_column(JSONB, default=list)
    interview_risk_areas: Mapped[list] = mapped_column(JSONB, default=list)
    recommended_resume_fixes: Mapped[list] = mapped_column(JSONB, default=list)
    question_targets: Mapped[list] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
