from __future__ import annotations

import uuid
from datetime import timedelta

import boto3
from botocore.client import Config
from loguru import logger

from app.core.config import settings


def _client():
    return boto3.client(
        "s3",
        endpoint_url=f"{'https' if settings.minio_use_ssl else 'http'}://{settings.minio_endpoint}",
        aws_access_key_id=settings.minio_root_user,
        aws_secret_access_key=settings.minio_root_password,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


def ensure_bucket() -> None:
    s3 = _client()
    try:
        s3.head_bucket(Bucket=settings.minio_bucket)
    except Exception:
        logger.info("Creating bucket {}", settings.minio_bucket)
        s3.create_bucket(Bucket=settings.minio_bucket)


def put_object(key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
    s3 = _client()
    s3.put_object(Bucket=settings.minio_bucket, Key=key, Body=data, ContentType=content_type)
    return key


def get_object(key: str) -> bytes:
    s3 = _client()
    obj = s3.get_object(Bucket=settings.minio_bucket, Key=key)
    return obj["Body"].read()


def presigned_put_url(key: str, expires_in: int = 3600) -> str:
    s3 = _client()
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.minio_bucket, "Key": key},
        ExpiresIn=expires_in,
    )


def presigned_get_url(key: str, expires_in: int = 3600) -> str:
    """Returns a URL using the public endpoint so browsers can access it."""
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.minio_public_endpoint,
        aws_access_key_id=settings.minio_root_user,
        aws_secret_access_key=settings.minio_root_password,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.minio_bucket, "Key": key},
        ExpiresIn=expires_in,
    )


def new_object_key(prefix: str = "uploads", ext: str = "") -> str:
    suffix = f".{ext.lstrip('.')}" if ext else ""
    return f"{prefix}/{uuid.uuid4().hex}{suffix}"


__all__ = [
    "ensure_bucket",
    "put_object",
    "get_object",
    "presigned_put_url",
    "presigned_get_url",
    "new_object_key",
]
