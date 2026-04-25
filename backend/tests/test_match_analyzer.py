from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from app.schemas.match import MatchAnalysisResult
from app.services.match_analyzer import _parse_llm_json, analyze_match


SAMPLE_JD = "We are hiring a senior Python developer with FastAPI and PostgreSQL experience."
SAMPLE_RESUME = "5 years Python, FastAPI, SQLAlchemy, REST API design. Led a team of 3 engineers."


# ── mock mode ────────────────────────────────────────────────────────────────

def test_mock_mode_returns_match_analysis_result():
    result = analyze_match(SAMPLE_JD, SAMPLE_RESUME)
    assert isinstance(result, MatchAnalysisResult)


def test_mock_mode_required_fields_present():
    result = analyze_match(SAMPLE_JD, SAMPLE_RESUME)
    assert result.role_title
    assert result.role_key
    assert result.seniority_level
    assert 0 <= result.match_score <= 100
    assert isinstance(result.matched_skills, list)
    assert isinstance(result.missing_skills, list)
    assert isinstance(result.risk_areas, list)
    assert isinstance(result.interview_focus_areas, list)


def test_mock_mode_role_key_is_snake_case():
    result = analyze_match(SAMPLE_JD, SAMPLE_RESUME)
    assert " " not in result.role_key
    assert result.role_key == result.role_key.lower()


def test_mock_mode_match_score_in_range():
    result = analyze_match(SAMPLE_JD, SAMPLE_RESUME)
    assert 0 <= result.match_score <= 100


def test_mock_mode_does_not_call_llm_chat():
    with patch("app.services.match_analyzer.llm.chat") as mock_chat:
        analyze_match(SAMPLE_JD, SAMPLE_RESUME)
    mock_chat.assert_not_called()


# ── session persistence ───────────────────────────────────────────────────────

class FakeSession:
    """Minimal sync-session stand-in that supports get() and attribute writes."""

    def __init__(self, session_obj: Any) -> None:
        self._obj = session_obj

    def get(self, model_cls: type, pk: str) -> Any:
        return self._obj


class MockSessionRow:
    def __init__(self) -> None:
        self.match_score: int | None = None
        self.role_title: str | None = None
        self.role_key: str | None = None


def test_persist_writes_match_score_to_session():
    row = MockSessionRow()
    db = FakeSession(row)

    analyze_match(SAMPLE_JD, SAMPLE_RESUME, db=db, session_id="s1")

    assert row.match_score is not None
    assert 0 <= row.match_score <= 100


def test_persist_writes_role_key_to_session():
    row = MockSessionRow()
    db = FakeSession(row)

    analyze_match(SAMPLE_JD, SAMPLE_RESUME, db=db, session_id="s1")

    assert row.role_key is not None
    assert " " not in row.role_key


def test_persist_writes_role_title_to_session():
    row = MockSessionRow()
    db = FakeSession(row)

    analyze_match(SAMPLE_JD, SAMPLE_RESUME, db=db, session_id="s1")

    assert row.role_title is not None


def test_missing_session_does_not_raise():
    db = FakeSession(None)  # get() returns None — session not found
    result = analyze_match(SAMPLE_JD, SAMPLE_RESUME, db=db, session_id="nonexistent")
    assert isinstance(result, MatchAnalysisResult)


def test_no_db_no_persist():
    """analyze_match with no db/session_id must still return a valid result."""
    result = analyze_match(SAMPLE_JD, SAMPLE_RESUME)
    assert isinstance(result, MatchAnalysisResult)


# ── JSON parser helper ────────────────────────────────────────────────────────

def test_parse_llm_json_extracts_object():
    raw = 'Sure! Here is the analysis:\n{"role_key": "dev", "match_score": 80}'
    data = _parse_llm_json(raw)
    assert data["role_key"] == "dev"
    assert data["match_score"] == 80


def test_parse_llm_json_raises_on_no_json():
    with pytest.raises(ValueError, match="No JSON object found"):
        _parse_llm_json("This response has no JSON at all.")


# ── schema validation ─────────────────────────────────────────────────────────

def test_match_analysis_result_rejects_score_out_of_range():
    with pytest.raises(Exception):
        MatchAnalysisResult(
            role_title="Dev",
            role_key="dev",
            seniority_level="mid",
            match_score=150,
            matched_skills=[],
            missing_skills=[],
            risk_areas=[],
            interview_focus_areas=[],
        )
