from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    question_id: str
    audio_object_key: str | None
    transcript: str | None
    duration_seconds: float | None
    word_count: int | None
    words_per_minute: float | None
    filler_word_count: int | None
    communication_metrics: dict[str, Any]
    created_at: datetime
