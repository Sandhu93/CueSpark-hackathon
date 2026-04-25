from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.benchmark_profile import BenchmarkSourceType


class BenchmarkProfileSummary(BaseModel):
    """Lightweight benchmark profile info returned inside comparison responses."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    profile_name: str
    role_title: str
    seniority_level: str
    quality_score: float | None


class BenchmarkComparisonResponse(BaseModel):
    """Full response for GET /api/sessions/{session_id}/benchmark when data is ready."""

    session_id: str
    role_key: str
    benchmark_similarity_score: int | None
    resume_competitiveness_score: int | None
    evidence_strength_score: int | None
    benchmark_profiles: list[BenchmarkProfileSummary]
    missing_skills: list[str]
    weak_skills: list[str]
    missing_metrics: list[str]
    weak_ownership_signals: list[str]
    interview_risk_areas: list[str]
    recommended_resume_fixes: list[str]
    question_targets: list[str]


class BenchmarkPendingResponse(BaseModel):
    """Response when the session exists but benchmark analysis has not run yet."""

    session_id: str
    status: str = "pending"


class BenchmarkAnalysisResult(BaseModel):
    """Structured output of a candidate-vs-benchmark comparison."""

    benchmark_similarity_score: int = Field(ge=0, le=100)
    resume_competitiveness_score: int = Field(ge=0, le=100)
    evidence_strength_score: int = Field(ge=0, le=100)
    missing_skills: list[str]
    weak_skills: list[str]
    missing_metrics: list[str]
    weak_ownership_signals: list[str]
    interview_risk_areas: list[str]
    recommended_resume_fixes: list[str]
    question_targets: list[str]


class BenchmarkProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    role_key: str
    role_title: str
    seniority_level: str
    domain: str | None
    profile_name: str
    skills: list
    tools: list
    project_signals: list
    impact_signals: list
    ownership_signals: list
    source_type: str
    source_url: str | None
    is_curated: bool
    quality_score: float | None
    created_at: datetime


class BenchmarkComparisonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    role_key: str
    benchmark_profile_ids: list
    benchmark_similarity_score: int | None
    resume_competitiveness_score: int | None
    evidence_strength_score: int | None
    missing_skills: list
    weak_skills: list
    missing_metrics: list
    weak_ownership_signals: list
    interview_risk_areas: list
    recommended_resume_fixes: list
    question_targets: list
    created_at: datetime
