from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.core.time import utc_now


class AgentType(str, Enum):
    AUDIO = "audio"
    VIDEO_SIGNAL = "video_signal"
    TEXT_ANSWER = "text_answer"
    CODE_EVALUATION = "code_evaluation"
    BENCHMARK_GAP = "benchmark_gap"
    FINAL_ORCHESTRATOR = "final_orchestrator"


class AgentResultStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class AgentResult(Base):
    __tablename__ = "agent_results"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    answer_id: Mapped[str] = mapped_column(
        ForeignKey("candidate_answers.id", ondelete="CASCADE"), index=True
    )
    agent_type: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(
        String, default=AgentResultStatus.PENDING.value, index=True
    )
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now
    )
