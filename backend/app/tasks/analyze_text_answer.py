from __future__ import annotations

from loguru import logger

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.job import Job, JobStatus
from app.models.question import InterviewQuestion
from app.services.text_answer_agent import analyze_text_answer
from app.tasks._db import session_scope


def run(job_id: str) -> None:
    logger.info("analyze_text_answer.run start job_id={}", job_id)

    with session_scope() as db:
        job = db.get(Job, job_id)
        if job is None:
            logger.error("analyze_text_answer.run job {} not found", job_id)
            return
        job.status = JobStatus.RUNNING.value

    try:
        with session_scope() as db:
            job = db.get(Job, job_id)
            answer_id = str(job.input["answer_id"])
            answer = db.get(CandidateAnswer, answer_id)
            if answer is None:
                raise ValueError(f"Candidate answer not found: {answer_id}")
            question = db.get(InterviewQuestion, answer.question_id)
            if question is None:
                raise ValueError(f"Interview question not found: {answer.question_id}")

            result = analyze_text_answer(question=question, answer=answer)
            row = store_text_answer_agent_result(db, answer_id=answer.id, result=result)
            job.status = JobStatus.SUCCEEDED.value
            job.result = {"agent_result_id": row.id, **result.model_dump()}

        logger.info("analyze_text_answer.run done job_id={}", job_id)

    except Exception as exc:
        logger.exception("analyze_text_answer.run failed job_id={}", job_id)
        with session_scope() as db:
            job = db.get(Job, job_id)
            if job is not None:
                job.status = JobStatus.FAILED.value
                job.error = str(exc)
        raise


def store_text_answer_agent_result(db, *, answer_id: str, result) -> AgentResult:
    score = _average_score(
        [
            result.relevance_score,
            result.structure_score,
            result.specificity_score,
            result.evidence_score,
            result.clarity_score,
            result.completeness_score,
        ]
    )
    row = AgentResult(
        answer_id=answer_id,
        agent_type=AgentType.TEXT_ANSWER.value,
        status=AgentResultStatus.SUCCEEDED.value,
        score=float(score),
        payload=result.model_dump(),
    )
    db.add(row)
    return row


def _average_score(values: list[int]) -> int:
    return round(sum(values) / len(values))
