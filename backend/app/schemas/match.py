from __future__ import annotations

from pydantic import BaseModel, Field


class MatchAnalysisResult(BaseModel):
    role_title: str
    role_key: str  # normalized snake_case, e.g. "backend_developer"
    seniority_level: str  # e.g. "mid", "senior", "lead"
    match_score: int = Field(ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    risk_areas: list[str]
    interview_focus_areas: list[str]
