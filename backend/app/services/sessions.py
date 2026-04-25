from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import InterviewSession, InterviewSessionStatus
from app.schemas.session import SessionCreate
from app.services.documents import create_pasted_resume_document


async def create_session(db: AsyncSession, payload: SessionCreate) -> InterviewSession:
    session = InterviewSession(
        job_description_text=payload.job_description,
        resume_text=payload.resume_text,
        role_title=payload.role_title,
        company_name=payload.company_name,
        status=InterviewSessionStatus.DRAFT.value,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    if payload.resume_text:
        await create_pasted_resume_document(db, session_id=session.id, resume_text=payload.resume_text)
        await db.commit()
    return session


async def get_session(db: AsyncSession, session_id: str) -> InterviewSession | None:
    return await db.get(InterviewSession, session_id)
