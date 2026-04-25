from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.session import SessionCreate, SessionCreateResponse, SessionRead
from app.services.sessions import create_session, get_session

router = APIRouter()


@router.post("", response_model=SessionCreateResponse, status_code=201)
async def create_interview_session(
    payload: SessionCreate, db: AsyncSession = Depends(get_db)
) -> SessionCreateResponse:
    session = await create_session(db, payload)
    return SessionCreateResponse(session_id=session.id, status=session.status)


@router.get("/{session_id}", response_model=SessionRead)
async def read_interview_session(
    session_id: str, db: AsyncSession = Depends(get_db)
) -> SessionRead:
    session = await get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
