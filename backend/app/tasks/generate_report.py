from __future__ import annotations

from loguru import logger

from app.models.job import Job, JobStatus
from app.services.report_generator import generate_multimodal_readiness_report
from app.tasks._db import session_scope


def run(job_id: str) -> None:
    logger.info("generate_report.run start job_id={}", job_id)

    with session_scope() as db:
        job = db.get(Job, job_id)
        if job is None:
            logger.error("generate_report.run job {} not found", job_id)
            return
        job.status = JobStatus.RUNNING.value

    try:
        with session_scope() as db:
            job = db.get(Job, job_id)
            session_id = str(job.input["session_id"])
            report = generate_multimodal_readiness_report(db, session_id)
            job.status = JobStatus.SUCCEEDED.value
            job.result = {
                "report_id": report.id,
                "session_id": report.session_id,
                "readiness_score": report.readiness_score,
                "hiring_recommendation": report.hiring_recommendation,
            }

        logger.info("generate_report.run done job_id={}", job_id)

    except Exception as exc:
        logger.exception("generate_report.run failed job_id={}", job_id)
        with session_scope() as db:
            job = db.get(Job, job_id)
            if job is not None:
                job.status = JobStatus.FAILED.value
                job.error = str(exc)
        raise
