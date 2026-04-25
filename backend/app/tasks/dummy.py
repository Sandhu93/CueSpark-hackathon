"""
Reference task that demonstrates the lifecycle every task should follow:
  1. Mark RUNNING
  2. Do work (call AI services, hit MinIO, etc.)
  3. Write result + mark SUCCEEDED
  4. On exception, mark FAILED with the error message

Copy this file as a starting point for new tasks.
"""
from __future__ import annotations

import time

from loguru import logger

from app.models.job import Job, JobStatus
from app.tasks._db import session_scope


def run(job_id: str) -> None:
    logger.info("dummy.run start job_id={}", job_id)

    with session_scope() as db:
        job = db.get(Job, job_id)
        if job is None:
            logger.error("Job {} not found", job_id)
            return
        job.status = JobStatus.RUNNING.value

    try:
        # ---- your real work goes here ----
        time.sleep(2)
        echo = {"echo": "hello from worker", "job_id": job_id}
        # ----------------------------------

        with session_scope() as db:
            job = db.get(Job, job_id)
            job.status = JobStatus.SUCCEEDED.value
            job.result = echo

        logger.info("dummy.run done job_id={}", job_id)

    except Exception as e:
        logger.exception("dummy.run failed")
        with session_scope() as db:
            job = db.get(Job, job_id)
            job.status = JobStatus.FAILED.value
            job.error = str(e)
        raise
