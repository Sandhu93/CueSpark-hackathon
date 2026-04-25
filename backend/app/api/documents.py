from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.document import DocumentUploadResponse
from app.services.documents import create_uploaded_resume_document, is_supported_resume_file
from app.services.sessions import get_session

router = APIRouter()


@router.post("/sessions/{session_id}/resume", response_model=DocumentUploadResponse)
async def upload_resume(
    session_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> DocumentUploadResponse:
    session = await get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if not is_supported_resume_file(file.filename or "", file.content_type):
        raise HTTPException(status_code=400, detail="Unsupported resume file type")

    document = await create_uploaded_resume_document(db, session_id=session_id, file=file)
    return DocumentUploadResponse(document_id=document.id, parse_status=document.parse_status)
