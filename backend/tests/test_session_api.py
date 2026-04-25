from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.db import get_db
from app.main import app


class FakeSession:
    def __init__(self) -> None:
        self.items: dict[str, Any] = {}
        self.pending: Any | None = None

    def add(self, item: Any) -> None:
        self.pending = item

    async def commit(self) -> None:
        if self.pending is not None:
            if self.pending.id is None:
                self.pending.id = str(uuid.uuid4())
            now = datetime.now(UTC)
            if self.pending.created_at is None:
                self.pending.created_at = now
            if self.pending.updated_at is None:
                self.pending.updated_at = now
            if hasattr(self.pending, "current_question_index") and self.pending.current_question_index is None:
                self.pending.current_question_index = 0
            self.items[self.pending.id] = self.pending

    async def refresh(self, item: Any) -> None:
        if item.id is None:
            item.id = str(uuid.uuid4())
        now = datetime.now(UTC)
        if item.created_at is None:
            item.created_at = now
        if item.updated_at is None:
            item.updated_at = now
        if hasattr(item, "current_question_index") and item.current_question_index is None:
            item.current_question_index = 0
        self.items[item.id] = item

    async def get(self, model: type, item_id: str) -> Any | None:
        return self.items.get(item_id)


@pytest.fixture
def client() -> TestClient:
    fake_db = FakeSession()

    async def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


def test_create_session_starts_in_draft_status(client: TestClient):
    response = client.post(
        "/api/sessions",
        json={"job_description": "Sample JD", "resume_text": "Sample resume"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "draft"
    assert body["session_id"]


def test_create_session_rejects_empty_job_description(client: TestClient):
    response = client.post(
        "/api/sessions",
        json={"job_description": "   ", "resume_text": "Sample resume"},
    )

    assert response.status_code == 422


def test_get_session_returns_benchmark_aware_state_fields(client: TestClient):
    created = client.post(
        "/api/sessions",
        json={
            "job_description": "Sample JD",
            "resume_text": "Sample resume",
            "role_title": "Backend Developer",
            "company_name": "Acme",
        },
    ).json()

    response = client.get(f"/api/sessions/{created['session_id']}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created["session_id"]
    assert body["status"] == "draft"
    assert body["role_title"] == "Backend Developer"
    assert body["company_name"] == "Acme"
    assert body["match_score"] is None
    assert body["benchmark_similarity_score"] is None
    assert body["resume_competitiveness_score"] is None
    assert body["evidence_strength_score"] is None


def test_get_unknown_session_returns_404(client: TestClient):
    response = client.get("/api/sessions/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_prepare_session_enqueues_job(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    enqueued: list[tuple[str, str]] = []

    def fake_enqueue(task_path: str, *args, **kwargs):
        enqueued.append((task_path, kwargs.get("job_id") or args[0]))

    monkeypatch.setattr("app.api.sessions.default_queue.enqueue", fake_enqueue)
    created = client.post(
        "/api/sessions",
        json={"job_description": "Sample JD", "resume_text": "Sample resume"},
    ).json()

    response = client.post(f"/api/sessions/{created['session_id']}/prepare")

    assert response.status_code == 200
    body = response.json()
    assert body["job_id"]
    assert body["status"] == "queued"
    assert enqueued == [("app.tasks.prepare_session.run", body["job_id"])]


def test_prepare_unknown_session_returns_404(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("app.api.sessions.default_queue.enqueue", lambda *args, **kwargs: None)

    response = client.post("/api/sessions/missing-session/prepare")

    assert response.status_code == 404
