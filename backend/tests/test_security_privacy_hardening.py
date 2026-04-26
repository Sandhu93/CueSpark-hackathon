from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.ai_mock import mock_text_response


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_generic_upload_init_rejects_unsupported_file_type(client: TestClient):
    response = client.post(
        "/uploads/init",
        json={"filename": "payload.exe", "content_type": "application/octet-stream"},
    )

    assert response.status_code == 400


def test_generic_direct_upload_rejects_oversized_file(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr("app.api.uploads.settings.max_generic_upload_bytes", 4)

    response = client.post(
        "/uploads/direct",
        files={"file": ("resume.txt", b"large upload", "text/plain")},
    )

    assert response.status_code == 413


def test_generic_upload_response_uses_signed_download_url_name(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr("app.api.uploads.storage.presigned_put_url", lambda key: f"http://put/{key}")
    monkeypatch.setattr("app.api.uploads.storage.presigned_get_url", lambda key: f"http://get/{key}")

    response = client.post(
        "/uploads/init",
        json={"filename": "resume.txt", "content_type": "text/plain"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "download_url" in body
    assert "public_url" not in body


def test_mock_ai_response_does_not_echo_sensitive_prompt():
    prompt = "Candidate resume: private phone number 555-0100 and transcript text"

    response = mock_text_response(prompt)

    assert "555-0100" not in response
    assert "private phone" not in response
