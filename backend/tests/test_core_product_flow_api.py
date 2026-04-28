from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.db import get_db
from app.main import app
from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.benchmark_comparison import BenchmarkComparison
from app.models.benchmark_profile import BenchmarkProfile, BenchmarkSourceType
from app.models.document import Document
from app.models.evaluation import AnswerEvaluation
from app.models.job import Job
from app.models.question import InterviewQuestion, QuestionCategory, QuestionSource, ResponseMode
from app.models.report import InterviewReport
from app.models.session import InterviewSession, InterviewSessionStatus
from app.schemas.benchmark import BenchmarkAnalysisResult
from app.schemas.match import MatchAnalysisResult
from app.services.report_generator import generate_multimodal_readiness_report
from app.tasks import prepare_session as prepare_task
from app.tasks import process_answer_pipeline as answer_pipeline


SAMPLE_JD = (
    "We need a Senior Backend Engineer with FastAPI, PostgreSQL, scalable APIs, "
    "debugging ownership, production reliability, and measurable business impact."
)
SAMPLE_RESUME = (
    "Backend engineer with API and PostgreSQL experience. Built services and supported "
    "production systems, but resume evidence has limited metrics and ownership proof."
)


class FakeResult:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    def scalars(self) -> "FakeResult":
        return self

    def all(self) -> list[Any]:
        return self.rows

    def first(self) -> Any | None:
        return self.rows[0] if self.rows else None


class SharedStore:
    def __init__(self) -> None:
        self.items: dict[tuple[type, str], Any] = {}
        self.pending: list[Any] = []
        self.benchmark_profiles: list[BenchmarkProfile] = []
        self.benchmark_comparisons: list[BenchmarkComparison] = []
        self.documents: list[Document] = []
        self.questions: list[InterviewQuestion] = []
        self.answers: list[CandidateAnswer] = []
        self.agent_results: list[AgentResult] = []
        self.evaluations: list[AnswerEvaluation] = []
        self.reports: list[InterviewReport] = []

    def persist(self, item: Any) -> None:
        if getattr(item, "id", None) is None:
            item.id = str(uuid.uuid4())
        now = datetime.now(UTC).replace(tzinfo=None)
        if getattr(item, "created_at", None) is None:
            item.created_at = now
        if hasattr(item, "updated_at") and getattr(item, "updated_at", None) is None:
            item.updated_at = now
        self._default_json_fields(item)

        self.items[(type(item), item.id)] = item
        self._append_unique(item)

    def get(self, model: type, item_id: str) -> Any | None:
        return self.items.get((model, item_id))

    def add_pending(self, item: Any) -> None:
        self.pending.append(item)

    def commit_pending(self) -> None:
        for item in self.pending:
            self.persist(item)
        self.pending.clear()

    def rows_for(self, entity: type | None) -> list[Any]:
        if entity is BenchmarkComparison:
            return self.benchmark_comparisons
        if entity is BenchmarkProfile:
            return self.benchmark_profiles
        if entity is Document:
            return self.documents
        if entity is InterviewQuestion:
            return sorted(self.questions, key=lambda q: q.question_number)
        if entity is CandidateAnswer:
            return self.answers
        if entity is AgentResult:
            return self.agent_results
        if entity is AnswerEvaluation:
            return self.evaluations
        if entity is InterviewReport:
            return sorted(self.reports, key=lambda r: r.created_at or datetime.min, reverse=True)
        return []

    def _append_unique(self, item: Any) -> None:
        collections = [
            (BenchmarkProfile, self.benchmark_profiles),
            (BenchmarkComparison, self.benchmark_comparisons),
            (Document, self.documents),
            (InterviewQuestion, self.questions),
            (CandidateAnswer, self.answers),
            (AgentResult, self.agent_results),
            (AnswerEvaluation, self.evaluations),
            (InterviewReport, self.reports),
        ]
        for model, rows in collections:
            if isinstance(item, model) and item not in rows:
                rows.append(item)

    def _default_json_fields(self, item: Any) -> None:
        for field_name in (
            "benchmark_profile_ids",
            "missing_skills",
            "weak_skills",
            "missing_metrics",
            "weak_ownership_signals",
            "missing_project_depth",
            "interview_risk_areas",
            "recommended_resume_fixes",
            "question_targets",
            "benchmark_gap_refs",
            "skill_gaps",
            "benchmark_gaps",
            "answer_feedback",
            "red_flags",
        ):
            if hasattr(item, field_name) and getattr(item, field_name, None) is None:
                setattr(item, field_name, [])
        for field_name in (
            "metadata_",
            "provenance",
            "communication_metrics",
            "communication_metadata",
            "visual_signal_metadata",
            "payload",
            "result",
            "input",
            "modality_breakdown",
            "multimodal_summary",
        ):
            if hasattr(item, field_name) and getattr(item, field_name, None) is None:
                setattr(item, field_name, {})
        if isinstance(item, InterviewSession) and item.current_question_index is None:
            item.current_question_index = 0


class ApiDB:
    def __init__(self, store: SharedStore) -> None:
        self.store = store

    def add(self, item: Any) -> None:
        self.store.add_pending(item)

    async def commit(self) -> None:
        self.store.commit_pending()

    async def refresh(self, item: Any) -> None:
        self.store.persist(item)

    async def get(self, model: type, item_id: str) -> Any | None:
        return self.store.get(model, item_id)

    async def execute(self, stmt: Any) -> FakeResult:
        entity = _statement_entity(stmt)
        return FakeResult(self.store.rows_for(entity))


class WorkerDB:
    def __init__(self, store: SharedStore) -> None:
        self.store = store

    def add(self, item: Any) -> None:
        self.store.persist(item)

    def get(self, model: type, item_id: str) -> Any | None:
        return self.store.get(model, item_id)

    def execute(self, stmt: Any) -> FakeResult:
        entity = _statement_entity(stmt)
        return FakeResult(self.store.rows_for(entity))


def _statement_entity(stmt: Any) -> type | None:
    descriptions = getattr(stmt, "column_descriptions", None) or []
    if not descriptions:
        return None
    return descriptions[0].get("entity")


@pytest.fixture
def store() -> SharedStore:
    return SharedStore()


@pytest.fixture
def client(store: SharedStore) -> TestClient:
    api_db = ApiDB(store)

    async def override_get_db():
        yield api_db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


def test_core_product_path_runs_with_mock_mode(
    client: TestClient,
    store: SharedStore,
    monkeypatch: pytest.MonkeyPatch,
):
    worker_db = WorkerDB(store)
    enqueued: list[tuple[str, str]] = []
    monkeypatch.setattr("app.api.sessions.default_queue.enqueue", _capture_enqueue(enqueued))
    monkeypatch.setattr("app.api.answers.default_queue.enqueue", _capture_enqueue(enqueued))
    monkeypatch.setattr("app.api.reports.default_queue.enqueue", _capture_enqueue(enqueued))
    monkeypatch.setattr("app.api.answers.storage.new_object_key", lambda prefix, ext: f"{prefix}/answer.{ext}")
    monkeypatch.setattr("app.api.answers.storage.put_object", lambda key, data, content_type: key)
    monkeypatch.setattr("app.services.question_audio.storage.put_object", lambda key, data, content_type: key)
    monkeypatch.setattr(
        "app.services.question_audio.storage.presigned_get_url",
        lambda key: f"http://minio.local/{key}",
    )
    _patch_prepare_pipeline(monkeypatch, store)
    _patch_answer_pipeline(monkeypatch, store)

    session_id = _create_session(client)
    prepare_response = client.post(f"/api/sessions/{session_id}/prepare")
    assert prepare_response.status_code == 200
    assert enqueued[-1][0] == "app.tasks.prepare_session.run"

    preparation = prepare_task.prepare_session(worker_db, session_id)
    assert preparation["status"] == InterviewSessionStatus.READY.value
    assert preparation["question_count"] == 1

    session_response = client.get(f"/api/sessions/{session_id}")
    assert session_response.status_code == 200
    assert session_response.json()["status"] == "ready"

    benchmark_response = client.get(f"/api/sessions/{session_id}/benchmark")
    assert benchmark_response.status_code == 200
    benchmark_body = benchmark_response.json()
    assert benchmark_body["benchmark_similarity_score"] == 64
    assert "missing reliability metrics" in benchmark_body["missing_metrics"]

    questions_response = client.get(f"/api/sessions/{session_id}/questions")
    assert questions_response.status_code == 200
    question = questions_response.json()["questions"][0]
    assert question["source"] == QuestionSource.BENCHMARK_GAP.value
    assert question["benchmark_gap_refs"] == ["weak ownership proof"]

    tts_response = client.post(f"/api/questions/{question['id']}/tts")
    assert tts_response.status_code == 200
    assert tts_response.json()["audio_url"].endswith(f"audio/questions/{question['id']}.wav")

    answer_response = client.post(
        f"/api/questions/{question['id']}/answers",
        data={"answer_mode": ResponseMode.SPOKEN_ANSWER.value},
        files={"audio": ("answer.webm", b"mock-audio", "audio/webm")},
    )
    assert answer_response.status_code == 200
    answer_id = answer_response.json()["answer_id"]
    assert enqueued[-1][0] == "app.tasks.process_answer_pipeline.run"

    pipeline_result = answer_pipeline.process_answer_pipeline(worker_db, answer_id)
    assert pipeline_result["processing_status"] == "evaluated"
    assert {row.agent_type for row in store.agent_results} >= {
        AgentType.AUDIO.value,
        AgentType.BENCHMARK_GAP.value,
    }
    assert store.evaluations[0].overall_score is not None

    answer_read_response = client.get(f"/api/answers/{answer_id}")
    assert answer_read_response.status_code == 200
    answer_body = answer_read_response.json()
    assert answer_body["evaluation"]["overall_score"] == store.evaluations[0].overall_score
    assert {row["agent_type"] for row in answer_body["agent_results"]} >= {
        AgentType.AUDIO.value,
        AgentType.BENCHMARK_GAP.value,
    }

    report_job_response = client.post(f"/api/sessions/{session_id}/report")
    assert report_job_response.status_code == 200
    assert enqueued[-1][0] == "app.tasks.generate_report.run"
    generate_multimodal_readiness_report(worker_db, session_id)

    report_response = client.get(f"/api/sessions/{session_id}/report")
    assert report_response.status_code == 200
    report = report_response.json()
    assert report["readiness_score"] is not None
    assert "weak ownership proof" in report["benchmark_gaps"]
    assert report["answer_feedback"][0]["answer_id"] == answer_id
    assert report["communication_summary"]


def test_product_path_missing_resources_return_clear_api_errors(client: TestClient):
    assert client.get("/api/questions/missing-question/tts").status_code == 404
    assert client.post("/api/questions/missing-question/tts").status_code == 404
    assert client.get("/api/answers/missing-answer").status_code == 404
    assert client.get("/api/answers/missing-answer/agent-results").status_code == 404
    assert client.post("/api/sessions/missing-session/report").status_code == 404
    assert client.get("/api/sessions/missing-session/report").status_code == 404


def test_answer_submission_accepts_written_code_and_mixed_modes(
    client: TestClient,
    store: SharedStore,
    monkeypatch: pytest.MonkeyPatch,
):
    enqueued: list[tuple[str, str]] = []
    monkeypatch.setattr("app.api.answers.default_queue.enqueue", _capture_enqueue(enqueued))
    monkeypatch.setattr("app.api.answers.storage.new_object_key", lambda prefix, ext: f"{prefix}/answer.{ext}")
    monkeypatch.setattr("app.api.answers.storage.put_object", lambda key, data, content_type: key)
    session = InterviewSession(
        id="session-multimodal",
        status=InterviewSessionStatus.READY.value,
        job_description_text=SAMPLE_JD,
        resume_text=SAMPLE_RESUME,
    )
    store.persist(session)
    written_question = _persist_question(
        store,
        question_id="question-written",
        session_id=session.id,
        question_number=1,
        response_mode=ResponseMode.WRITTEN_ANSWER,
        requires_text=True,
    )
    code_question = _persist_question(
        store,
        question_id="question-code",
        session_id=session.id,
        question_number=2,
        response_mode=ResponseMode.CODE_ANSWER,
        requires_code=True,
    )
    mixed_question = _persist_question(
        store,
        question_id="question-mixed",
        session_id=session.id,
        question_number=3,
        response_mode=ResponseMode.MIXED_ANSWER,
        requires_audio=True,
        requires_text=True,
        requires_code=True,
        requires_video=True,
    )

    written_response = client.post(
        f"/api/questions/{written_question.id}/answers",
        json={
            "answer_mode": ResponseMode.WRITTEN_ANSWER.value,
            "text_answer": "Context, action, evidence, and measurable result.",
        },
    )
    assert written_response.status_code == 200
    written_answer = store.get(CandidateAnswer, written_response.json()["answer_id"])
    assert written_answer.answer_mode == ResponseMode.WRITTEN_ANSWER.value
    assert written_answer.text_answer == "Context, action, evidence, and measurable result."

    code_response = client.post(
        f"/api/questions/{code_question.id}/answers",
        json={
            "answer_mode": ResponseMode.CODE_ANSWER.value,
            "code_answer": "def solve(items):\n    return len(items)",
            "code_language": "python",
        },
    )
    assert code_response.status_code == 200
    code_answer = store.get(CandidateAnswer, code_response.json()["answer_id"])
    assert code_answer.answer_mode == ResponseMode.CODE_ANSWER.value
    assert code_answer.code_language == "python"
    assert "def solve" in code_answer.code_answer

    mixed_response = client.post(
        f"/api/questions/{mixed_question.id}/answers",
        data={
            "answer_mode": ResponseMode.MIXED_ANSWER.value,
            "text_answer": "I would first clarify constraints and success metrics.",
            "code_answer": "SELECT count(*) FROM events;",
            "code_language": "sql",
            "visual_signal_metadata": (
                '{"face_in_frame_ratio":0.95,"safe_signal_labels":["face in frame"]}'
            ),
        },
        files={"audio": ("answer.webm", b"mock-audio", "audio/webm")},
    )
    assert mixed_response.status_code == 200
    mixed_answer = store.get(CandidateAnswer, mixed_response.json()["answer_id"])
    assert mixed_answer.answer_mode == ResponseMode.MIXED_ANSWER.value
    assert mixed_answer.audio_object_key == "answers/audio/answer.webm"
    assert mixed_answer.text_answer == "I would first clarify constraints and success metrics."
    assert mixed_answer.code_answer == "SELECT count(*) FROM events;"
    assert mixed_answer.code_language == "sql"
    assert mixed_answer.visual_signal_metadata["safe_signal_labels"] == ["face in frame"]
    assert len(enqueued) == 3


def _capture_enqueue(enqueued: list[tuple[str, str]]):
    def fake_enqueue(task_path: str, *args: Any, **kwargs: Any) -> None:
        enqueued.append((task_path, str(kwargs.get("job_id") or args[0])))

    return fake_enqueue


def _create_session(client: TestClient) -> str:
    response = client.post(
        "/api/sessions",
        json={
            "job_description": SAMPLE_JD,
            "resume_text": SAMPLE_RESUME,
            "role_title": "Senior Backend Engineer",
            "company_name": "Acme",
        },
    )
    assert response.status_code == 201
    return str(response.json()["session_id"])


def _persist_question(
    store: SharedStore,
    *,
    question_id: str,
    session_id: str,
    question_number: int,
    response_mode: ResponseMode,
    requires_audio: bool = False,
    requires_video: bool = False,
    requires_text: bool = False,
    requires_code: bool = False,
) -> InterviewQuestion:
    question = InterviewQuestion(
        id=question_id,
        session_id=session_id,
        question_number=question_number,
        category=QuestionCategory.BENCHMARK_GAP_VALIDATION.value,
        question_text="Answer this benchmark-driven question.",
        expected_signal="Mode-specific response evidence.",
        difficulty="medium",
        source=QuestionSource.BENCHMARK_GAP.value,
        benchmark_gap_refs=["mock validation gap"],
        why_this_was_asked="Benchmark gap: mock validation gap",
        response_mode=response_mode.value,
        requires_audio=requires_audio,
        requires_video=requires_video,
        requires_text=requires_text,
        requires_code=requires_code,
    )
    store.persist(question)
    return question


def _patch_prepare_pipeline(monkeypatch: pytest.MonkeyPatch, store: SharedStore) -> None:
    profile = BenchmarkProfile(
        id="benchmark-profile-1",
        role_key="backend_engineer",
        role_title="Backend Engineer",
        seniority_level="senior",
        domain="engineering",
        profile_name="Backend benchmark profile",
        resume_text="Strong profile with ownership, metrics, and reliability depth.",
        skills=["FastAPI", "PostgreSQL", "reliability"],
        tools=["PostgreSQL"],
        project_signals=["Owned API reliability project"],
        impact_signals=["Reduced latency by 35%"],
        ownership_signals=["Led production rollout"],
        source_type=BenchmarkSourceType.CURATED.value,
        is_curated=True,
        quality_score=88,
    )
    store.persist(profile)

    monkeypatch.setattr(prepare_task, "embed_and_store", lambda *args, **kwargs: [object(), object()])
    monkeypatch.setattr(prepare_task, "retrieve_benchmark_profiles", lambda *args, **kwargs: [profile])

    def fake_analyze_match(*args: Any, **kwargs: Any) -> MatchAnalysisResult:
        session = store.get(InterviewSession, str(kwargs["session_id"]))
        session.role_key = "backend_engineer"
        session.match_score = 71
        return MatchAnalysisResult(
            role_title="Senior Backend Engineer",
            role_key="backend_engineer",
            seniority_level="senior",
            match_score=71,
            matched_skills=["FastAPI", "PostgreSQL"],
            missing_skills=["observability"],
            risk_areas=["weak metrics"],
            interview_focus_areas=["ownership proof"],
        )

    def fake_benchmark_analysis(*args: Any, **kwargs: Any) -> BenchmarkAnalysisResult:
        session_id = str(kwargs["session_id"])
        session = store.get(InterviewSession, session_id)
        session.benchmark_similarity_score = 64
        session.resume_competitiveness_score = 58
        session.evidence_strength_score = 52
        comparison = BenchmarkComparison(
            session_id=session_id,
            role_key="backend_engineer",
            benchmark_profile_ids=[profile.id],
            benchmark_similarity_score=64,
            resume_competitiveness_score=58,
            evidence_strength_score=52,
            missing_skills=["observability"],
            weak_skills=["production debugging"],
            missing_metrics=["missing reliability metrics"],
            weak_ownership_signals=["weak ownership proof"],
            interview_risk_areas=["strict interviewer will challenge ownership depth"],
            recommended_resume_fixes=["Add quantified production impact."],
            question_targets=["weak ownership proof"],
        )
        store.persist(comparison)
        return BenchmarkAnalysisResult(
            benchmark_similarity_score=64,
            resume_competitiveness_score=58,
            evidence_strength_score=52,
            missing_skills=["observability"],
            weak_skills=["production debugging"],
            missing_metrics=["missing reliability metrics"],
            weak_ownership_signals=["weak ownership proof"],
            interview_risk_areas=["strict interviewer will challenge ownership depth"],
            recommended_resume_fixes=["Add quantified production impact."],
            question_targets=["weak ownership proof"],
        )

    def fake_generate_questions(*args: Any, **kwargs: Any) -> list[InterviewQuestion]:
        question = InterviewQuestion(
            session_id=str(kwargs["session_id"]),
            question_number=1,
            category=QuestionCategory.BENCHMARK_GAP_VALIDATION.value,
            question_text="Walk me through a time you owned a production reliability issue.",
            expected_signal="Concrete ownership, metrics, and production impact.",
            difficulty="hard",
            source=QuestionSource.BENCHMARK_GAP.value,
            benchmark_gap_refs=["weak ownership proof"],
            why_this_was_asked="Benchmark gap: weak ownership proof",
            response_mode=ResponseMode.SPOKEN_ANSWER.value,
            requires_audio=True,
            requires_video=False,
            requires_text=False,
            requires_code=False,
            provenance={"source": "integration_test_mock"},
        )
        store.persist(question)
        return [question]

    monkeypatch.setattr(prepare_task, "analyze_match", fake_analyze_match)
    monkeypatch.setattr(prepare_task, "analyze_candidate_vs_benchmark", fake_benchmark_analysis)
    monkeypatch.setattr(prepare_task, "generate_interview_questions", fake_generate_questions)


def _patch_answer_pipeline(monkeypatch: pytest.MonkeyPatch, store: SharedStore) -> None:
    monkeypatch.setattr(
        answer_pipeline,
        "_has_successful_agent_result",
        lambda _db, answer_id, agent_type: any(
            row.answer_id == answer_id
            and row.agent_type == agent_type
            and row.status == AgentResultStatus.SUCCEEDED.value
            for row in store.agent_results
        ),
    )
    monkeypatch.setattr(
        answer_pipeline,
        "_has_evaluation",
        lambda _db, answer_id: any(row.answer_id == answer_id for row in store.evaluations),
    )

    def fake_audio_agent(answer: CandidateAnswer) -> dict[str, Any]:
        answer.transcript = (
            "I owned the reliability rollout, reduced API error rate by 30 percent, "
            "and coordinated the PostgreSQL migration with on-call monitoring."
        )
        answer.word_count = len(answer.transcript.split())
        answer.duration_seconds = 42
        answer.words_per_minute = 115
        answer.filler_word_count = 1
        answer.transcription_status = "transcribed"
        answer.communication_metrics = {
            "communication_signal_score": 8,
            "structure_observations": ["context-action-impact structure is present"],
        }
        return {
            "transcript": answer.transcript,
            "word_count": answer.word_count,
            "duration_seconds": answer.duration_seconds,
            "words_per_minute": answer.words_per_minute,
            "filler_word_count": answer.filler_word_count,
            "communication_signal_score": 8,
            "structure_observations": ["context-action-impact structure is present"],
        }

    monkeypatch.setattr(answer_pipeline, "process_candidate_answer_audio", fake_audio_agent)
