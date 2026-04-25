from __future__ import annotations

from loguru import logger

from app.models.job import Job, JobStatus
from app.services.final_evaluation_orchestrator import evaluate_answer
from app.tasks._db import session_scope


def run(job_id: str) -> None:
    logger.info("evaluate_answer.run start job_id={}", job_id)

    with session_scope() as db:
        job = db.get(Job, job_id)
        if job is None:
            logger.error("evaluate_answer.run job {} not found", job_id)
            return
        job.status = JobStatus.RUNNING.value

    try:
        with session_scope() as db:
            job = db.get(Job, job_id)
            answer_id = str(job.input["answer_id"])
            result, row = evaluate_answer(db, answer_id)
            job.status = JobStatus.SUCCEEDED.value
            job.result = {"evaluation_id": row.id, **result.model_dump()}

        logger.info("evaluate_answer.run done job_id={}", job_id)

    except Exception as exc:
        logger.exception("evaluate_answer.run failed job_id={}", job_id)
        with session_scope() as db:
            job = db.get(Job, job_id)
            if job is not None:
                job.status = JobStatus.FAILED.value
                job.error = str(exc)
        raise
