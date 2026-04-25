from __future__ import annotations

from datetime import datetime

from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.schemas.agent_results import AgentResultCreate, AgentResultRead


def test_agent_type_enum_covers_contract_values():
    expected = {
        "audio",
        "video_signal",
        "text_answer",
        "code_evaluation",
        "benchmark_gap",
        "final_orchestrator",
    }
    assert {item.value for item in AgentType} == expected


def test_agent_result_status_enum_covers_contract_values():
    expected = {"pending", "running", "succeeded", "failed"}
    assert {item.value for item in AgentResultStatus} == expected


def test_agent_result_model_stores_agent_output_payload():
    result = AgentResult(
        answer_id="answer-1",
        agent_type=AgentType.AUDIO.value,
        status=AgentResultStatus.SUCCEEDED.value,
        score=7.0,
        payload={"transcript": "sample", "communication_signal_score": 7},
    )

    assert result.answer_id == "answer-1"
    assert result.agent_type == AgentType.AUDIO.value
    assert result.status == AgentResultStatus.SUCCEEDED.value
    assert result.score == 7.0
    assert result.payload["communication_signal_score"] == 7


def test_agent_result_create_schema_defaults_to_pending_with_empty_payload():
    payload = AgentResultCreate(answer_id="answer-1", agent_type=AgentType.TEXT_ANSWER)

    assert payload.status == AgentResultStatus.PENDING
    assert payload.payload == {}
    assert payload.score is None
    assert payload.error is None


def test_agent_result_read_schema_accepts_model_attributes():
    row = AgentResult(
        id="agent-result-1",
        answer_id="answer-1",
        agent_type=AgentType.BENCHMARK_GAP.value,
        status=AgentResultStatus.FAILED.value,
        score=None,
        payload={"gap": "metrics"},
        error="agent failed",
        created_at=datetime(2026, 1, 1),
        updated_at=datetime(2026, 1, 2),
    )

    read = AgentResultRead.model_validate(row)

    assert read.id == "agent-result-1"
    assert read.answer_id == "answer-1"
    assert read.agent_type == AgentType.BENCHMARK_GAP
    assert read.status == AgentResultStatus.FAILED
    assert read.payload == {"gap": "metrics"}
    assert read.error == "agent failed"
