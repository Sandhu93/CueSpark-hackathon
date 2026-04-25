from __future__ import annotations

from app.models.answer import CandidateAnswer
from app.schemas.answer import AudioAgentResult
from app.services.audio_agent import process_audio_answer
from app.services.communication_analysis import analyze_communication_signals
from app.tasks import process_audio_answer as task


def test_audio_agent_mock_mode_returns_safe_structured_output(monkeypatch):
    monkeypatch.setattr("app.services.transcription.settings.ai_mock_mode", True)
    monkeypatch.setattr("app.services.transcription.settings.openai_api_key", "")

    result = process_audio_answer(b"fake-audio", duration_seconds=30)

    assert result.transcript
    assert result.word_count > 0
    assert result.duration_seconds == 30
    assert result.words_per_minute is not None
    assert isinstance(result.filler_words, list)
    assert isinstance(result.hesitation_markers, list)
    assert isinstance(result.structure_observations, list)
    assert 1 <= result.communication_signal_score <= 10


def test_communication_analysis_counts_safe_observable_signals():
    result = analyze_communication_signals(
        "Um I owned the API and then improved latency impact, like, after tracing.",
        duration_seconds=20,
    )

    assert result.word_count == 13
    assert result.filler_word_count == 2
    assert result.filler_words == ["like", "um"]
    assert "Uses sequence markers" in result.structure_observations
    assert "Mentions impact" in result.structure_observations
    assert "Mentions ownership" in result.structure_observations


def test_process_candidate_answer_audio_stores_transcript_and_metrics(monkeypatch):
    answer = CandidateAnswer(
        id="answer-1",
        session_id="session-1",
        question_id="question-1",
        audio_object_key="answers/audio/answer.webm",
        duration_seconds=12,
    )

    monkeypatch.setattr(task.storage, "get_object", lambda key: b"audio-bytes")
    monkeypatch.setattr(
        task,
        "process_audio_answer",
        lambda *args, **kwargs: AudioAgentResult(
            transcript="I owned the API and improved latency.",
            word_count=7,
            duration_seconds=12,
            words_per_minute=35.0,
            filler_word_count=0,
            filler_words=[],
            hesitation_markers=[],
            structure_observations=["Mentions ownership", "Mentions impact"],
            communication_signal_score=8,
        ),
    )

    result = task.process_candidate_answer_audio(answer)

    assert result["transcript"] == "I owned the API and improved latency."
    assert answer.transcript == "I owned the API and improved latency."
    assert answer.word_count == 7
    assert answer.words_per_minute == 35.0
    assert answer.filler_word_count == 0
    assert answer.communication_metrics["communication_signal_score"] == 8
    assert "speaking pace" in answer.communication_metrics["safe_signal_labels"]


def test_process_candidate_answer_audio_requires_audio_object_key():
    answer = CandidateAnswer(
        id="answer-1",
        session_id="session-1",
        question_id="question-1",
    )

    try:
        task.process_candidate_answer_audio(answer)
    except ValueError as exc:
        assert "audio object key" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_audio_processing_job_kind_registered():
    from app.api.jobs import TASK_REGISTRY

    assert TASK_REGISTRY["process_audio_answer"] == "app.tasks.process_audio_answer.run"
