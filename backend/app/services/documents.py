from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import storage
from app.core.config import settings
from app.models.document import (
    Document,
    DocumentInputType,
    DocumentParseStatus,
    DocumentType,
)
from app.services.document_parser import extract_document_text

ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx", "txt"}
ALLOWED_RESUME_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}


def is_supported_resume_file(filename: str, content_type: str | None) -> bool:
    extension = Path(filename).suffix.lower().lstrip(".")
    return extension in ALLOWED_RESUME_EXTENSIONS and (
        not content_type or content_type in ALLOWED_RESUME_CONTENT_TYPES
    )


async def create_pasted_resume_document(
    db: AsyncSession, *, session_id: str, resume_text: str
) -> Document:
    document = Document(
        session_id=session_id,
        document_type=DocumentType.RESUME.value,
        input_type=DocumentInputType.PASTE.value,
        extracted_text=resume_text,
        parse_status=DocumentParseStatus.PARSED.value,
        metadata_={"character_count": len(resume_text)},
    )
    db.add(document)
    return document


async def create_uploaded_resume_document(
    db: AsyncSession, *, session_id: str, file: UploadFile
) -> Document:
    filename = Path(file.filename or "resume").name
    extension = Path(filename).suffix.lower().lstrip(".")
    object_key = storage.new_object_key(prefix=f"resumes/original/{session_id}", ext=extension)
    body = await file.read()
    if len(body) > settings.max_resume_upload_bytes:
        raise HTTPException(status_code=413, detail="Resume file is too large")
    storage.put_object(
        object_key,
        body,
        content_type=file.content_type or "application/octet-stream",
    )
    parsed = extract_document_text(body, filename, file.content_type)

    document = Document(
        session_id=session_id,
        document_type=DocumentType.RESUME.value,
        input_type=DocumentInputType.UPLOAD.value,
        object_key=object_key,
        filename=filename,
        content_type=file.content_type,
        extracted_text=parsed.extracted_text,
        parse_status=parsed.parse_status.value,
        metadata_={"size": len(body), **parsed.metadata},
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document
