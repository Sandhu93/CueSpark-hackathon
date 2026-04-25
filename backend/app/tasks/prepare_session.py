from __future__ import annotations

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core import storage
from app.models.benchmark_comparison import BenchmarkComparison
from app.models.document import Document, DocumentParseStatus, DocumentType
from app.models.embedding_chunk import ChunkType, EmbeddingChunk
from app.models.job import Job, JobStatus
from app.models.question import InterviewQuestion
from app.models.session import InterviewSession, InterviewSessionStatus
from app.services.benchmark_analyzer import analyze_candidate_vs_benchmark
from app.services.benchmark_retrieval import retrieve_benchmark_profiles
from app.services.document_parser import extract_document_text
from app.services.embeddings import embed_and_store
from app.services.match_analyzer import analyze_match
from app.services.question_generator import generate_interview_questions
from app.tasks._db import session_scope


def run(job_id: str) -> None:
    logger.info("prepare_session.run start job_id={}", job_id)

    with session_scope() as db:
        job = db.get(Job, job_id)
        if job is None:
            logger.error("prepare_session.run job {} not found", job_id)
            return
        job.status = JobStatus.RUNNING.value
        session_id = str(job.input.get("session_id", ""))
        session = db.get(InterviewSession, session_id)
        if session is None:
            job.status = JobStatus.FAILED.value
            job.error = f"Session not found: {session_id}"
            logger.error("prepare_session.run session {} not found", session_id)
            return
        session.status = InterviewSessionStatus.PREPARING.value

    try:
        with session_scope() as db:
            job = db.get(Job, job_id)
            session_id = str(job.input["session_id"])
            result = prepare_session(db, session_id)
            job.status = JobStatus.SUCCEEDED.value
            job.result = result

        logger.info("prepare_session.run done job_id={}", job_id)

    except Exception as exc:
        logger.exception("prepare_session.run failed job_id={}", job_id)
        with session_scope() as db:
            job = db.get(Job, job_id)
            if job is not None:
                job.status = JobStatus.FAILED.value
                job.error = str(exc)
                session_id = job.input.get("session_id") if job.input else None
                if session_id:
                    session = db.get(InterviewSession, str(session_id))
                    if session is not None:
                        session.status = InterviewSessionStatus.FAILED.value
        raise


def prepare_session(db: Session, session_id: str) -> dict:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise ValueError(f"Session not found: {session_id}")

    session.status = InterviewSessionStatus.PREPARING.value
    resume_text = _get_resume_text(db, session)
    jd_text = session.job_description_text
    if not jd_text or not jd_text.strip():
        raise ValueError("Session has no job description text")
    if not resume_text or not resume_text.strip():
        raise ValueError("Session has no parsed resume text")

    _clear_previous_preparation(db, session_id)

    jd_chunks = embed_and_store(
        text=jd_text,
        chunk_type=ChunkType.JD.value,
        session_id=session_id,
        db=db,
    )
    resume_chunks = embed_and_store(
        text=resume_text,
        chunk_type=ChunkType.RESUME.value,
        session_id=session_id,
        db=db,
    )

    match_result = analyze_match(
        jd_text,
        resume_text,
        db=db,
        session_id=session_id,
    )
    benchmark_profiles = retrieve_benchmark_profiles(
        match_result.role_key,
        jd_text,
        db,
        top_k=5,
    )
    benchmark_result = analyze_candidate_vs_benchmark(
        resume_text,
        benchmark_profiles,
        role_key=match_result.role_key,
        session_id=session_id,
        db=db,
    )
    questions = generate_interview_questions(
        jd_text,
        resume_text,
        match_result,
        benchmark_result,
        session_id=session_id,
        db=db,
    )

    session.status = InterviewSessionStatus.READY.value
    return {
        "session_id": session_id,
        "status": session.status,
        "role_key": match_result.role_key,
        "match_score": match_result.match_score,
        "benchmark_similarity_score": benchmark_result.benchmark_similarity_score,
        "resume_competitiveness_score": benchmark_result.resume_competitiveness_score,
        "evidence_strength_score": benchmark_result.evidence_strength_score,
        "benchmark_profile_count": len(benchmark_profiles),
        "jd_chunk_count": len(jd_chunks),
        "resume_chunk_count": len(resume_chunks),
        "question_count": len(questions),
    }


def _get_resume_text(db: Session, session: InterviewSession) -> str:
    if session.resume_text and session.resume_text.strip():
        return session.resume_text

    stmt = (
        select(Document)
        .where(
            Document.session_id == session.id,
            Document.document_type == DocumentType.RESUME.value,
        )
        .order_by(Document.created_at.desc())
    )
    documents = list(db.execute(stmt).scalars().all())
    for document in documents:
        if document.extracted_text and document.extracted_text.strip():
            session.resume_text = document.extracted_text
            return document.extracted_text

    for document in documents:
        if document.object_key and document.filename:
            parsed = extract_document_text(
                storage.get_object(document.object_key),
                document.filename,
                document.content_type,
            )
            document.extracted_text = parsed.extracted_text
            document.parse_status = parsed.parse_status.value
            document.metadata_ = {**(document.metadata_ or {}), **parsed.metadata}
            if parsed.parse_status == DocumentParseStatus.PARSED and parsed.extracted_text:
                session.resume_text = parsed.extracted_text
                return parsed.extracted_text

    return ""


def _clear_previous_preparation(db: Session, session_id: str) -> None:
    db.execute(delete(EmbeddingChunk).where(EmbeddingChunk.session_id == session_id))
    db.execute(delete(BenchmarkComparison).where(BenchmarkComparison.session_id == session_id))
    db.execute(delete(InterviewQuestion).where(InterviewQuestion.session_id == session_id))
