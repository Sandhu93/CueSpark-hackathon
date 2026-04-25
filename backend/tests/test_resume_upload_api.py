from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.db import get_db
from app.main import app
from app.models.document import Document
from app.models.session import InterviewSession


class FakeSession:
    def __init__(self) -> None:
        self.items: dict[tuple[type, str], Any] = {}
        self.pending: list[Any] = []

    def add(self, item: Any) -> None:
        self.pending.append(item)

    async def commit(self) -> None:
        for item in self.pending:
            self._persist(item)
        self.pending.clear()

    async def refresh(self, item: Any) -> None:
        self._persist(item)

    async def get(self, model: type, item_id: str) -> Any | None:
        return self.items.get((model, item_id))

    def _persist(self, item: Any) -> None:
        if item.id is None:
            item.id = str(uuid.uuid4())
        now = datetime.utcnow()
        if hasattr(item, "created_at") and item.created_at is None:
            item.created_at = now
        if hasattr(item, "updated_at") and item.updated_at is None:
            item.updated_at = now
        if hasattr(item, "current_question_index") and item.current_question_index is None:
            item.current_question_index = 0
        self.items[(type(item), item.id)] = item


@pytest.fixture
def fake_db() -> FakeSession:
    db = FakeSession()
    session = InterviewSession(
        id="session-id",
        job_description_text="Sample JD",
        status="draft",
    )
    db._persist(session)
    return db


@pytest.fixture
def client(fake_db: FakeSession) -> TestClient:
    async def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


def test_resume_upload_stores_file_and_document_row(
    client: TestClient, fake_db: FakeSession, monkeypatch: pytest.MonkeyPatch
):
    stored: dict[str, Any] = {}

    def fake_put_object(key: str, data: bytes, content_type: str) -> str:
        stored["key"] = key
        stored["data"] = data
        stored["content_type"] = content_type
        return key

    monkeypatch.setattr("app.services.documents.storage.put_object", fake_put_object)
    monkeypatch.setattr(
        "app.services.documents.storage.new_object_key",
        lambda prefix, ext: f"{prefix}/resume.{ext}",
    )

    response = client.post(
        "/api/sessions/session-id/resume",
        files={
            "file": (
                "resume.txt",
                b"Experienced backend developer with Python, APIs, and production ownership.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["parse_status"] == "parsed"
    document = fake_db.items[(Document, body["document_id"])]
    assert document.document_type == "resume"
    assert document.input_type == "upload"
    assert document.object_key == "resumes/original/session-id/resume.txt"
    assert document.extracted_text == (
        "Experienced backend developer with Python, APIs, and production ownership."
    )
    assert stored["data"] == b"Experienced backend developer with Python, APIs, and production ownership."
    assert stored["content_type"] == "text/plain"


def test_resume_upload_rejects_unsupported_file_type(client: TestClient):
    response = client.post(
        "/api/sessions/session-id/resume",
        files={"file": ("resume.exe", b"binary", "application/octet-stream")},
    )

    assert response.status_code == 400


def test_resume_upload_unknown_session_returns_404(client: TestClient):
    response = client.post(
        "/api/sessions/missing/resume",
        files={"file": ("resume.txt", b"resume text", "text/plain")},
    )

    assert response.status_code == 404
