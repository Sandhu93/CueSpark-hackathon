from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.db import get_db
from app.main import app
from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.evaluation import AnswerEvaluation
from app.models.job import Job
from app.models.question import InterviewQuestion, QuestionCategory, ResponseMode
from app.models.report import InterviewReport
from app.models.session import InterviewSession


class FakeResult:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    def scalars(self) -> "FakeResult":
        return self

    def all(self) -> list[Any]:
        return self.rows

    def first(self) -> Any | None:
        return self.rows[0] if self.rows else None


class FakeSession:
    def __init__(self) -> None:
        self.items: dict[tuple[type, str], Any] = {}
        self.pending: list[Any] = []
        self.questions: list[InterviewQuestion] = []
        self.agent_results: list[AgentResult] = []
        self.evaluations: list[AnswerEvaluation] = []
        self.reports: list[InterviewReport] = []

    async def get(self, model: type, item_id: str) -> Any | None:
        return self.items.get((model, item_id))

    async def execute(self, stmt: Any) -> FakeResult:
        entity = stmt.column_descriptions[0].get("entity")
        if entity is InterviewQuestion:
            return FakeResult(self.questions)
        if entity is AgentResult:
            return FakeResult(self.agent_results)
        if entity is AnswerEvaluation:
            return FakeResult(self.evaluations)
        if entity is InterviewReport:
            return FakeResult(self.reports)
        return FakeResult([])

    def add(self, item: Any) -> None:
        self.pending.append(item)

    async def commit(self) -> None:
        for item in self.pending:
            self.persist(item)
        self.pending.clear()

    async def refresh(self, item: Any) -> None:
        self.persist(item)

    def persist(self, item: Any) -> None:
        if getattr(item, "id", None) is None:
            item.id = f"generated-{len(self.items) + len(self.pending)}"
        now = datetime.now(UTC).replace(tzinfo=None)
        if getattr(item, "created_at", None) is None:
            item.created_at = now
        if getattr(item, "updated_at", None) is None:
            item.updated_at = now
        self.items[(type(item), item.id)] = item
        if isinstance(item, InterviewQuestion) and item not in self.questions:
            self.questions.append(item)
        if isinstance(item, AgentResult) and item not in self.agent_results:
            self.agent_results.append(item)
        if isinstance(item, AnswerEvaluation) and item not in self.evaluations:
            self.evaluations.append(item)
        if isinstance(item, InterviewReport) and item not in self.reports:
            self.reports.append(item)


@pytest.fixture
def fake_db() -> FakeSession:
    db = FakeSession()
    session = InterviewSession(
        id="session-1",
        job_description_text="Backend role.",
        resume_text="Resume text.",
        status="ready",
    )
    question = InterviewQuestion(
        id="question-1",
        session_id="session-1",
        question_number=1,
        category=QuestionCategory.BENCHMARK_GAP_VALIDATION.value,
        question_text="Prove ownership with metrics.",
        source="benchmark_gap",
        benchmark_gap_refs=["weak ownership proof"],
        response_mode=ResponseMode.WRITTEN_ANSWER.value,
        requires_audio=False,
        requires_text=True,
        requires_code=False,
        requires_video=False,
    )
    answer = CandidateAnswer(
        id="answer-1",
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.WRITTEN_ANSWER.value,
        text_answer="I owned the API and reduced p95 latency.",
        transcription_status="not_required",
        processing_status="evaluated",
    )
    agent_result = AgentResult(
        id="agent-1",
        answer_id="answer-1",
        agent_type=AgentType.BENCHMARK_GAP.value,
        status=AgentResultStatus.SUCCEEDED.value,
        score=7,
        payload={"benchmark_gap_coverage_score": 7},
    )
    evaluation = AnswerEvaluation(
        id="evaluation-1",
        answer_id="answer-1",
        overall_score=72,
        benchmark_gap_coverage_score=70,
        strict_feedback="Usable answer with some benchmark evidence.",
    )
    report = InterviewReport(
        id="report-1",
        session_id="session-1",
        readiness_score=70,
        hiring_recommendation="maybe",
        summary="Moderate readiness signal.",
    )
    for item in (session, question, answer, agent_result, evaluation, report):
        db.persist(item)
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


def test_session_questions_endpoint_returns_generated_questions(client: TestClient):
    response = client.get("/api/sessions/session-1/questions")

    assert response.status_code == 200
    body = response.json()
    assert body["questions"][0]["id"] == "question-1"
    assert body["questions"][0]["response_mode"] == "written_answer"
    assert body["questions"][0]["tts_audio_url"] is None


def test_question_tts_create_and_get_endpoints(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr("app.services.question_audio.storage.put_object", lambda *args, **kwargs: args[0])
    monkeypatch.setattr(
        "app.services.question_audio.storage.presigned_get_url",
        lambda key: f"http://minio.local/{key}",
    )

    create_response = client.post("/api/questions/question-1/tts")
    get_response = client.get("/api/questions/question-1/tts")

    assert create_response.status_code == 200
    assert create_response.json()["audio_url"].endswith("audio/questions/question-1.wav")
    assert get_response.status_code == 200
    assert get_response.json()["audio_url"].endswith("audio/questions/question-1.wav")


def test_answer_read_endpoint_includes_agent_results_and_evaluation(client: TestClient):
    response = client.get("/api/answers/answer-1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "answer-1"
    assert body["agent_results"][0]["agent_type"] == "benchmark_gap"
    assert body["evaluation"]["overall_score"] == 72


def test_answer_agent_results_endpoint(client: TestClient):
    response = client.get("/api/answers/answer-1/agent-results")

    assert response.status_code == 200
    body = response.json()
    assert body["answer_id"] == "answer-1"
    assert body["agent_results"][0]["status"] == "succeeded"


def test_report_generate_endpoint_enqueues_report_job(
    client: TestClient,
    fake_db: FakeSession,
    monkeypatch: pytest.MonkeyPatch,
):
    enqueued: list[tuple[str, str]] = []
    monkeypatch.setattr(
        "app.api.reports.default_queue.enqueue",
        lambda task_path, *args, **kwargs: enqueued.append((task_path, kwargs.get("job_id") or args[0])),
    )

    response = client.post("/api/sessions/session-1/report")

    assert response.status_code == 200
    body = response.json()
    assert body["kind"] == "generate_report"
    assert enqueued == [("app.tasks.generate_report.run", body["id"])]
    assert (Job, body["id"]) in fake_db.items


def test_report_read_endpoint_returns_latest_report(client: TestClient):
    response = client.get("/api/sessions/session-1/report")

    assert response.status_code == 200
    body = response.json()
    assert body["readiness_score"] == 70
    assert body["summary"] == "Moderate readiness signal."
