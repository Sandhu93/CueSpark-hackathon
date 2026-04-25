from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.agent_result import AgentResultStatus, AgentType


class AgentResultCreate(BaseModel):
    answer_id: str
    agent_type: AgentType
    status: AgentResultStatus = AgentResultStatus.PENDING
    score: float | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class AgentResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    answer_id: str
    agent_type: AgentType
    status: AgentResultStatus
    score: float | None
    payload: dict[str, Any]
    error: str | None
    created_at: datetime
    updated_at: datetime


class BenchmarkGapCoverageResult(BaseModel):
    benchmark_gap_coverage_score: int
    covered_gaps: list[str]
    missed_gaps: list[str]
    evidence_quality: str
    gap_specific_feedback: str
    remaining_interview_risk: str


class TextAnswerAnalysisResult(BaseModel):
    relevance_score: int
    structure_score: int
    specificity_score: int
    evidence_score: int
    clarity_score: int
    completeness_score: int
    strengths: list[str]
    weaknesses: list[str]
    improvement_suggestions: list[str]


class CodeEvaluationResult(BaseModel):
    correctness_score: int
    edge_case_score: int
    complexity_score: int
    readability_score: int
    testability_score: int
    explanation_score: int
    strengths: list[str]
    weaknesses: list[str]
    suggested_improvements: list[str]
    complexity_analysis: str


class VideoSignalResult(BaseModel):
    face_in_frame_score: int
    lighting_score: int
    eye_contact_proxy_score: int
    posture_stability_score: int
    camera_presence_score: int
    visual_signal_score: int
    observations: list[str]
    risks: list[str]
