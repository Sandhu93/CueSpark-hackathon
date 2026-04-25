"""
Workers run sync code (RQ uses fork/spawn, not asyncio).
This module gives tasks a simple sync session backed by psycopg.
"""
from __future__ import annotations

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

_sync_url = (
    f"postgresql+psycopg://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

# Lazy — workers may import tasks before psycopg is needed.
_engine = None
_SessionFactory = None


def _ensure():
    global _engine, _SessionFactory
    if _engine is None:
        _engine = create_engine(_sync_url, future=True, pool_pre_ping=True)
        _SessionFactory = sessionmaker(_engine, class_=Session, expire_on_commit=False)


@contextmanager
def session_scope():
    _ensure()
    session = _SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
