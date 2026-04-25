"""Tests for GET /api/sessions/{session_id}/benchmark."""
from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.db import get_db
from app.main import app


# ── fake DB helpers ───────────────────────────────────────────────────────────

class _ScalarResult:
    """Mimics the chain result.scalars().first() / .all()."""

    def __init__(self, data: Any) -> None:
        self._data = data

    def scalars(self) -> "_ScalarResult":
        return self

    def first(self) -> Any:
        if isinstance(self._data, list):
            return self._data[0] if self._data else None
        return self._data

    def all(self) -> list:
        if self._data is None:
            return []
        return self._data if isinstance(self._data, list) else [self._data]


class FakeDB:
    """Minimal async-session stand-in for benchmark API tests."""

    def __init__(
        self,
        session: Any = None,
        comparison: Any = None,
        profiles: list[Any] | None = None,
    ) -> None:
        self._session = session
        self._execute_queue = [
            _ScalarResult(comparison),
            _ScalarResult(profiles or []),
        ]
        self._execute_idx = 0

    async def get(self, model_cls: type, pk: str) -> Any:
        return self._session

    async def execute(self, stmt: Any) -> _ScalarResult:
        result = self._execute_queue[self._execute_idx]
        self._execute_idx = min(self._execute_idx + 1, len(self._execute_queue) - 1)
        return result


class FakeSession:
    """Sentinel object representing a found InterviewSession row."""
    id: str = "sess-1"


class FakeComparisonRow:
    session_id: str = "sess-1"
    role_key: str = "project_manager"
    benchmark_profile_ids: list = ["bp-1"]
    benchmark_similarity_score: int = 65
    resume_competitiveness_score: int = 70
    evidence_strength_score: int = 60
    missing_skills: list = ["system design at scale"]
    weak_skills: list = ["cross-team delivery"]
    missing_metrics: list = ["team size led"]
    weak_ownership_signals: list = ["no P&L ownership"]
    interview_risk_areas: list = ["limited leadership evidence"]
    recommended_resume_fixes: list = ["add measurable outcomes"]
    question_targets: list = ["walk me through a project end-to-end"]


class FakeProfileRow:
    def __init__(self, pid: str = "bp-1") -> None:
        self.id = pid
        self.profile_name = "Benchmark PM 01"
        self.role_title = "Project Manager"
        self.seniority_level = "senior"
        self.quality_score = 90.0


# ── client fixture factory ────────────────────────────────────────────────────

def _make_client(db: FakeDB) -> TestClient:
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def _clear():
    app.dependency_overrides.clear()


# ── 404 — unknown session ─────────────────────────────────────────────────────

def test_unknown_session_returns_404():
    db = FakeDB(session=None)
    client = _make_client(db)
    try:
        response = client.get("/api/sessions/nonexistent-id/benchmark")
        assert response.status_code == 404
    finally:
        _clear()


def test_404_detail_message():
    db = FakeDB(session=None)
    client = _make_client(db)
    try:
        response = client.get("/api/sessions/nonexistent-id/benchmark")
        assert "not found" in response.json()["detail"].lower()
    finally:
        _clear()


# ── pending — session exists but no comparison yet ────────────────────────────

def test_pending_response_when_no_comparison():
    db = FakeDB(session=FakeSession(), comparison=None)
    client = _make_client(db)
    try:
        response = client.get("/api/sessions/sess-1/benchmark")
        assert response.status_code == 200
        assert response.json()["status"] == "pending"
    finally:
        _clear()


def test_pending_response_includes_session_id():
    db = FakeDB(session=FakeSession(), comparison=None)
    client = _make_client(db)
    try:
        response = client.get("/api/sessions/sess-1/benchmark")
        assert response.json()["session_id"] == "sess-1"
    finally:
        _clear()


# ── 200 — comparison ready ────────────────────────────────────────────────────

def test_ready_response_returns_200():
    db = FakeDB(
        session=FakeSession(),
        comparison=FakeComparisonRow(),
        profiles=[FakeProfileRow()],
    )
    client = _make_client(db)
    try:
        response = client.get("/api/sessions/sess-1/benchmark")
        assert response.status_code == 200
    finally:
        _clear()


def test_ready_response_has_session_id_and_role_key():
    db = FakeDB(
        session=FakeSession(),
        comparison=FakeComparisonRow(),
        profiles=[FakeProfileRow()],
    )
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        assert body["session_id"] == "sess-1"
        assert body["role_key"] == "project_manager"
    finally:
        _clear()


def test_ready_response_has_all_score_fields():
    db = FakeDB(
        session=FakeSession(),
        comparison=FakeComparisonRow(),
        profiles=[FakeProfileRow()],
    )
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        assert body["benchmark_similarity_score"] == 65
        assert body["resume_competitiveness_score"] == 70
        assert body["evidence_strength_score"] == 60
    finally:
        _clear()


def test_ready_response_has_all_list_fields():
    db = FakeDB(
        session=FakeSession(),
        comparison=FakeComparisonRow(),
        profiles=[FakeProfileRow()],
    )
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        for field in (
            "missing_skills", "weak_skills", "missing_metrics",
            "weak_ownership_signals", "interview_risk_areas",
            "recommended_resume_fixes", "question_targets",
        ):
            assert isinstance(body[field], list), f"{field} must be a list"
    finally:
        _clear()


def test_ready_response_list_field_values_preserved():
    db = FakeDB(
        session=FakeSession(),
        comparison=FakeComparisonRow(),
        profiles=[FakeProfileRow()],
    )
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        assert body["missing_skills"] == ["system design at scale"]
        assert body["question_targets"] == ["walk me through a project end-to-end"]
    finally:
        _clear()


def test_ready_response_includes_benchmark_profiles():
    db = FakeDB(
        session=FakeSession(),
        comparison=FakeComparisonRow(),
        profiles=[FakeProfileRow()],
    )
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        assert isinstance(body["benchmark_profiles"], list)
        assert len(body["benchmark_profiles"]) == 1
    finally:
        _clear()


def test_ready_response_profile_summary_fields():
    db = FakeDB(
        session=FakeSession(),
        comparison=FakeComparisonRow(),
        profiles=[FakeProfileRow("bp-1")],
    )
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        p = body["benchmark_profiles"][0]
        assert p["id"] == "bp-1"
        assert p["profile_name"] == "Benchmark PM 01"
        assert p["role_title"] == "Project Manager"
        assert p["seniority_level"] == "senior"
        assert p["quality_score"] == 90.0
    finally:
        _clear()


def test_ready_response_no_profiles_when_ids_empty():
    comparison = FakeComparisonRow()
    comparison.benchmark_profile_ids = []
    db = FakeDB(session=FakeSession(), comparison=comparison, profiles=[])
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        assert body["benchmark_profiles"] == []
    finally:
        _clear()


def test_ready_response_multiple_profiles():
    db = FakeDB(
        session=FakeSession(),
        comparison=FakeComparisonRow(),
        profiles=[FakeProfileRow("bp-1"), FakeProfileRow("bp-2")],
    )
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        assert len(body["benchmark_profiles"]) == 2
        ids = {p["id"] for p in body["benchmark_profiles"]}
        assert ids == {"bp-1", "bp-2"}
    finally:
        _clear()


def test_ready_response_null_scores_allowed():
    comparison = FakeComparisonRow()
    comparison.benchmark_similarity_score = None
    comparison.resume_competitiveness_score = None
    comparison.evidence_strength_score = None
    db = FakeDB(session=FakeSession(), comparison=comparison, profiles=[])
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        assert body["benchmark_similarity_score"] is None
        assert body["resume_competitiveness_score"] is None
        assert body["evidence_strength_score"] is None
    finally:
        _clear()


def test_ready_response_none_list_fields_coerced_to_empty():
    comparison = FakeComparisonRow()
    comparison.missing_skills = None
    comparison.weak_skills = None
    db = FakeDB(session=FakeSession(), comparison=comparison, profiles=[])
    client = _make_client(db)
    try:
        body = client.get("/api/sessions/sess-1/benchmark").json()
        assert body["missing_skills"] == []
        assert body["weak_skills"] == []
    finally:
        _clear()
