from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.question import QuestionCategory, QuestionSource, ResponseMode


class GeneratedQuestion(BaseModel):
    """Structured output of the question generator — returned before DB persistence."""

    question_number: int
    category: str
    question_text: str
    expected_signal: str | None = None
    difficulty: str | None = None
    source: str = QuestionSource.BASE_PLAN.value
    benchmark_gap_refs: list[str] = Field(default_factory=list)
    why_this_was_asked: str | None = None
    response_mode: ResponseMode = ResponseMode.SPOKEN_ANSWER
    requires_audio: bool = True
    requires_video: bool = False
    requires_text: bool = False
    requires_code: bool = False


class QuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    question_number: int
    category: QuestionCategory
    question_text: str
    expected_signal: str | None
    difficulty: str | None
    source: QuestionSource
    benchmark_gap_refs: list[Any]
    why_this_was_asked: str | None
    response_mode: ResponseMode
    requires_audio: bool
    requires_video: bool
    requires_text: bool
    requires_code: bool
    tts_object_key: str | None
    created_at: datetime
