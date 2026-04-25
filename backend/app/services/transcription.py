from __future__ import annotations

from io import BytesIO

from loguru import logger

from app.core.config import settings


def transcribe_audio(
    audio_bytes: bytes,
    *,
    filename: str = "answer.webm",
    content_type: str = "audio/webm",
) -> str:
    if settings.ai_mock_mode or not settings.openai_api_key:
        logger.info("transcription: mock mode returning deterministic transcript")
        return (
            "I owned a backend reliability improvement where we reduced latency, added "
            "monitoring, and followed up with clearer operational ownership."
        )

    import openai

    client = openai.OpenAI(api_key=settings.openai_api_key)
    audio_file = BytesIO(audio_bytes)
    audio_file.name = filename
    response = client.audio.transcriptions.create(
        model=settings.openai_transcribe_model,
        file=audio_file,
    )
    transcript = getattr(response, "text", "")
    logger.info(
        "transcription: transcribed {} bytes with model {} content_type={}",
        len(audio_bytes),
        settings.openai_transcribe_model,
        content_type,
    )
    return transcript
