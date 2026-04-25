from __future__ import annotations

from typing import Any

from loguru import logger

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.job import Job, JobStatus
from app.services.video_signal_agent import SAFE_VISUAL_SIGNAL_LABELS, analyze_video_signals
from app.tasks._db import session_scope


def run(job_id: str) -> None:
    logger.info("analyze_video_signals.run start job_id={}", job_id)

    with session_scope() as db:
        job = db.get(Job, job_id)
        if job is None:
            logger.error("analyze_video_signals.run job {} not found", job_id)
            return
        job.status = JobStatus.RUNNING.value

    try:
        with session_scope() as db:
            job = db.get(Job, job_id)
            answer_id = str(job.input["answer_id"])
            answer = db.get(CandidateAnswer, answer_id)
            if answer is None:
                raise ValueError(f"Candidate answer not found: {answer_id}")

            metadata = _metadata_from_job_input(job.input)
            if metadata:
                answer.visual_signal_metadata = metadata
            result = analyze_video_signals(answer=answer, metadata=metadata)
            row = store_video_signal_agent_result(db, answer_id=answer.id, result=result)
            answer.visual_signal_metadata = {
                **(answer.visual_signal_metadata or {}),
                "visual_signal_summary": result.model_dump(),
                "safe_signal_labels": SAFE_VISUAL_SIGNAL_LABELS,
            }
            job.status = JobStatus.SUCCEEDED.value
            job.result = {"agent_result_id": row.id, **result.model_dump()}

        logger.info("analyze_video_signals.run done job_id={}", job_id)

    except Exception as exc:
        logger.exception("analyze_video_signals.run failed job_id={}", job_id)
        with session_scope() as db:
            job = db.get(Job, job_id)
            if job is not None:
                job.status = JobStatus.FAILED.value
                job.error = str(exc)
        raise


def store_video_signal_agent_result(db, *, answer_id: str, result) -> AgentResult:
    row = AgentResult(
        answer_id=answer_id,
        agent_type=AgentType.VIDEO_SIGNAL.value,
        status=AgentResultStatus.SUCCEEDED.value,
        score=float(result.visual_signal_score),
        payload=result.model_dump(),
    )
    db.add(row)
    return row


def _metadata_from_job_input(job_input: dict[str, Any]) -> dict[str, Any]:
    value = job_input.get("visual_signal_metadata")
    return value if isinstance(value, dict) else {}
