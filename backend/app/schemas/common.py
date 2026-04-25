from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class UploadInitRequest(BaseModel):
    filename: str
    content_type: str = "application/octet-stream"


class UploadInitResponse(BaseModel):
    object_key: str
    upload_url: str = Field(description="PUT this URL with the file body")
    public_url: str


class JobCreate(BaseModel):
    kind: str
    input: dict[str, Any] = Field(default_factory=dict)


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    kind: str
    status: str
    input: dict[str, Any]
    result: dict[str, Any]
    error: str | None
    created_at: datetime
    updated_at: datetime
