from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

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
    provenance: dict[str, Any]
    response_mode: ResponseMode
    requires_audio: bool
    requires_video: bool
    requires_text: bool
    requires_code: bool
    tts_object_key: str | None
    tts_status: str | None
    created_at: datetime
    updated_at: datetime

    @field_validator("benchmark_gap_refs", mode="before")
    @classmethod
    def _default_benchmark_gap_refs(cls, value: object) -> object:
        return [] if value is None else value

    @field_validator("provenance", mode="before")
    @classmethod
    def _default_provenance(cls, value: object) -> object:
        return {} if value is None else value


class QuestionWithAudioRead(QuestionRead):
    tts_audio_url: str | None = None


class QuestionsResponse(BaseModel):
    questions: list[QuestionWithAudioRead]


class TtsResponse(BaseModel):
    question_id: str
    audio_url: str
