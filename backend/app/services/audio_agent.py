from __future__ import annotations

from app.schemas.answer import AudioAgentResult
from app.services.communication_analysis import analyze_communication_signals
from app.services.transcription import transcribe_audio


def process_audio_answer(
    audio_bytes: bytes,
    *,
    filename: str = "answer.webm",
    content_type: str = "audio/webm",
    duration_seconds: float | None = None,
) -> AudioAgentResult:
    transcript = transcribe_audio(
        audio_bytes,
        filename=filename,
        content_type=content_type,
    )
    return analyze_communication_signals(
        transcript,
        duration_seconds=duration_seconds,
    )
