from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.core.time import utc_now


class BenchmarkSourceType(str, Enum):
    CURATED = "curated"
    PUBLIC = "public"
    SYNTHETIC = "synthetic"


class BenchmarkProfile(Base):
    __tablename__ = "benchmark_profiles"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role_key: Mapped[str] = mapped_column(String, index=True)
    role_title: Mapped[str] = mapped_column(String)
    seniority_level: Mapped[str] = mapped_column(String, index=True)
    domain: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    profile_name: Mapped[str] = mapped_column(String)
    resume_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[list] = mapped_column(JSONB, default=list)
    tools: Mapped[list] = mapped_column(JSONB, default=list)
    project_signals: Mapped[list] = mapped_column(JSONB, default=list)
    impact_signals: Mapped[list] = mapped_column(JSONB, default=list)
    ownership_signals: Mapped[list] = mapped_column(JSONB, default=list)
    source_type: Mapped[str] = mapped_column(
        String, default=BenchmarkSourceType.CURATED.value, index=True
    )
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    is_curated: Mapped[bool] = mapped_column(Boolean, default=False)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)
