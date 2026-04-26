from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.jobs import TASK_REGISTRY
from app.core.db import get_db
from app.core.redis_client import default_queue
from app.models.job import Job, JobStatus
from app.models.report import InterviewReport
from app.models.session import InterviewSession
from app.schemas.common import JobOut
from app.schemas.report import ReportRead

router = APIRouter()


@router.post("/sessions/{session_id}/report", response_model=JobOut)
async def create_session_report(
    session_id: str,
    db: AsyncSession = Depends(get_db),
) -> Job:
    session = await db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    job = Job(
        kind="generate_report",
        status=JobStatus.QUEUED.value,
        input={"session_id": session_id},
        result={},
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    default_queue.enqueue(TASK_REGISTRY["generate_report"], job.id, job_id=job.id)
    return job


@router.get("/sessions/{session_id}/report", response_model=ReportRead)
async def get_session_report(
    session_id: str,
    db: AsyncSession = Depends(get_db),
) -> InterviewReport:
    report = (
        await db.execute(
            select(InterviewReport)
            .where(InterviewReport.session_id == session_id)
            .order_by(InterviewReport.created_at.desc())
        )
    ).scalars().first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
