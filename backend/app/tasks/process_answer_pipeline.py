from __future__ import annotations

from collections.abc import Callable
from typing import Any

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import AnswerProcessingStatus, CandidateAnswer
from app.models.evaluation import AnswerEvaluation
from app.models.job import Job, JobStatus
from app.models.question import InterviewQuestion, ResponseMode
from app.services.benchmark_gap_agent import analyze_benchmark_gap_coverage
from app.services.code_evaluation_agent import analyze_code_answer
from app.services.final_evaluation_orchestrator import evaluate_answer
from app.services.text_answer_agent import analyze_text_answer
from app.services.video_signal_agent import SAFE_VISUAL_SIGNAL_LABELS, analyze_video_signals
from app.tasks._db import session_scope
from app.tasks.analyze_benchmark_gap_coverage import store_benchmark_gap_agent_result
from app.tasks.analyze_code_answer import store_code_evaluation_agent_result
from app.tasks.analyze_text_answer import store_text_answer_agent_result
from app.tasks.analyze_video_signals import store_video_signal_agent_result
from app.tasks.process_audio_answer import process_candidate_answer_audio


def run(job_id: str) -> None:
    logger.info("process_answer_pipeline.run start job_id={}", job_id)

    with session_scope() as db:
        job = db.get(Job, job_id)
        if job is None:
            logger.error("process_answer_pipeline.run job {} not found", job_id)
            return
        job.status = JobStatus.RUNNING.value

    try:
        with session_scope() as db:
            job = db.get(Job, job_id)
            answer_id = str(job.input["answer_id"])
            result = process_answer_pipeline(db, answer_id)
            job.status = JobStatus.SUCCEEDED.value
            job.result = result

        logger.info("process_answer_pipeline.run done job_id={}", job_id)

    except Exception as exc:
        logger.exception("process_answer_pipeline.run failed job_id={}", job_id)
        with session_scope() as db:
            job = db.get(Job, job_id)
            if job is not None:
                job.status = JobStatus.FAILED.value
                job.error = str(exc)
                answer_id = str(job.input.get("answer_id", "")) if job.input else ""
                if answer_id:
                    answer = db.get(CandidateAnswer, answer_id)
                    if answer is not None:
                        answer.processing_status = AnswerProcessingStatus.FAILED.value
        raise


def process_answer_pipeline(db: Session, answer_id: str) -> dict[str, Any]:
    answer = db.get(CandidateAnswer, answer_id)
    if answer is None:
        raise ValueError(f"Candidate answer not found: {answer_id}")
    question = db.get(InterviewQuestion, answer.question_id)
    if question is None:
        raise ValueError(f"Interview question not found: {answer.question_id}")

    answer.processing_status = AnswerProcessingStatus.PROCESSING.value
    steps_run: list[str] = []
    steps_skipped: list[str] = []

    if _should_run_audio(answer, question):
        _run_agent_once(
            db,
            answer=answer,
            agent_type=AgentType.AUDIO.value,
            steps_run=steps_run,
            steps_skipped=steps_skipped,
            runner=lambda: _run_audio_agent(db, answer),
        )

    if _should_run_text(answer, question):
        _run_agent_once(
            db,
            answer=answer,
            agent_type=AgentType.TEXT_ANSWER.value,
            steps_run=steps_run,
            steps_skipped=steps_skipped,
            runner=lambda: store_text_answer_agent_result(
                db,
                answer_id=answer.id,
                result=analyze_text_answer(question=question, answer=answer),
            ),
        )

    if _should_run_code(answer, question):
        _run_agent_once(
            db,
            answer=answer,
            agent_type=AgentType.CODE_EVALUATION.value,
            steps_run=steps_run,
            steps_skipped=steps_skipped,
            runner=lambda: store_code_evaluation_agent_result(
                db,
                answer_id=answer.id,
                result=analyze_code_answer(question=question, answer=answer),
            ),
        )

    if _should_run_video(answer, question):
        _run_agent_once(
            db,
            answer=answer,
            agent_type=AgentType.VIDEO_SIGNAL.value,
            steps_run=steps_run,
            steps_skipped=steps_skipped,
            runner=lambda: _run_video_agent(db, answer),
        )

    _run_agent_once(
        db,
        answer=answer,
        agent_type=AgentType.BENCHMARK_GAP.value,
        steps_run=steps_run,
        steps_skipped=steps_skipped,
        runner=lambda: store_benchmark_gap_agent_result(
            db,
            answer_id=answer.id,
            result=analyze_benchmark_gap_coverage(question=question, answer=answer),
        ),
    )

    if _has_evaluation(db, answer.id):
        steps_skipped.append("final_evaluation")
        answer.processing_status = AnswerProcessingStatus.EVALUATED.value
    else:
        answer.processing_status = AnswerProcessingStatus.EVALUATING.value
        evaluate_answer(db, answer.id)
        steps_run.append("final_evaluation")

    return {
        "answer_id": answer.id,
        "processing_status": answer.processing_status,
        "steps_run": steps_run,
        "steps_skipped": steps_skipped,
    }


def _run_video_agent(db: Session, answer: CandidateAnswer) -> AgentResult:
    result = analyze_video_signals(answer=answer, metadata=answer.visual_signal_metadata or {})
    row = store_video_signal_agent_result(db, answer_id=answer.id, result=result)
    answer.visual_signal_metadata = {
        **(answer.visual_signal_metadata or {}),
        "visual_signal_summary": result.model_dump(),
        "safe_signal_labels": SAFE_VISUAL_SIGNAL_LABELS,
    }
    return row


def _run_audio_agent(db: Session, answer: CandidateAnswer) -> AgentResult:
    result = process_candidate_answer_audio(answer)
    row = AgentResult(
        answer_id=answer.id,
        agent_type=AgentType.AUDIO.value,
        status=AgentResultStatus.SUCCEEDED.value,
        score=float(result.get("communication_signal_score", 0)),
        payload=result,
    )
    db.add(row)
    return row


def _run_agent_once(
    db: Session,
    *,
    answer: CandidateAnswer,
    agent_type: str,
    steps_run: list[str],
    steps_skipped: list[str],
    runner: Callable[[], Any],
) -> None:
    if _has_successful_agent_result(db, answer.id, agent_type):
        steps_skipped.append(agent_type)
        return

    try:
        runner()
    except Exception as exc:
        _store_failed_agent_result(db, answer_id=answer.id, agent_type=agent_type, exc=exc)
        answer.processing_status = AnswerProcessingStatus.FAILED.value
        raise
    steps_run.append(agent_type)


def _has_successful_agent_result(db: Session, answer_id: str, agent_type: str) -> bool:
    stmt = select(AgentResult).where(
        AgentResult.answer_id == answer_id,
        AgentResult.agent_type == agent_type,
        AgentResult.status == AgentResultStatus.SUCCEEDED.value,
    )
    return db.execute(stmt).scalars().first() is not None


def _has_evaluation(db: Session, answer_id: str) -> bool:
    stmt = select(AnswerEvaluation).where(AnswerEvaluation.answer_id == answer_id)
    return db.execute(stmt).scalars().first() is not None


def _store_failed_agent_result(
    db: Session,
    *,
    answer_id: str,
    agent_type: str,
    exc: Exception,
) -> AgentResult:
    row = AgentResult(
        answer_id=answer_id,
        agent_type=agent_type,
        status=AgentResultStatus.FAILED.value,
        payload={},
        error=str(exc),
    )
    db.add(row)
    return row


def _answer_mode(answer: CandidateAnswer, question: InterviewQuestion) -> ResponseMode:
    raw_mode = answer.answer_mode or question.response_mode or ResponseMode.SPOKEN_ANSWER.value
    return ResponseMode(raw_mode)


def _should_run_audio(answer: CandidateAnswer, question: InterviewQuestion) -> bool:
    mode = _answer_mode(answer, question)
    return bool(answer.audio_object_key) or bool(question.requires_audio) or mode == ResponseMode.SPOKEN_ANSWER


def _should_run_text(answer: CandidateAnswer, question: InterviewQuestion) -> bool:
    mode = _answer_mode(answer, question)
    return bool(answer.text_answer) or bool(question.requires_text) or mode == ResponseMode.WRITTEN_ANSWER


def _should_run_code(answer: CandidateAnswer, question: InterviewQuestion) -> bool:
    mode = _answer_mode(answer, question)
    return bool(answer.code_answer) or bool(question.requires_code) or mode == ResponseMode.CODE_ANSWER


def _should_run_video(answer: CandidateAnswer, question: InterviewQuestion) -> bool:
    return bool(answer.visual_signal_metadata) or bool(question.requires_video)
