from __future__ import annotations

import io
import math
import struct
import wave

from app.core import storage
from app.models.question import InterviewQuestion


def ensure_question_tts(question: InterviewQuestion) -> str:
    if not question.tts_object_key:
        question.tts_object_key = f"audio/questions/{question.id}.wav"
        question.tts_status = "ready"
        storage.put_object(
            question.tts_object_key,
            _mock_wav_bytes(),
            content_type="audio/wav",
        )
    elif not question.tts_status:
        question.tts_status = "ready"
    return storage.presigned_get_url(question.tts_object_key)


def question_tts_url(question: InterviewQuestion) -> str | None:
    if not question.tts_object_key:
        return None
    return storage.presigned_get_url(question.tts_object_key)


def _mock_wav_bytes() -> bytes:
    sample_rate = 16000
    duration_seconds = 0.35
    frequency = 440.0
    frame_count = int(sample_rate * duration_seconds)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for index in range(frame_count):
            amplitude = int(1200 * math.sin(2 * math.pi * frequency * index / sample_rate))
            wav.writeframes(struct.pack("<h", amplitude))
    return buffer.getvalue()
