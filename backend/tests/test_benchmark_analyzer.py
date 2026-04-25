"""Tests for app.services.benchmark_analyzer."""
from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from app.models.benchmark_comparison import BenchmarkComparison
from app.models.benchmark_profile import BenchmarkProfile
from app.schemas.benchmark import BenchmarkAnalysisResult
from app.services.benchmark_analyzer import (
    _format_benchmark_summaries,
    _mock_result,
    _parse_llm_json,
    analyze_candidate_vs_benchmark,
)

# ── shared helpers ────────────────────────────────────────────────────────────

SAMPLE_RESUME = (
    "5 years as a project manager in software delivery. "
    "Led sprints, managed stakeholders, delivered 3 products."
)


def _profile(pid: str = "bp-1", role_key: str = "project_manager") -> BenchmarkProfile:
    return BenchmarkProfile(
        id=pid,
        role_key=role_key,
        role_title="Project Manager",
        seniority_level="senior",
        profile_name=f"Benchmark {pid}",
        resume_text="[redacted]",
        skills=["stakeholder management", "risk management", "OKRs"],
        tools=["Jira", "Confluence"],
        project_signals=["led 18-month platform program"],
        impact_signals=["reduced time-to-market by 25%"],
        ownership_signals=["sole accountable owner for P&L"],
        source_type="curated",
        is_curated=True,
        quality_score=90.0,
    )


class FakeDB:
    """Minimal sync-session stand-in."""

    def __init__(self, session_obj: Any = None) -> None:
        self.added: list[Any] = []
        self._session = session_obj

    def add(self, obj: Any) -> None:
        self.added.append(obj)

    def get(self, model_cls: type, pk: str) -> Any:
        return self._session


class MockSessionRow:
    def __init__(self) -> None:
        self.benchmark_similarity_score: int | None = None
        self.resume_competitiveness_score: int | None = None
        self.evidence_strength_score: int | None = None


# ── _mock_result ──────────────────────────────────────────────────────────────

def test_mock_result_returns_correct_type():
    assert isinstance(_mock_result(), BenchmarkAnalysisResult)


def test_mock_result_all_score_fields_in_range():
    r = _mock_result()
    for field in ("benchmark_similarity_score", "resume_competitiveness_score", "evidence_strength_score"):
        val = getattr(r, field)
        assert isinstance(val, int), f"{field} must be int"
        assert 0 <= val <= 100, f"{field} out of range: {val}"


def test_mock_result_all_list_fields_are_lists():
    r = _mock_result()
    for field in (
        "missing_skills", "weak_skills", "missing_metrics",
        "weak_ownership_signals", "interview_risk_areas",
        "recommended_resume_fixes", "question_targets",
    ):
        assert isinstance(getattr(r, field), list), f"{field} must be a list"


def test_mock_result_non_empty_lists():
    r = _mock_result()
    for field in ("interview_risk_areas", "question_targets", "recommended_resume_fixes"):
        assert len(getattr(r, field)) > 0, f"{field} must be non-empty"


# ── _parse_llm_json ───────────────────────────────────────────────────────────

def test_parse_llm_json_extracts_json_object():
    raw = 'Sure:\n{"benchmark_similarity_score": 70, "missing_skills": []}'
    data = _parse_llm_json(raw)
    assert data["benchmark_similarity_score"] == 70


def test_parse_llm_json_raises_when_no_json():
    with pytest.raises(ValueError, match="No JSON object found"):
        _parse_llm_json("No JSON here at all.")


# ── _format_benchmark_summaries ───────────────────────────────────────────────

def test_format_summaries_includes_role_title():
    text = _format_benchmark_summaries([_profile()])
    assert "Project Manager" in text


def test_format_summaries_includes_skills():
    text = _format_benchmark_summaries([_profile()])
    assert "stakeholder management" in text


def test_format_summaries_includes_impact_signals():
    text = _format_benchmark_summaries([_profile()])
    assert "reduced time-to-market" in text


def test_format_summaries_empty_list_returns_empty_string():
    text = _format_benchmark_summaries([])
    assert text == ""


def test_format_summaries_does_not_include_resume_text():
    p = _profile()
    p.resume_text = "SECRET RESUME CONTENT"
    text = _format_benchmark_summaries([p])
    assert "SECRET RESUME CONTENT" not in text


# ── analyze_candidate_vs_benchmark (mock mode) ────────────────────────────────

def test_analyze_returns_benchmark_analysis_result():
    db = FakeDB(MockSessionRow())
    result = analyze_candidate_vs_benchmark(
        SAMPLE_RESUME,
        [_profile()],
        role_key="project_manager",
        session_id="s1",
        db=db,
    )
    assert isinstance(result, BenchmarkAnalysisResult)


def test_analyze_mock_mode_does_not_call_llm():
    db = FakeDB(MockSessionRow())
    with patch("app.services.benchmark_analyzer.llm.chat") as mock_chat:
        analyze_candidate_vs_benchmark(
            SAMPLE_RESUME, [_profile()],
            role_key="project_manager", session_id="s1", db=db,
        )
    mock_chat.assert_not_called()


def test_analyze_accepts_empty_profiles_list():
    db = FakeDB(MockSessionRow())
    result = analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [],
        role_key="project_manager", session_id="s1", db=db,
    )
    assert isinstance(result, BenchmarkAnalysisResult)


# ── persistence: BenchmarkComparison row ─────────────────────────────────────

def test_analyze_adds_comparison_row_to_db():
    db = FakeDB(MockSessionRow())
    analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="s1", db=db,
    )
    comparison_rows = [o for o in db.added if isinstance(o, BenchmarkComparison)]
    assert len(comparison_rows) == 1


def test_comparison_row_has_correct_session_id_and_role_key():
    db = FakeDB(MockSessionRow())
    analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="sess-99", db=db,
    )
    row = db.added[0]
    assert row.session_id == "sess-99"
    assert row.role_key == "project_manager"


def test_comparison_row_stores_benchmark_profile_ids():
    db = FakeDB(MockSessionRow())
    profiles = [_profile("bp-1"), _profile("bp-2"), _profile("bp-3")]
    analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, profiles,
        role_key="project_manager", session_id="s1", db=db,
    )
    row = db.added[0]
    assert set(row.benchmark_profile_ids) == {"bp-1", "bp-2", "bp-3"}


def test_comparison_row_stores_score_fields():
    db = FakeDB(MockSessionRow())
    analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="s1", db=db,
    )
    row = db.added[0]
    assert isinstance(row.benchmark_similarity_score, int)
    assert isinstance(row.resume_competitiveness_score, int)
    assert isinstance(row.evidence_strength_score, int)


def test_comparison_row_stores_list_fields():
    db = FakeDB(MockSessionRow())
    analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="s1", db=db,
    )
    row = db.added[0]
    for field in (
        "missing_skills", "weak_skills", "missing_metrics",
        "weak_ownership_signals", "interview_risk_areas",
        "recommended_resume_fixes", "question_targets",
    ):
        assert isinstance(getattr(row, field), list), f"{field} must be a list"


def test_comparison_row_question_targets_populated():
    db = FakeDB(MockSessionRow())
    analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="s1", db=db,
    )
    row = db.added[0]
    assert len(row.question_targets) > 0


def test_comparison_row_has_uuid_id():
    db = FakeDB(MockSessionRow())
    analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="s1", db=db,
    )
    row = db.added[0]
    assert row.id is not None
    assert len(row.id) == 36


# ── persistence: session score update ────────────────────────────────────────

def test_session_scores_updated():
    session_row = MockSessionRow()
    db = FakeDB(session_row)
    analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="s1", db=db,
    )
    assert session_row.benchmark_similarity_score is not None
    assert session_row.resume_competitiveness_score is not None
    assert session_row.evidence_strength_score is not None


def test_session_scores_match_result():
    session_row = MockSessionRow()
    db = FakeDB(session_row)
    result = analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="s1", db=db,
    )
    assert session_row.benchmark_similarity_score == result.benchmark_similarity_score
    assert session_row.resume_competitiveness_score == result.resume_competitiveness_score
    assert session_row.evidence_strength_score == result.evidence_strength_score


def test_missing_session_does_not_raise():
    db = FakeDB(session_obj=None)  # db.get() returns None
    # should complete without error and still return result
    result = analyze_candidate_vs_benchmark(
        SAMPLE_RESUME, [_profile()],
        role_key="project_manager", session_id="nonexistent", db=db,
    )
    assert isinstance(result, BenchmarkAnalysisResult)


# ── schema validation ─────────────────────────────────────────────────────────

def test_schema_rejects_score_above_100():
    with pytest.raises(Exception):
        BenchmarkAnalysisResult(
            benchmark_similarity_score=101,
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


def test_schema_rejects_negative_score():
    with pytest.raises(Exception):
        BenchmarkAnalysisResult(
            benchmark_similarity_score=70,
            resume_competitiveness_score=-1,
            evidence_strength_score=60,
            missing_skills=[],
            weak_skills=[],
            missing_metrics=[],
            weak_ownership_signals=[],
            interview_risk_areas=[],
            recommended_resume_fixes=[],
            question_targets=[],
        )
