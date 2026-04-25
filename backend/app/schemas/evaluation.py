from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    answer_id: str
    relevance_score: int | None
    role_depth_score: int | None
    evidence_score: int | None
    clarity_score: int | None
    jd_alignment_score: int | None
    benchmark_gap_coverage_score: int | None
    communication_score: int | None
    overall_score: int | None
    strengths: str | None
    weaknesses: str | None
    strict_feedback: str | None
    improved_answer: str | None
    created_at: datetime
