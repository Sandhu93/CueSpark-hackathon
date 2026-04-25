from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.core import storage
from app.schemas.common import UploadInitRequest, UploadInitResponse

router = APIRouter()


@router.post("/init", response_model=UploadInitResponse)
async def init_upload(payload: UploadInitRequest) -> UploadInitResponse:
    """
    Get a presigned PUT URL. The frontend uploads directly to MinIO,
    skipping the API for the file body. Best for large files.
    """
    ext = Path(payload.filename).suffix.lstrip(".")
    key = storage.new_object_key(prefix="uploads", ext=ext)
    return UploadInitResponse(
        object_key=key,
        upload_url=storage.presigned_put_url(key),
        public_url=storage.presigned_get_url(key),
    )


@router.post("/direct")
async def direct_upload(file: UploadFile = File(...)) -> dict:
    """
    Convenience endpoint that streams through the API. Use for small files
    or when CORS-direct uploads to MinIO are inconvenient.
    """
    ext = Path(file.filename or "").suffix.lstrip(".")
    key = storage.new_object_key(prefix="uploads", ext=ext)
    body = await file.read()
    storage.put_object(key, body, content_type=file.content_type or "application/octet-stream")
    return {
        "object_key": key,
        "public_url": storage.presigned_get_url(key),
        "size": len(body),
    }
