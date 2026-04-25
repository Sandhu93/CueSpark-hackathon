from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class QuestionCategory(str, Enum):
    TECHNICAL = "technical"
    PROJECT_EXPERIENCE = "project_experience"
    BEHAVIORAL = "behavioral"
    HR = "hr"
    RESUME_GAP = "resume_gap"
    JD_SKILL_VALIDATION = "jd_skill_validation"
    BENCHMARK_GAP_VALIDATION = "benchmark_gap_validation"


class QuestionSource(str, Enum):
    BASE_PLAN = "base_plan"
    ADAPTIVE_FOLLOWUP = "adaptive_followup"
    BENCHMARK_GAP = "benchmark_gap"


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True
    )
    question_number: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String, index=True)
    question_text: Mapped[str] = mapped_column(Text)
    expected_signal: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, default=QuestionSource.BASE_PLAN.value)
    # References to benchmark gap(s) this question tests, populated by benchmark engine
    benchmark_gap_refs: Mapped[list] = mapped_column(JSONB, default=list)
    # Human-readable annotation explaining why this question was chosen
    why_this_was_asked: Mapped[str | None] = mapped_column(Text, nullable=True)
    tts_object_key: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
