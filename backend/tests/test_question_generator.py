from __future__ import annotations

from typing import Any
from unittest.mock import patch

from app.models.question import InterviewQuestion, QuestionCategory, QuestionSource, ResponseMode
from app.schemas.benchmark import BenchmarkAnalysisResult
from app.schemas.match import MatchAnalysisResult
from app.services import question_generator as qg
from app.services.question_generator import (
    _format_benchmark_section,
    generate_interview_questions,
)


SAMPLE_JD = "Senior backend role requiring FastAPI, PostgreSQL, ownership, and clear metrics."
SAMPLE_RESUME = "Backend engineer with Python, APIs, and platform delivery experience."


class FakeDB:
    def __init__(self) -> None:
        self.added: list[Any] = []

    def add(self, obj: Any) -> None:
        self.added.append(obj)


def _match_result() -> MatchAnalysisResult:
    return MatchAnalysisResult(
        role_title="Senior Backend Engineer",
        role_key="senior_backend_engineer",
        seniority_level="senior",
        match_score=72,
        matched_skills=["Python", "FastAPI"],
        missing_skills=["distributed systems"],
        risk_areas=["not enough quantified impact"],
        interview_focus_areas=["ownership", "system design"],
    )


def _benchmark_result() -> BenchmarkAnalysisResult:
    return BenchmarkAnalysisResult(
        benchmark_similarity_score=68,
        resume_competitiveness_score=64,
        evidence_strength_score=52,
        missing_skills=["distributed tracing"],
        weak_skills=["capacity planning"],
        missing_metrics=["latency reduction metrics"],
        weak_ownership_signals=["platform roadmap ownership"],
        interview_risk_areas=["production incident response"],
        recommended_resume_fixes=["add quantified reliability wins"],
        question_targets=["distributed systems trade-offs", "SLO ownership"],
    )


def test_generation_with_benchmark_returns_10_questions(monkeypatch):
    monkeypatch.setattr(qg.settings, "ai_mock_mode", True)
    db = FakeDB()

    questions = generate_interview_questions(
        SAMPLE_JD,
        SAMPLE_RESUME,
        _match_result(),
        _benchmark_result(),
        session_id="session-1",
        db=db,
    )

    assert len(questions) == 10
    assert [q.question_number for q in questions] == list(range(1, 11))
    assert len(db.added) == 10


def test_mock_generation_uses_multimodal_distribution(monkeypatch):
    monkeypatch.setattr(qg.settings, "ai_mock_mode", True)
    db = FakeDB()

    questions = generate_interview_questions(
        SAMPLE_JD,
        SAMPLE_RESUME,
        _match_result(),
        _benchmark_result(),
        session_id="session-1",
        db=db,
    )

    assert [q.response_mode for q in questions] == [
        ResponseMode.SPOKEN_ANSWER,
        ResponseMode.SPOKEN_ANSWER,
        ResponseMode.WRITTEN_ANSWER,
        ResponseMode.CODE_ANSWER,
        ResponseMode.MIXED_ANSWER,
        ResponseMode.SPOKEN_ANSWER,
        ResponseMode.SPOKEN_ANSWER,
        ResponseMode.WRITTEN_ANSWER,
        ResponseMode.SPOKEN_ANSWER,
        ResponseMode.MIXED_ANSWER,
    ]
    assert {q.response_mode for q in questions} == {
        ResponseMode.SPOKEN_ANSWER,
        ResponseMode.WRITTEN_ANSWER,
        ResponseMode.CODE_ANSWER,
        ResponseMode.MIXED_ANSWER,
    }
    assert [(q.requires_audio, q.requires_text, q.requires_code, q.requires_video) for q in questions] == [
        (True, False, False, False),
        (True, False, False, False),
        (False, True, False, False),
        (False, False, True, False),
        (True, True, True, False),
        (True, False, False, False),
        (True, False, False, False),
        (False, True, False, False),
        (True, False, False, False),
        (True, True, False, True),
    ]


def test_generation_with_benchmark_includes_at_least_four_gap_questions(monkeypatch):
    monkeypatch.setattr(qg.settings, "ai_mock_mode", True)
    db = FakeDB()

    questions = generate_interview_questions(
        SAMPLE_JD,
        SAMPLE_RESUME,
        _match_result(),
        _benchmark_result(),
        session_id="session-1",
        db=db,
    )

    benchmark_questions = [
        q for q in questions if q.source == QuestionSource.BENCHMARK_GAP.value
    ]
    assert len(benchmark_questions) >= 4
    assert all(
        q.category == QuestionCategory.BENCHMARK_GAP_VALIDATION.value
        for q in benchmark_questions
    )
    assert all(q.benchmark_gap_refs for q in benchmark_questions)
    assert all(q.why_this_was_asked.startswith("Benchmark gap:") for q in benchmark_questions)


def test_generation_uses_benchmark_question_targets(monkeypatch):
    monkeypatch.setattr(qg.settings, "ai_mock_mode", True)
    db = FakeDB()

    questions = generate_interview_questions(
        SAMPLE_JD,
        SAMPLE_RESUME,
        _match_result(),
        _benchmark_result(),
        session_id="session-1",
        db=db,
    )

    all_refs = [ref for question in questions for ref in question.benchmark_gap_refs]
    assert "distributed systems trade-offs" in all_refs


def test_generation_without_benchmark_uses_base_plan_only(monkeypatch):
    monkeypatch.setattr(qg.settings, "ai_mock_mode", True)
    db = FakeDB()

    questions = generate_interview_questions(
        SAMPLE_JD,
        SAMPLE_RESUME,
        _match_result(),
        None,
        session_id="session-1",
        db=db,
    )

    assert len(questions) == 10
    assert all(q.source == QuestionSource.BASE_PLAN.value for q in questions)
    assert all(not q.benchmark_gap_refs for q in questions)


def test_generation_persists_question_rows(monkeypatch):
    monkeypatch.setattr(qg.settings, "ai_mock_mode", True)
    db = FakeDB()

    generate_interview_questions(
        SAMPLE_JD,
        SAMPLE_RESUME,
        _match_result(),
        _benchmark_result(),
        session_id="session-42",
        db=db,
    )

    rows = [obj for obj in db.added if isinstance(obj, InterviewQuestion)]
    assert len(rows) == 10
    assert rows[0].session_id == "session-42"
    assert rows[0].source == QuestionSource.BENCHMARK_GAP.value
    assert rows[0].benchmark_gap_refs
    assert rows[0].response_mode == "spoken_answer"
    assert rows[0].requires_audio is True
    assert rows[0].requires_video is False
    assert rows[0].requires_text is False
    assert rows[0].requires_code is False


def test_generation_persists_multimodal_question_flags(monkeypatch):
    monkeypatch.setattr(qg.settings, "ai_mock_mode", True)
    db = FakeDB()

    generate_interview_questions(
        SAMPLE_JD,
        SAMPLE_RESUME,
        _match_result(),
        _benchmark_result(),
        session_id="session-42",
        db=db,
    )

    rows = [obj for obj in db.added if isinstance(obj, InterviewQuestion)]
    rows.sort(key=lambda row: row.question_number)
    assert [(row.response_mode, row.requires_audio, row.requires_text, row.requires_code, row.requires_video) for row in rows] == [
        ("spoken_answer", True, False, False, False),
        ("spoken_answer", True, False, False, False),
        ("written_answer", False, True, False, False),
        ("code_answer", False, False, True, False),
        ("mixed_answer", True, True, True, False),
        ("spoken_answer", True, False, False, False),
        ("spoken_answer", True, False, False, False),
        ("written_answer", False, True, False, False),
        ("spoken_answer", True, False, False, False),
        ("mixed_answer", True, True, False, True),
    ]


def test_format_benchmark_section_includes_question_targets():
    text = _format_benchmark_section(_benchmark_result())

    assert "Question targets: distributed systems trade-offs; SLO ownership" in text
    assert "Weak skills: capacity planning" in text
    assert "Resume fixes to probe: add quantified reliability wins" in text


def test_real_mode_parse_failure_falls_back_to_mock_questions(monkeypatch):
    monkeypatch.setattr(qg.settings, "ai_mock_mode", False)
    monkeypatch.setattr(qg.settings, "openai_api_key", "test-key")
    db = FakeDB()

    with patch("app.services.question_generator.llm.chat", return_value="not-json"):
        questions = generate_interview_questions(
            SAMPLE_JD,
            SAMPLE_RESUME,
            _match_result(),
            _benchmark_result(),
            session_id="session-1",
            db=db,
        )

    assert len(questions) == 10
    assert len([q for q in questions if q.source == QuestionSource.BENCHMARK_GAP.value]) >= 4
