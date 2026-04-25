from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class InterviewSessionStatus(str, Enum):
    DRAFT = "draft"
    PREPARING = "preparing"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    EVALUATING = "evaluating"
    REPORT_READY = "report_ready"
    COMPLETED = "completed"
    FAILED = "failed"


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role_title: Mapped[str | None] = mapped_column(String, nullable=True)
    role_key: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    company_name: Mapped[str | None] = mapped_column(String, nullable=True)
    job_description_text: Mapped[str] = mapped_column(Text)
    resume_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    match_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    benchmark_similarity_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    resume_competitiveness_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    evidence_strength_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String, default=InterviewSessionStatus.DRAFT.value, index=True
    )
    current_question_index: Mapped[int] = mapped_column(Integer, default=0)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    documents: Mapped[list["Document"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
