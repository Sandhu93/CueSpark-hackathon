from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.session import InterviewSessionStatus


class SessionCreate(BaseModel):
    job_description: str = Field(min_length=1)
    resume_text: str | None = None
    role_title: str | None = None
    company_name: str | None = None

    @field_validator("job_description")
    @classmethod
    def validate_job_description(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Job description is required")
        return stripped


class SessionCreateResponse(BaseModel):
    session_id: str
    status: InterviewSessionStatus


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: InterviewSessionStatus
    role_title: str | None
    role_key: str | None
    company_name: str | None
    job_description_text: str
    resume_text: str | None
    match_score: int | None
    benchmark_similarity_score: int | None
    resume_competitiveness_score: int | None
    evidence_strength_score: int | None
    current_question_index: int
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
