from __future__ import annotations

from typing import Any

from app.models.session import InterviewSession, InterviewSessionStatus
from app.schemas.benchmark import BenchmarkAnalysisResult
from app.schemas.match import MatchAnalysisResult
from app.schemas.question import GeneratedQuestion
from app.tasks import prepare_session as task


class FakeDB:
    def __init__(self, session: InterviewSession) -> None:
        self.session = session
        self.added: list[Any] = []
        self.executed: list[Any] = []

    def get(self, model_cls: type, pk: str) -> Any:
        if model_cls is InterviewSession and pk == self.session.id:
            return self.session
        return None

    def add(self, obj: Any) -> None:
        self.added.append(obj)

    def execute(self, stmt: Any) -> Any:
        self.executed.append(stmt)

        class Result:
            def scalars(self) -> "Result":
                return self

            def all(self) -> list:
                return []

        return Result()


def _session() -> InterviewSession:
    return InterviewSession(
        id="session-1",
        job_description_text="We need a backend engineer with FastAPI, PostgreSQL, and ownership.",
        resume_text="Built APIs with Python and FastAPI. Owned platform delivery and reliability.",
        status=InterviewSessionStatus.DRAFT.value,
    )


def test_prepare_session_runs_pipeline_and_marks_ready(monkeypatch):
    session = _session()
    db = FakeDB(session)

    match_result = MatchAnalysisResult(
        role_title="Backend Engineer",
        role_key="backend_developer",
        seniority_level="mid",
        match_score=72,
        matched_skills=["FastAPI"],
        missing_skills=["system design"],
        risk_areas=["limited metrics"],
        interview_focus_areas=["ownership"],
    )
    benchmark_result = BenchmarkAnalysisResult(
        benchmark_similarity_score=65,
        resume_competitiveness_score=70,
        evidence_strength_score=60,
        missing_skills=[],
        weak_skills=[],
        missing_metrics=[],
        weak_ownership_signals=[],
        interview_risk_areas=[],
        recommended_resume_fixes=[],
        question_targets=[],
    )

    monkeypatch.setattr(
        task,
        "embed_and_store",
        lambda **kwargs: [object()],
    )
    monkeypatch.setattr(task, "analyze_match", lambda *args, **kwargs: match_result)
    monkeypatch.setattr(task, "retrieve_benchmark_profiles", lambda *args, **kwargs: [])
    monkeypatch.setattr(
        task,
        "analyze_candidate_vs_benchmark",
        lambda *args, **kwargs: benchmark_result,
    )
    monkeypatch.setattr(
        task,
        "generate_interview_questions",
        lambda *args, **kwargs: [
            GeneratedQuestion(
                question_number=1,
                category="technical",
                question_text="Question?",
            )
        ],
    )

    result = task.prepare_session(db, session.id)

    assert session.status == InterviewSessionStatus.READY.value
    assert result["role_key"] == "backend_developer"
    assert result["match_score"] == 72
    assert result["benchmark_similarity_score"] == 65
    assert result["jd_chunk_count"] == 1
    assert result["resume_chunk_count"] == 1
    assert result["question_count"] == 1


def test_prepare_session_requires_resume_text(monkeypatch):
    session = _session()
    session.resume_text = None
    db = FakeDB(session)

    try:
        task.prepare_session(db, session.id)
    except ValueError as exc:
        assert "resume" in str(exc).lower()
    else:
        raise AssertionError("Expected ValueError")
