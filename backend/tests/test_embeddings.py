from __future__ import annotations

import sys
from typing import Any
from unittest.mock import patch

import pytest

from app.models.embedding_chunk import EMBEDDING_DIMENSIONS, EmbeddingChunk
from app.services.embeddings import embed_and_store


class FakeDB:
    """Minimal sync-session stand-in that records add() calls."""

    def __init__(self) -> None:
        self.added: list[Any] = []

    def add(self, obj: Any) -> None:
        self.added.append(obj)


# ── basic storage behaviour ──────────────────────────────────────────────────

def test_jd_chunks_are_stored(monkeypatch: pytest.MonkeyPatch):
    db = FakeDB()
    text = " ".join([f"word{i}" for i in range(200)])

    rows = embed_and_store(text=text, chunk_type="jd", session_id="s1", db=db)

    assert len(rows) > 0
    assert all(isinstance(r, EmbeddingChunk) for r in rows)
    assert all(r.chunk_type == "jd" for r in rows)
    assert all(r.session_id == "s1" for r in rows)
    assert db.added == rows


def test_resume_chunks_are_stored():
    db = FakeDB()
    text = " ".join([f"skill{i}" for i in range(200)])

    rows = embed_and_store(text=text, chunk_type="resume", session_id="s2", db=db)

    assert len(rows) > 0
    assert all(r.chunk_type == "resume" for r in rows)
    assert all(r.session_id == "s2" for r in rows)


def test_benchmark_profile_chunk_type_is_accepted():
    """benchmark_profile must not be hard-rejected; owner_type/owner_id are used instead."""
    db = FakeDB()
    text = "Experienced project manager with proven delivery record and measurable team outcomes."

    rows = embed_and_store(
        text=text,
        chunk_type="benchmark_profile",
        session_id=None,
        owner_type="benchmark_profile",
        owner_id="bp-123",
        db=db,
    )

    assert len(rows) == 1
    assert rows[0].chunk_type == "benchmark_profile"
    assert rows[0].session_id is None
    assert rows[0].owner_type == "benchmark_profile"
    assert rows[0].owner_id == "bp-123"


def test_empty_text_returns_no_rows():
    db = FakeDB()

    rows = embed_and_store(text="   ", chunk_type="jd", session_id="s3", db=db)

    assert rows == []
    assert db.added == []


def test_chunk_indices_are_sequential():
    db = FakeDB()
    text = " ".join([f"t{i}" for i in range(400)])

    rows = embed_and_store(text=text, chunk_type="jd", session_id="s4", db=db, chunk_size=100)

    for expected_idx, row in enumerate(rows):
        assert row.chunk_index == expected_idx


# ── embedding dimensions ─────────────────────────────────────────────────────

def test_mock_vectors_match_db_column_dimension():
    db = FakeDB()
    text = "Backend developer with Python and FastAPI experience."

    rows = embed_and_store(text=text, chunk_type="jd", session_id="s5", db=db)

    assert len(rows) == 1
    assert len(rows[0].embedding) == EMBEDDING_DIMENSIONS


def test_all_chunks_have_correct_embedding_dimension():
    db = FakeDB()
    text = " ".join([f"word{i}" for i in range(300)])

    rows = embed_and_store(text=text, chunk_type="resume", session_id="s6", db=db, chunk_size=100)

    assert all(len(r.embedding) == EMBEDDING_DIMENSIONS for r in rows)


# ── mock mode isolation ───────────────────────────────────────────────────────

def test_mock_mode_does_not_call_openai():
    """With AI_MOCK_MODE=true (the default), the service must work without an API key.

    We verify this by ensuring no real network call occurs: mock_embedding is
    used instead, so the result always has the correct dimension regardless of
    whether OPENAI_API_KEY is set.
    """
    db = FakeDB()
    text = "Some resume text for the candidate."

    # Patch out the real openai module entirely so any accidental import raises
    with patch.dict("sys.modules", {"openai": None}):
        rows = embed_and_store(text=text, chunk_type="resume", session_id="s7", db=db)

    assert len(rows) == 1
    assert len(rows[0].embedding) == EMBEDDING_DIMENSIONS


def test_owner_type_and_owner_id_stored_on_row():
    db = FakeDB()

    rows = embed_and_store(
        text="Sample rubric content.",
        chunk_type="rubric",
        session_id="s8",
        owner_type="session",
        owner_id="s8",
        db=db,
    )

    assert rows[0].owner_type == "session"
    assert rows[0].owner_id == "s8"
