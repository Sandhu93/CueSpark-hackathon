"""Read-only benchmark comparison endpoint.

Returns stored BenchmarkComparison data for a prepared session.
Does not generate benchmark analysis or call any external service.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.benchmark_comparison import BenchmarkComparison
from app.models.benchmark_profile import BenchmarkProfile
from app.models.session import InterviewSession
from app.schemas.benchmark import (
    BenchmarkComparisonResponse,
    BenchmarkPendingResponse,
    BenchmarkProfileSummary,
)

router = APIRouter()


@router.get("/{session_id}/benchmark")
async def get_session_benchmark(
    session_id: str,
    db: AsyncSession = Depends(get_db),
) -> BenchmarkComparisonResponse | BenchmarkPendingResponse:
    session = await db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    result = await db.execute(
        select(BenchmarkComparison).where(BenchmarkComparison.session_id == session_id)
    )
    comparison = result.scalars().first()
    if comparison is None:
        return BenchmarkPendingResponse(session_id=session_id)

    profiles: list[BenchmarkProfileSummary] = []
    if comparison.benchmark_profile_ids:
        prof_result = await db.execute(
            select(BenchmarkProfile).where(
                BenchmarkProfile.id.in_(comparison.benchmark_profile_ids)
            )
        )
        profiles = [
            BenchmarkProfileSummary.model_validate(p)
            for p in prof_result.scalars().all()
        ]

    return BenchmarkComparisonResponse(
        session_id=session_id,
        role_key=comparison.role_key,
        benchmark_similarity_score=comparison.benchmark_similarity_score,
        resume_competitiveness_score=comparison.resume_competitiveness_score,
        evidence_strength_score=comparison.evidence_strength_score,
        benchmark_profiles=profiles,
        missing_skills=comparison.missing_skills or [],
        weak_skills=comparison.weak_skills or [],
        missing_metrics=comparison.missing_metrics or [],
        weak_ownership_signals=comparison.weak_ownership_signals or [],
        interview_risk_areas=comparison.interview_risk_areas or [],
        recommended_resume_fixes=comparison.recommended_resume_fixes or [],
        question_targets=comparison.question_targets or [],
    )
