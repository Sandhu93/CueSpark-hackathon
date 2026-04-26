from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.report import HiringRecommendation


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    readiness_score: int | None
    hiring_recommendation: HiringRecommendation | None
    summary: str | None
    jd_resume_match_summary: str | None
    benchmark_similarity_score: int | None
    resume_competitiveness_score: int | None
    evidence_strength_score: int | None
    skill_gaps: list[Any]
    benchmark_gaps: list[Any]
    interview_risk_areas: list[Any]
    answer_feedback: list[Any]
    benchmark_gap_coverage_summary: str | None
    audio_communication_summary: str | None
    communication_summary: str | None
    visual_signal_summary: str | None
    written_answer_quality_summary: str | None
    written_answer_summary: str | None
    code_answer_quality_summary: str | None
    code_answer_summary: str | None
    multimodal_summary: dict[str, Any]
    resume_feedback: str | None
    improvement_plan: str | None
    created_at: datetime
    updated_at: datetime

    @field_validator(
        "skill_gaps",
        "benchmark_gaps",
        "interview_risk_areas",
        "answer_feedback",
        mode="before",
    )
    @classmethod
    def _default_json_list(cls, value: object) -> object:
        return [] if value is None else value

    @field_validator("multimodal_summary", mode="before")
    @classmethod
    def _default_multimodal_summary(cls, value: object) -> object:
        return {} if value is None else value
