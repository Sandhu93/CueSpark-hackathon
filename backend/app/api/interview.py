from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.question import InterviewQuestion
from app.schemas.question import QuestionWithAudioRead, QuestionsResponse, TtsResponse
from app.services.question_audio import ensure_question_tts, question_tts_url

router = APIRouter()


@router.get("/sessions/{session_id}/questions", response_model=QuestionsResponse)
async def list_session_questions(
    session_id: str,
    db: AsyncSession = Depends(get_db),
) -> QuestionsResponse:
    rows = (
        await db.execute(
            select(InterviewQuestion)
            .where(InterviewQuestion.session_id == session_id)
            .order_by(InterviewQuestion.question_number.asc())
        )
    ).scalars().all()
    return QuestionsResponse(
        questions=[_question_with_audio(row) for row in rows],
    )


@router.post("/questions/{question_id}/tts", response_model=TtsResponse)
async def create_question_tts(
    question_id: str,
    db: AsyncSession = Depends(get_db),
) -> TtsResponse:
    question = await db.get(InterviewQuestion, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    audio_url = ensure_question_tts(question)
    await db.commit()
    await db.refresh(question)
    return TtsResponse(question_id=question.id, audio_url=audio_url)


@router.get("/questions/{question_id}/tts", response_model=TtsResponse)
async def get_question_tts(
    question_id: str,
    db: AsyncSession = Depends(get_db),
) -> TtsResponse:
    question = await db.get(InterviewQuestion, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    audio_url = question_tts_url(question)
    if audio_url is None:
        raise HTTPException(status_code=404, detail="Question audio not generated")
    return TtsResponse(question_id=question.id, audio_url=audio_url)


def _question_with_audio(question: InterviewQuestion) -> QuestionWithAudioRead:
    return QuestionWithAudioRead(
        **QuestionWithAudioRead.model_validate(question).model_dump(exclude={"tts_audio_url"}),
        tts_audio_url=question_tts_url(question),
    )
