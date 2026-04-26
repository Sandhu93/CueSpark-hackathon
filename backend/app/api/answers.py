from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import storage
from app.core.config import settings
from app.core.db import get_db
from app.core.redis_client import default_queue
from app.models.job import Job, JobStatus
from app.models.agent_result import AgentResult
from app.models.answer import AnswerProcessingStatus, AnswerTranscriptionStatus, CandidateAnswer
from app.models.evaluation import AnswerEvaluation
from app.models.question import InterviewQuestion, ResponseMode
from app.schemas.agent_results import AgentResultRead
from app.schemas.answer import AgentResultsResponse, AnswerDetailRead, AnswerRead, AnswerSubmitResponse
from app.schemas.evaluation import EvaluationRead

router = APIRouter()

SUPPORTED_AUDIO_CONTENT_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/mp4",
    "audio/wav",
    "audio/wave",
    "audio/x-wav",
    "audio/webm",
    "audio/ogg",
    "audio/x-m4a",
    "video/webm",
}
SUPPORTED_AUDIO_EXTENSIONS = {"mp3", "mp4", "m4a", "wav", "wave", "webm", "ogg"}


@router.post("/questions/{question_id}/answers", response_model=AnswerSubmitResponse)
async def submit_answer(
    question_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> AnswerSubmitResponse:
    question = await db.get(InterviewQuestion, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    payload, audio = await _parse_payload(request)
    answer_mode = _parse_answer_mode(payload.get("answer_mode"), question)
    _validate_answer_against_question(payload, audio, answer_mode, question)

    audio_object_key = None
    if audio is not None:
        if not _is_supported_audio_file(audio):
            raise HTTPException(status_code=400, detail="Unsupported audio file type")
        ext = Path(audio.filename or "").suffix.lstrip(".")
        body = await audio.read()
        if len(body) > settings.max_audio_upload_bytes:
            raise HTTPException(status_code=413, detail="Audio file is too large")
        audio_object_key = storage.new_object_key(prefix="answers/audio", ext=ext)
        storage.put_object(
            audio_object_key,
            body,
            content_type=audio.content_type or "application/octet-stream",
        )

    answer = CandidateAnswer(
        session_id=question.session_id,
        question_id=question.id,
        audio_object_key=audio_object_key,
        answer_mode=answer_mode.value,
        transcription_status=(
            AnswerTranscriptionStatus.PENDING.value
            if audio_object_key
            else AnswerTranscriptionStatus.NOT_REQUIRED.value
        ),
        processing_status=AnswerProcessingStatus.QUEUED.value,
        text_answer=_clean_optional_text(payload.get("text_answer")),
        code_answer=_clean_optional_text(payload.get("code_answer")),
        code_language=_clean_optional_text(payload.get("code_language")),
        visual_signal_metadata=_parse_visual_signal_metadata(
            payload.get("visual_signal_metadata")
        ),
    )
    db.add(answer)
    await db.commit()
    await db.refresh(answer)

    job = Job(
        kind="process_answer_pipeline",
        status=JobStatus.QUEUED.value,
        input={"answer_id": answer.id},
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    default_queue.enqueue(
        "app.tasks.process_answer_pipeline.run",
        job.id,
        job_id=job.id,
    )

    return AnswerSubmitResponse(answer_id=answer.id, processing_status=answer.processing_status)


@router.get("/answers/{answer_id}", response_model=AnswerDetailRead)
async def get_answer(
    answer_id: str,
    db: AsyncSession = Depends(get_db),
) -> AnswerDetailRead:
    answer = await db.get(CandidateAnswer, answer_id)
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")

    agent_results = (
        await db.execute(
            select(AgentResult)
            .where(AgentResult.answer_id == answer_id)
            .order_by(AgentResult.created_at.asc())
        )
    ).scalars().all()
    evaluation = (
        await db.execute(
            select(AnswerEvaluation)
            .where(AnswerEvaluation.answer_id == answer_id)
            .order_by(AnswerEvaluation.created_at.desc())
        )
    ).scalars().first()

    return AnswerDetailRead(
        **AnswerRead.model_validate(answer).model_dump(),
        agent_results=[AgentResultRead.model_validate(row) for row in agent_results],
        evaluation=EvaluationRead.model_validate(evaluation) if evaluation else None,
    )


@router.get("/answers/{answer_id}/agent-results", response_model=AgentResultsResponse)
async def get_answer_agent_results(
    answer_id: str,
    db: AsyncSession = Depends(get_db),
) -> AgentResultsResponse:
    answer = await db.get(CandidateAnswer, answer_id)
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    agent_results = (
        await db.execute(
            select(AgentResult)
            .where(AgentResult.answer_id == answer_id)
            .order_by(AgentResult.created_at.asc())
        )
    ).scalars().all()
    return AgentResultsResponse(
        answer_id=answer_id,
        agent_results=[AgentResultRead.model_validate(row) for row in agent_results],
    )


async def _parse_payload(request: Request) -> tuple[dict[str, Any], UploadFile | None]:
    content_type = request.headers.get("content-type", "")
    if content_type.startswith("multipart/form-data"):
        form = await request.form()
        audio_value = form.get("audio")
        audio = audio_value if _looks_like_upload_file(audio_value) else None
        payload = {
            key: value
            for key, value in form.multi_items()
            if key != "audio" and isinstance(value, str)
        }
        return payload, audio

    if content_type.startswith("application/json"):
        body = await request.json()
        if not isinstance(body, dict):
            raise HTTPException(status_code=422, detail="JSON answer payload must be an object")
        return body, None

    raise HTTPException(
        status_code=415,
        detail="Use application/json or multipart/form-data for answer submission",
    )


def _parse_answer_mode(value: Any, question: InterviewQuestion) -> ResponseMode:
    raw_value = str(value or question.response_mode or ResponseMode.SPOKEN_ANSWER.value)
    try:
        return ResponseMode(raw_value)
    except ValueError:
        raise HTTPException(status_code=422, detail=f"Unsupported answer mode: {raw_value}")


def _validate_answer_against_question(
    payload: dict[str, Any],
    audio: UploadFile | None,
    answer_mode: ResponseMode,
    question: InterviewQuestion,
) -> None:
    expected_mode = ResponseMode(question.response_mode or ResponseMode.SPOKEN_ANSWER.value)
    if answer_mode != expected_mode:
        raise HTTPException(
            status_code=422,
            detail=f"Answer mode must match question response mode: {expected_mode.value}",
        )

    requires_audio = bool(question.requires_audio) or answer_mode == ResponseMode.SPOKEN_ANSWER
    requires_text = bool(question.requires_text) or answer_mode == ResponseMode.WRITTEN_ANSWER
    requires_code = bool(question.requires_code) or answer_mode == ResponseMode.CODE_ANSWER

    if requires_audio and audio is None:
        raise HTTPException(status_code=422, detail="Audio answer is required")
    if requires_text and not _clean_optional_text(payload.get("text_answer")):
        raise HTTPException(status_code=422, detail="Text answer is required")
    if requires_code:
        if not _clean_optional_text(payload.get("code_answer")):
            raise HTTPException(status_code=422, detail="Code answer is required")
        if not _clean_optional_text(payload.get("code_language")):
            raise HTTPException(status_code=422, detail="Code language is required")


def _is_supported_audio_file(file: UploadFile) -> bool:
    extension = Path(file.filename or "").suffix.lower().lstrip(".")
    return (
        (file.content_type or "").lower() in SUPPORTED_AUDIO_CONTENT_TYPES
        and extension in SUPPORTED_AUDIO_EXTENSIONS
    )


def _looks_like_upload_file(value: Any) -> bool:
    return all(hasattr(value, attr) for attr in ("filename", "content_type", "read"))


def _clean_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _parse_visual_signal_metadata(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return {}
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=422,
                detail="visual_signal_metadata must be a JSON object",
            )
        if isinstance(parsed, dict):
            return parsed
    raise HTTPException(status_code=422, detail="visual_signal_metadata must be a JSON object")
