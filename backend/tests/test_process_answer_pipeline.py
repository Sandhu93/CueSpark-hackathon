from __future__ import annotations

from typing import Any

import pytest

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.question import InterviewQuestion, QuestionCategory, ResponseMode
from app.tasks import process_answer_pipeline as pipeline


class FakeDB:
    def __init__(self, answer: CandidateAnswer, question: InterviewQuestion) -> None:
        self.answer = answer
        self.question = question
        self.added: list[Any] = []

    def get(self, model: type, item_id: str) -> Any | None:
        if model is CandidateAnswer and item_id == self.answer.id:
            return self.answer
        if model is InterviewQuestion and item_id == self.question.id:
            return self.question
        return None

    def add(self, item: Any) -> None:
        self.added.append(item)


def _question(
    *,
    mode: ResponseMode,
    requires_audio: bool = False,
    requires_text: bool = False,
    requires_code: bool = False,
    requires_video: bool = False,
) -> InterviewQuestion:
    return InterviewQuestion(
        id="question-1",
        session_id="session-1",
        question_number=1,
        category=QuestionCategory.BENCHMARK_GAP_VALIDATION.value,
        question_text="Prove the benchmark gap.",
        expected_signal="Evidence with metrics and ownership.",
        benchmark_gap_refs=["weak ownership proof"],
        response_mode=mode.value,
        requires_audio=requires_audio,
        requires_text=requires_text,
        requires_code=requires_code,
        requires_video=requires_video,
    )


def _answer(mode: ResponseMode, **kwargs: Any) -> CandidateAnswer:
    return CandidateAnswer(
        id="answer-1",
        session_id="session-1",
        question_id="question-1",
        answer_mode=mode.value,
        **kwargs,
    )


def _patch_common_pipeline(monkeypatch: pytest.MonkeyPatch, calls: list[str]) -> None:
    monkeypatch.setattr(pipeline, "_has_successful_agent_result", lambda *args: False)
    monkeypatch.setattr(pipeline, "_has_evaluation", lambda *args: False)
    monkeypatch.setattr(
        pipeline,
        "store_text_answer_agent_result",
        lambda *args, **kwargs: calls.append(AgentType.TEXT_ANSWER.value),
    )
    monkeypatch.setattr(pipeline, "analyze_text_answer", lambda *args, **kwargs: object())
    monkeypatch.setattr(
        pipeline,
        "store_code_evaluation_agent_result",
        lambda *args, **kwargs: calls.append(AgentType.CODE_EVALUATION.value),
    )
    monkeypatch.setattr(pipeline, "analyze_code_answer", lambda *args, **kwargs: object())
    monkeypatch.setattr(
        pipeline,
        "store_benchmark_gap_agent_result",
        lambda *args, **kwargs: calls.append(AgentType.BENCHMARK_GAP.value),
    )
    monkeypatch.setattr(
        pipeline,
        "analyze_benchmark_gap_coverage",
        lambda *args, **kwargs: object(),
    )
    monkeypatch.setattr(
        pipeline,
        "_run_audio_agent",
        lambda *args, **kwargs: calls.append(AgentType.AUDIO.value),
    )
    monkeypatch.setattr(
        pipeline,
        "_run_video_agent",
        lambda *args, **kwargs: calls.append(AgentType.VIDEO_SIGNAL.value),
    )

    def fake_evaluate(db, answer_id: str):
        calls.append("final_evaluation")
        db.answer.processing_status = "evaluated"

    monkeypatch.setattr(pipeline, "evaluate_answer", fake_evaluate)


def test_written_answer_pipeline_runs_text_benchmark_and_final(
    monkeypatch: pytest.MonkeyPatch,
):
    calls: list[str] = []
    _patch_common_pipeline(monkeypatch, calls)
    answer = _answer(ResponseMode.WRITTEN_ANSWER, text_answer="Evidence with ownership.")
    question = _question(mode=ResponseMode.WRITTEN_ANSWER, requires_text=True)
    db = FakeDB(answer, question)

    result = pipeline.process_answer_pipeline(db, answer.id)

    assert calls == [
        AgentType.TEXT_ANSWER.value,
        AgentType.BENCHMARK_GAP.value,
        "final_evaluation",
    ]
    assert result["processing_status"] == "evaluated"


def test_mixed_answer_pipeline_runs_available_modalities(
    monkeypatch: pytest.MonkeyPatch,
):
    calls: list[str] = []
    _patch_common_pipeline(monkeypatch, calls)
    answer = _answer(
        ResponseMode.MIXED_ANSWER,
        audio_object_key="answers/audio/a.webm",
        text_answer="Evidence with ownership.",
        code_answer="SELECT 1",
        code_language="sql",
        visual_signal_metadata={"face_in_frame_ratio": 0.9},
    )
    question = _question(mode=ResponseMode.MIXED_ANSWER)
    db = FakeDB(answer, question)

    pipeline.process_answer_pipeline(db, answer.id)

    assert calls == [
        AgentType.AUDIO.value,
        AgentType.TEXT_ANSWER.value,
        AgentType.CODE_EVALUATION.value,
        AgentType.VIDEO_SIGNAL.value,
        AgentType.BENCHMARK_GAP.value,
        "final_evaluation",
    ]


def test_pipeline_skips_existing_successful_agent_result(
    monkeypatch: pytest.MonkeyPatch,
):
    calls: list[str] = []
    _patch_common_pipeline(monkeypatch, calls)
    monkeypatch.setattr(
        pipeline,
        "_has_successful_agent_result",
        lambda _db, _answer_id, agent_type: agent_type == AgentType.TEXT_ANSWER.value,
    )
    answer = _answer(ResponseMode.WRITTEN_ANSWER, text_answer="Evidence with ownership.")
    question = _question(mode=ResponseMode.WRITTEN_ANSWER, requires_text=True)
    db = FakeDB(answer, question)

    result = pipeline.process_answer_pipeline(db, answer.id)

    assert AgentType.TEXT_ANSWER.value not in calls
    assert AgentType.TEXT_ANSWER.value in result["steps_skipped"]
    assert AgentType.BENCHMARK_GAP.value in calls
    assert "final_evaluation" in calls


def test_pipeline_stores_failed_agent_result_and_marks_answer_failed(
    monkeypatch: pytest.MonkeyPatch,
):
    calls: list[str] = []
    _patch_common_pipeline(monkeypatch, calls)
    monkeypatch.setattr(
        pipeline,
        "analyze_text_answer",
        lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("text failed")),
    )
    answer = _answer(ResponseMode.WRITTEN_ANSWER, text_answer="Evidence with ownership.")
    question = _question(mode=ResponseMode.WRITTEN_ANSWER, requires_text=True)
    db = FakeDB(answer, question)

    with pytest.raises(ValueError, match="text failed"):
        pipeline.process_answer_pipeline(db, answer.id)

    failed_rows = [
        row
        for row in db.added
        if isinstance(row, AgentResult) and row.status == AgentResultStatus.FAILED.value
    ]
    assert answer.processing_status == "failed"
    assert failed_rows
    assert failed_rows[0].agent_type == AgentType.TEXT_ANSWER.value


def test_process_answer_pipeline_job_kind_registered():
    from app.api.jobs import TASK_REGISTRY

    assert TASK_REGISTRY["process_answer_pipeline"] == "app.tasks.process_answer_pipeline.run"
