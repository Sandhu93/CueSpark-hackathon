from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.question import ResponseMode


class AudioAgentResult(BaseModel):
    transcript: str
    word_count: int
    duration_seconds: float | None
    words_per_minute: float | None
    filler_word_count: int
    filler_words: list[str]
    hesitation_markers: list[str]
    structure_observations: list[str]
    communication_signal_score: int


class AnswerSubmitResponse(BaseModel):
    answer_id: str
    processing_status: str


class AnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    question_id: str
    audio_object_key: str | None
    answer_mode: ResponseMode
    transcript: str | None
    text_answer: str | None
    code_answer: str | None
    code_language: str | None
    duration_seconds: float | None
    word_count: int | None
    words_per_minute: float | None
    filler_word_count: int | None
    communication_metrics: dict[str, Any]
    visual_signal_metadata: dict[str, Any]
    created_at: datetime
