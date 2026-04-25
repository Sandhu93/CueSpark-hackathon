from __future__ import annotations

from typing import Any

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.question import ResponseMode
from app.schemas.agent_results import VideoSignalResult
from app.services.video_signal_agent import analyze_video_signals
from app.tasks.analyze_video_signals import store_video_signal_agent_result


class FakeDB:
    def __init__(self) -> None:
        self.added: list[Any] = []

    def add(self, item: Any) -> None:
        self.added.append(item)


def _answer(metadata: dict[str, Any] | None = None) -> CandidateAnswer:
    return CandidateAnswer(
        id="answer-1",
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.SPOKEN_ANSWER.value,
        visual_signal_metadata=metadata or {},
    )


def test_video_signal_agent_scores_frontend_metadata():
    result = analyze_video_signals(
        answer=_answer(),
        metadata={
            "face_in_frame_ratio": 0.92,
            "lighting_quality": "good",
            "eye_contact_proxy": "moderate",
            "posture_stability": "steady",
            "camera_presence": "stable",
            "distraction_markers": [],
        },
    )

    assert result.face_in_frame_score == 9
    assert result.lighting_score == 8
    assert result.eye_contact_proxy_score == 6
    assert result.posture_stability_score == 8
    assert result.camera_presence_score == 8
    assert result.visual_signal_score == 8
    assert result.observations
    assert result.risks == []


def test_video_signal_agent_flags_safe_visual_presence_risks():
    result = analyze_video_signals(
        answer=_answer(),
        metadata={
            "face_in_frame_ratio": 0.41,
            "lighting_quality": "poor",
            "eye_contact_proxy": "low",
            "posture_stability": "unstable",
            "camera_presence": "intermittent",
            "distraction_markers": ["frequent off-screen movement"],
        },
    )

    assert result.visual_signal_score < 6
    assert any("Face-in-frame" in risk for risk in result.risks)
    assert any("distraction marker" in risk for risk in result.risks)
    joined = " ".join(result.observations + result.risks).lower()
    assert "emotion" not in joined
    assert "personality" not in joined
    assert "confidence" not in joined
    assert "truthfulness" not in joined


def test_video_signal_agent_mock_mode_uses_safe_defaults(monkeypatch):
    monkeypatch.setattr("app.services.video_signal_agent.settings.ai_mock_mode", True)
    monkeypatch.setattr("app.services.video_signal_agent.settings.openai_api_key", "")

    result = analyze_video_signals(answer=_answer())

    assert result.visual_signal_score >= 6
    assert any("Observable visual presence signals only" in item for item in result.observations)


def test_video_signal_agent_requires_metadata_outside_mock_mode(monkeypatch):
    monkeypatch.setattr("app.services.video_signal_agent.settings.ai_mock_mode", False)
    monkeypatch.setattr("app.services.video_signal_agent.settings.openai_api_key", "sk-test")

    try:
        analyze_video_signals(answer=_answer())
    except ValueError as exc:
        assert "video signal metadata" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_store_video_signal_agent_result_persists_agent_result_row():
    db = FakeDB()
    result = VideoSignalResult(
        face_in_frame_score=9,
        lighting_score=8,
        eye_contact_proxy_score=6,
        posture_stability_score=7,
        camera_presence_score=9,
        visual_signal_score=8,
        observations=["Observable visual presence signals only."],
        risks=[],
    )

    row = store_video_signal_agent_result(db, answer_id="answer-1", result=result)

    assert row in db.added
    assert isinstance(row, AgentResult)
    assert row.answer_id == "answer-1"
    assert row.agent_type == AgentType.VIDEO_SIGNAL.value
    assert row.status == AgentResultStatus.SUCCEEDED.value
    assert row.score == 8.0
    assert row.payload["visual_signal_score"] == 8


def test_video_signal_job_kind_registered():
    from app.api.jobs import TASK_REGISTRY

    assert TASK_REGISTRY["analyze_video_signals"] == "app.tasks.analyze_video_signals.run"
