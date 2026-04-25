from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.document import DocumentInputType, DocumentParseStatus, DocumentType


class DocumentCreate(BaseModel):
    session_id: str
    document_type: DocumentType
    input_type: DocumentInputType
    object_key: str | None = None
    filename: str | None = None
    content_type: str | None = None
    extracted_text: str | None = None
    parse_status: DocumentParseStatus = DocumentParseStatus.PENDING
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    session_id: str
    document_type: DocumentType
    input_type: DocumentInputType
    object_key: str | None
    filename: str | None
    content_type: str | None
    extracted_text: str | None
    parse_status: DocumentParseStatus
    metadata: dict[str, Any] = Field(alias="metadata_")
    created_at: datetime
    updated_at: datetime


class DocumentUploadResponse(BaseModel):
    document_id: str
    parse_status: DocumentParseStatus
