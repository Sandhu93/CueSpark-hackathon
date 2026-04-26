from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core import storage
from app.core.config import settings
from app.schemas.common import UploadInitRequest, UploadInitResponse

router = APIRouter()

ALLOWED_GENERIC_UPLOAD_EXTENSIONS = {"pdf", "docx", "txt", "mp3", "mp4", "m4a", "wav", "webm", "ogg"}
ALLOWED_GENERIC_UPLOAD_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "audio/mpeg",
    "audio/mp3",
    "audio/mp4",
    "audio/wav",
    "audio/wave",
    "audio/x-wav",
    "audio/webm",
    "audio/ogg",
    "audio/x-m4a",
    "video/webm",
}


@router.post("/init", response_model=UploadInitResponse)
async def init_upload(payload: UploadInitRequest) -> UploadInitResponse:
    """
    Get a presigned PUT URL. The frontend uploads directly to MinIO,
    skipping the API for the file body. Best for large files.
    """
    ext = Path(payload.filename).suffix.lstrip(".")
    if not _is_allowed_upload(payload.filename, payload.content_type):
        raise HTTPException(status_code=400, detail="Unsupported upload file type")
    key = storage.new_object_key(prefix="uploads", ext=ext)
    return UploadInitResponse(
        object_key=key,
        upload_url=storage.presigned_put_url(key),
        download_url=storage.presigned_get_url(key),
    )


@router.post("/direct")
async def direct_upload(file: UploadFile = File(...)) -> dict:
    """
    Convenience endpoint that streams through the API. Use for small files
    or when CORS-direct uploads to MinIO are inconvenient.
    """
    ext = Path(file.filename or "").suffix.lstrip(".")
    if not _is_allowed_upload(file.filename or "", file.content_type):
        raise HTTPException(status_code=400, detail="Unsupported upload file type")
    key = storage.new_object_key(prefix="uploads", ext=ext)
    body = await file.read()
    if len(body) > settings.max_generic_upload_bytes:
        raise HTTPException(status_code=413, detail="Uploaded file is too large")
    storage.put_object(key, body, content_type=file.content_type or "application/octet-stream")
    return {
        "object_key": key,
        "download_url": storage.presigned_get_url(key),
        "size": len(body),
    }


def _is_allowed_upload(filename: str, content_type: str | None) -> bool:
    extension = Path(filename).suffix.lower().lstrip(".")
    return (
        extension in ALLOWED_GENERIC_UPLOAD_EXTENSIONS
        and (content_type or "").lower() in ALLOWED_GENERIC_UPLOAD_CONTENT_TYPES
    )
