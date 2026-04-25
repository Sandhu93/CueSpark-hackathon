from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.api.jobs import TASK_REGISTRY
from app.core.redis_client import default_queue
from app.models.job import Job, JobStatus
from app.schemas.session import (
    SessionCreate,
    SessionCreateResponse,
    SessionPrepareResponse,
    SessionRead,
)
from app.services.sessions import create_session, get_session

router = APIRouter()


@router.post("", response_model=SessionCreateResponse, status_code=201)
async def create_interview_session(
    payload: SessionCreate, db: AsyncSession = Depends(get_db)
) -> SessionCreateResponse:
    session = await create_session(db, payload)
    return SessionCreateResponse(session_id=session.id, status=session.status)


@router.get("/{session_id}", response_model=SessionRead)
async def read_interview_session(
    session_id: str, db: AsyncSession = Depends(get_db)
) -> SessionRead:
    session = await get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/{session_id}/prepare", response_model=SessionPrepareResponse)
async def prepare_interview_session(
    session_id: str, db: AsyncSession = Depends(get_db)
) -> SessionPrepareResponse:
    session = await get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    job = Job(
        kind="prepare_session",
        status=JobStatus.QUEUED.value,
        input={"session_id": session_id},
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    default_queue.enqueue(TASK_REGISTRY["prepare_session"], job.id, job_id=job.id)
    return SessionPrepareResponse(job_id=job.id, status=job.status)
