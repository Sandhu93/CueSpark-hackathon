from __future__ import annotations

from loguru import logger

from app.core import storage
from app.models.answer import AnswerTranscriptionStatus, CandidateAnswer
from app.models.job import Job, JobStatus
from app.services.audio_agent import process_audio_answer
from app.tasks._db import session_scope


def run(job_id: str) -> None:
    logger.info("process_audio_answer.run start job_id={}", job_id)

    with session_scope() as db:
        job = db.get(Job, job_id)
        if job is None:
            logger.error("process_audio_answer.run job {} not found", job_id)
            return
        job.status = JobStatus.RUNNING.value
        answer_id = str(job.input.get("answer_id", ""))

    try:
        with session_scope() as db:
            job = db.get(Job, job_id)
            answer_id = str(job.input["answer_id"])
            answer = db.get(CandidateAnswer, answer_id)
            if answer is None:
                raise ValueError(f"Candidate answer not found: {answer_id}")
            result = process_candidate_answer_audio(answer)
            job.status = JobStatus.SUCCEEDED.value
            job.result = result

        logger.info("process_audio_answer.run done job_id={}", job_id)

    except Exception as exc:
        logger.exception("process_audio_answer.run failed job_id={}", job_id)
        with session_scope() as db:
            job = db.get(Job, job_id)
            if job is not None:
                job.status = JobStatus.FAILED.value
                job.error = str(exc)
        raise


def process_candidate_answer_audio(answer: CandidateAnswer) -> dict:
    if not answer.audio_object_key:
        answer.transcription_status = AnswerTranscriptionStatus.FAILED.value
        raise ValueError("Candidate answer has no audio object key")

    audio_bytes = storage.get_object(answer.audio_object_key)
    result = process_audio_answer(
        audio_bytes,
        filename=answer.audio_object_key.rsplit("/", 1)[-1],
        duration_seconds=answer.duration_seconds,
    )
    answer.transcript = result.transcript
    answer.word_count = result.word_count
    answer.duration_seconds = result.duration_seconds
    answer.words_per_minute = result.words_per_minute
    answer.filler_word_count = result.filler_word_count
    answer.transcription_status = AnswerTranscriptionStatus.TRANSCRIBED.value
    answer.communication_metrics = {
        "filler_words": result.filler_words,
        "hesitation_markers": result.hesitation_markers,
        "structure_observations": result.structure_observations,
        "communication_signal_score": result.communication_signal_score,
        "safe_signal_labels": [
            "communication signal score",
            "speaking pace",
            "filler words",
            "pause markers",
            "answer structure",
            "clarity",
        ],
    }
    return result.model_dump()
