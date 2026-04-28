from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.db import get_db
from app.main import app
from app.models.answer import CandidateAnswer
from app.models.job import Job
from app.models.question import InterviewQuestion, QuestionCategory, ResponseMode


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
        now = datetime.now(UTC)
        if hasattr(item, "created_at") and item.created_at is None:
            item.created_at = now
        self.items[(type(item), item.id)] = item


@pytest.fixture
def fake_db() -> FakeSession:
    return FakeSession()


@pytest.fixture
def client(fake_db: FakeSession, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    async def override_get_db():
        yield fake_db

    monkeypatch.setattr("app.api.answers.default_queue.enqueue", lambda *args, **kwargs: None)
    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


def _question(
    fake_db: FakeSession,
    *,
    question_id: str,
    response_mode: ResponseMode,
    requires_audio: bool = False,
    requires_text: bool = False,
    requires_code: bool = False,
) -> InterviewQuestion:
    question = InterviewQuestion(
        id=question_id,
        session_id="session-1",
        question_number=1,
        category=QuestionCategory.TECHNICAL.value,
        question_text="Answer this question.",
        response_mode=response_mode.value,
        requires_audio=requires_audio,
        requires_video=False,
        requires_text=requires_text,
        requires_code=requires_code,
    )
    fake_db._persist(question)
    return question


def test_spoken_answer_upload_stores_audio(
    client: TestClient, fake_db: FakeSession, monkeypatch: pytest.MonkeyPatch
):
    _question(
        fake_db,
        question_id="question-spoken",
        response_mode=ResponseMode.SPOKEN_ANSWER,
        requires_audio=True,
    )
    stored: dict[str, Any] = {}

    monkeypatch.setattr(
        "app.api.answers.storage.new_object_key",
        lambda prefix, ext: f"{prefix}/answer.{ext}",
    )

    def fake_put_object(key: str, data: bytes, content_type: str) -> str:
        stored["key"] = key
        stored["data"] = data
        stored["content_type"] = content_type
        return key

    monkeypatch.setattr("app.api.answers.storage.put_object", fake_put_object)

    response = client.post(
        "/api/questions/question-spoken/answers",
        data={"answer_mode": "spoken_answer"},
        files={"audio": ("answer.webm", b"audio-bytes", "audio/webm")},
    )

    assert response.status_code == 200
    body = response.json()
    answer = fake_db.items[(CandidateAnswer, body["answer_id"])]
    assert body["processing_status"] == "queued"
    assert answer.answer_mode == "spoken_answer"
    assert answer.audio_object_key == "answers/audio/answer.webm"
    assert answer.transcription_status == "pending"
    assert answer.processing_status == "queued"
    assert stored["data"] == b"audio-bytes"
    assert stored["content_type"] == "audio/webm"


def test_spoken_answer_accepts_mediarecorder_audio_type_with_codec(
    client: TestClient, fake_db: FakeSession, monkeypatch: pytest.MonkeyPatch
):
    _question(
        fake_db,
        question_id="question-spoken-codec",
        response_mode=ResponseMode.SPOKEN_ANSWER,
        requires_audio=True,
    )
    stored: dict[str, Any] = {}

    monkeypatch.setattr(
        "app.api.answers.storage.new_object_key",
        lambda prefix, ext: f"{prefix}/answer.{ext}",
    )

    def fake_put_object(key: str, data: bytes, content_type: str) -> str:
        stored["key"] = key
        stored["data"] = data
        stored["content_type"] = content_type
        return key

    monkeypatch.setattr("app.api.answers.storage.put_object", fake_put_object)

    response = client.post(
        "/api/questions/question-spoken-codec/answers",
        data={"answer_mode": "spoken_answer"},
        files={"audio": ("answer.webm", b"audio-bytes", "audio/webm;codecs=opus")},
    )

    assert response.status_code == 200
    body = response.json()
    answer = fake_db.items[(CandidateAnswer, body["answer_id"])]
    assert answer.audio_object_key == "answers/audio/answer.webm"
    assert stored["data"] == b"audio-bytes"
    assert stored["content_type"] == "audio/webm;codecs=opus"


def test_written_answer_submission_stores_text(client: TestClient, fake_db: FakeSession):
    _question(
        fake_db,
        question_id="question-written",
        response_mode=ResponseMode.WRITTEN_ANSWER,
        requires_text=True,
    )

    response = client.post(
        "/api/questions/question-written/answers",
        json={"answer_mode": "written_answer", "text_answer": "Structured written response."},
    )

    assert response.status_code == 200
    answer = fake_db.items[(CandidateAnswer, response.json()["answer_id"])]
    assert answer.answer_mode == "written_answer"
    assert answer.text_answer == "Structured written response."
    assert answer.audio_object_key is None
    assert answer.transcription_status == "not_required"
    assert answer.processing_status == "queued"


def test_answer_submission_enqueues_processing_pipeline(
    fake_db: FakeSession, monkeypatch: pytest.MonkeyPatch
):
    enqueued: list[tuple[str, str]] = []

    def fake_enqueue(task_path: str, *args, **kwargs):
        enqueued.append((task_path, kwargs.get("job_id") or args[0]))

    monkeypatch.setattr("app.api.answers.default_queue.enqueue", fake_enqueue)

    async def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        _question(
            fake_db,
            question_id="question-enqueue",
            response_mode=ResponseMode.WRITTEN_ANSWER,
            requires_text=True,
        )

        response = client.post(
            "/api/questions/question-enqueue/answers",
            json={"answer_mode": "written_answer", "text_answer": "Structured response."},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert enqueued
    task_path, job_id = enqueued[0]
    assert task_path == "app.tasks.process_answer_pipeline.run"
    assert (Job, job_id) in fake_db.items


def test_answer_submission_stores_visual_signal_metadata(
    client: TestClient, fake_db: FakeSession
):
    _question(
        fake_db,
        question_id="question-video-metadata",
        response_mode=ResponseMode.WRITTEN_ANSWER,
        requires_text=True,
    )

    response = client.post(
        "/api/questions/question-video-metadata/answers",
        json={
            "answer_mode": "written_answer",
            "text_answer": "Structured written response.",
            "visual_signal_metadata": {
                "face_in_frame_ratio": 0.92,
                "lighting_quality": "good",
            },
        },
    )

    assert response.status_code == 200
    answer = fake_db.items[(CandidateAnswer, response.json()["answer_id"])]
    assert answer.visual_signal_metadata["face_in_frame_ratio"] == 0.92
    assert answer.visual_signal_metadata["lighting_quality"] == "good"


def test_code_answer_submission_stores_code_and_language(client: TestClient, fake_db: FakeSession):
    _question(
        fake_db,
        question_id="question-code",
        response_mode=ResponseMode.CODE_ANSWER,
        requires_code=True,
    )

    response = client.post(
        "/api/questions/question-code/answers",
        json={
            "answer_mode": "code_answer",
            "code_answer": "print('hello')",
            "code_language": "python",
        },
    )

    assert response.status_code == 200
    answer = fake_db.items[(CandidateAnswer, response.json()["answer_id"])]
    assert answer.answer_mode == "code_answer"
    assert answer.code_answer == "print('hello')"
    assert answer.code_language == "python"


def test_mixed_answer_submission_stores_audio_text_and_code(
    client: TestClient, fake_db: FakeSession, monkeypatch: pytest.MonkeyPatch
):
    _question(
        fake_db,
        question_id="question-mixed",
        response_mode=ResponseMode.MIXED_ANSWER,
        requires_audio=True,
        requires_text=True,
        requires_code=True,
    )
    monkeypatch.setattr(
        "app.api.answers.storage.new_object_key",
        lambda prefix, ext: f"{prefix}/mixed.{ext}",
    )
    monkeypatch.setattr("app.api.answers.storage.put_object", lambda *args, **kwargs: args[0])

    response = client.post(
        "/api/questions/question-mixed/answers",
        data={
            "answer_mode": "mixed_answer",
            "text_answer": "Explanation",
            "code_answer": "SELECT 1",
            "code_language": "sql",
        },
        files={"audio": ("mixed.ogg", b"audio", "audio/ogg")},
    )

    assert response.status_code == 200
    answer = fake_db.items[(CandidateAnswer, response.json()["answer_id"])]
    assert answer.answer_mode == "mixed_answer"
    assert answer.audio_object_key == "answers/audio/mixed.ogg"
    assert answer.text_answer == "Explanation"
    assert answer.code_answer == "SELECT 1"
    assert answer.code_language == "sql"


def test_answer_submission_unknown_question_returns_404(client: TestClient):
    response = client.post(
        "/api/questions/missing/answers",
        json={"answer_mode": "written_answer", "text_answer": "Answer"},
    )

    assert response.status_code == 404


def test_answer_submission_rejects_unsupported_audio_type(
    client: TestClient, fake_db: FakeSession
):
    _question(
        fake_db,
        question_id="question-audio",
        response_mode=ResponseMode.SPOKEN_ANSWER,
        requires_audio=True,
    )

    response = client.post(
        "/api/questions/question-audio/answers",
        data={"answer_mode": "spoken_answer"},
        files={"audio": ("answer.exe", b"binary", "application/octet-stream")},
    )

    assert response.status_code == 400


def test_answer_submission_rejects_unsupported_audio_mime_with_supported_extension(
    client: TestClient, fake_db: FakeSession
):
    _question(
        fake_db,
        question_id="question-audio-mime",
        response_mode=ResponseMode.SPOKEN_ANSWER,
        requires_audio=True,
    )

    response = client.post(
        "/api/questions/question-audio-mime/answers",
        data={"answer_mode": "spoken_answer"},
        files={"audio": ("answer.webm", b"binary", "application/octet-stream")},
    )

    assert response.status_code == 400


def test_answer_submission_rejects_audio_extension_mismatch(
    client: TestClient, fake_db: FakeSession
):
    _question(
        fake_db,
        question_id="question-audio-extension",
        response_mode=ResponseMode.SPOKEN_ANSWER,
        requires_audio=True,
    )

    response = client.post(
        "/api/questions/question-audio-extension/answers",
        data={"answer_mode": "spoken_answer"},
        files={"audio": ("answer.txt", b"audio", "audio/webm")},
    )

    assert response.status_code == 400


def test_answer_submission_rejects_oversized_audio(
    client: TestClient,
    fake_db: FakeSession,
    monkeypatch: pytest.MonkeyPatch,
):
    _question(
        fake_db,
        question_id="question-large-audio",
        response_mode=ResponseMode.SPOKEN_ANSWER,
        requires_audio=True,
    )
    monkeypatch.setattr("app.api.answers.settings.max_audio_upload_bytes", 4)

    response = client.post(
        "/api/questions/question-large-audio/answers",
        data={"answer_mode": "spoken_answer"},
        files={"audio": ("answer.webm", b"large audio", "audio/webm")},
    )

    assert response.status_code == 413


def test_answer_submission_validates_required_text(client: TestClient, fake_db: FakeSession):
    _question(
        fake_db,
        question_id="question-text-required",
        response_mode=ResponseMode.WRITTEN_ANSWER,
        requires_text=True,
    )

    response = client.post(
        "/api/questions/question-text-required/answers",
        json={"answer_mode": "written_answer", "text_answer": "   "},
    )

    assert response.status_code == 422


def test_answer_submission_rejects_invalid_answer_mode(
    client: TestClient, fake_db: FakeSession
):
    _question(
        fake_db,
        question_id="question-invalid-mode",
        response_mode=ResponseMode.WRITTEN_ANSWER,
        requires_text=True,
    )

    response = client.post(
        "/api/questions/question-invalid-mode/answers",
        json={"answer_mode": "essay", "text_answer": "Answer"},
    )

    assert response.status_code == 422
    assert "Unsupported answer mode" in response.json()["detail"]


def test_answer_submission_rejects_mode_mismatch(
    client: TestClient, fake_db: FakeSession
):
    _question(
        fake_db,
        question_id="question-mode-mismatch",
        response_mode=ResponseMode.CODE_ANSWER,
        requires_code=True,
    )

    response = client.post(
        "/api/questions/question-mode-mismatch/answers",
        json={"answer_mode": "written_answer", "text_answer": "Wrong mode"},
    )

    assert response.status_code == 422
    assert "must match question response mode" in response.json()["detail"]


def test_code_answer_submission_requires_language(client: TestClient, fake_db: FakeSession):
    _question(
        fake_db,
        question_id="question-code-language",
        response_mode=ResponseMode.CODE_ANSWER,
        requires_code=True,
    )

    response = client.post(
        "/api/questions/question-code-language/answers",
        json={"answer_mode": "code_answer", "code_answer": "SELECT 1"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Code language is required"


def test_answer_submission_rejects_invalid_visual_signal_metadata(
    client: TestClient, fake_db: FakeSession
):
    _question(
        fake_db,
        question_id="question-bad-visual-metadata",
        response_mode=ResponseMode.WRITTEN_ANSWER,
        requires_text=True,
    )

    response = client.post(
        "/api/questions/question-bad-visual-metadata/answers",
        json={
            "answer_mode": "written_answer",
            "text_answer": "Answer",
            "visual_signal_metadata": "[1, 2, 3]",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "visual_signal_metadata must be a JSON object"


def test_answer_submission_rejects_unsupported_content_type(
    client: TestClient, fake_db: FakeSession
):
    _question(
        fake_db,
        question_id="question-content-type",
        response_mode=ResponseMode.WRITTEN_ANSWER,
        requires_text=True,
    )

    response = client.post(
        "/api/questions/question-content-type/answers",
        content="answer_mode=written_answer&text_answer=Answer",
        headers={"content-type": "text/plain"},
    )

    assert response.status_code == 415
