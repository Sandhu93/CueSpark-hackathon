from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.redis_client import default_queue
from app.models.job import Job, JobStatus
from app.schemas.common import JobCreate, JobOut

router = APIRouter()

# Map of kind -> dotted path to the task function the worker should run.
# Add new task kinds here as you build features.
TASK_REGISTRY: dict[str, str] = {
    "dummy": "app.tasks.dummy.run",
    "prepare_session": "app.tasks.prepare_session.run",
    "process_audio_answer": "app.tasks.process_audio_answer.run",
    "analyze_text_answer": "app.tasks.analyze_text_answer.run",
    "analyze_code_answer": "app.tasks.analyze_code_answer.run",
    "analyze_video_signals": "app.tasks.analyze_video_signals.run",
    "analyze_benchmark_gap_coverage": "app.tasks.analyze_benchmark_gap_coverage.run",
    "evaluate_answer": "app.tasks.evaluate_answer.run",
    "generate_report": "app.tasks.generate_report.run",
    # "transcribe": "app.tasks.transcribe.run",
    # "score_answer": "app.tasks.score_answer.run",
}


@router.post("", response_model=JobOut)
async def create_job(payload: JobCreate, db: AsyncSession = Depends(get_db)) -> Job:
    if payload.kind not in TASK_REGISTRY:
        raise HTTPException(400, f"Unknown job kind: {payload.kind}")

    job = Job(kind=payload.kind, status=JobStatus.QUEUED.value, input=payload.input)
    db.add(job)
    await db.commit()
    await db.refresh(job)

    default_queue.enqueue(TASK_REGISTRY[payload.kind], job.id, job_id=job.id)
    return job


@router.get("/{job_id}", response_model=JobOut)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)) -> Job:
    job = await db.get(Job, job_id)
    if job is None:
        raise HTTPException(404, "Job not found")
    return job
