"""Tests for app.services.benchmark_retrieval."""
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from app.models.benchmark_profile import BenchmarkProfile
from app.models.embedding_chunk import EMBEDDING_DIMENSIONS, ChunkType, EmbeddingChunk
from app.services.benchmark_retrieval import (
    embed_benchmark_profile,
    retrieve_benchmark_profiles,
)


# ── shared fixtures ───────────────────────────────────────────────────────────

class FakeDB:
    """Minimal sync-session stand-in that records add() calls."""

    def __init__(self) -> None:
        self.added: list[Any] = []

    def add(self, obj: Any) -> None:
        self.added.append(obj)


def _profile(
    profile_id: str = "bp-1",
    role_key: str = "project_manager",
    quality_score: float = 80.0,
    resume_text: str = "Experienced project manager with 5 years leading software delivery.",
) -> BenchmarkProfile:
    return BenchmarkProfile(
        id=profile_id,
        role_key=role_key,
        role_title="Project Manager",
        seniority_level="mid",
        profile_name=f"Profile {profile_id}",
        resume_text=resume_text,
        skills=["planning", "stakeholder management"],
        tools=["Jira"],
        project_signals=[],
        impact_signals=[],
        ownership_signals=[],
        source_type="curated",
        is_curated=True,
        quality_score=quality_score,
    )


def _mock_db(profiles: list[BenchmarkProfile]) -> MagicMock:
    """Return a sync-session MagicMock whose execute chain returns profiles."""
    db = MagicMock()
    db.execute.return_value.scalars.return_value.all.return_value = profiles
    return db


# ── embed_benchmark_profile ───────────────────────────────────────────────────

def test_embed_returns_chunks_for_non_empty_resume():
    db = FakeDB()
    profile = _profile()

    rows = embed_benchmark_profile(profile, db)

    assert len(rows) > 0
    assert db.added == rows


def test_embed_returns_empty_for_blank_resume():
    db = FakeDB()
    profile = _profile(resume_text="   ")

    rows = embed_benchmark_profile(profile, db)

    assert rows == []
    assert db.added == []


def test_embed_chunk_type_is_benchmark_profile():
    db = FakeDB()
    rows = embed_benchmark_profile(_profile(), db)

    assert all(r.chunk_type == ChunkType.BENCHMARK_PROFILE.value for r in rows)


def test_embed_session_id_is_none():
    db = FakeDB()
    rows = embed_benchmark_profile(_profile(), db)

    assert all(r.session_id is None for r in rows)


def test_embed_owner_fields_match_profile():
    db = FakeDB()
    profile = _profile(profile_id="bp-42")

    rows = embed_benchmark_profile(profile, db)

    assert all(r.owner_type == "benchmark_profile" for r in rows)
    assert all(r.owner_id == "bp-42" for r in rows)


def test_embed_vectors_have_correct_dimension():
    db = FakeDB()
    rows = embed_benchmark_profile(_profile(), db)

    assert all(len(r.embedding) == EMBEDDING_DIMENSIONS for r in rows)


def test_embed_chunk_indices_are_sequential():
    db = FakeDB()
    # long text forces multiple chunks
    long_text = " ".join([f"word{i}" for i in range(400)])
    profile = _profile(resume_text=long_text)

    rows = embed_benchmark_profile(profile, db, chunk_size=100)

    for expected, row in enumerate(rows):
        assert row.chunk_index == expected


def test_embed_custom_chunk_size_respected():
    db_small = FakeDB()
    db_large = FakeDB()
    text = " ".join([f"word{i}" for i in range(300)])
    profile = _profile(resume_text=text)

    # overlap must be < chunk_size; use 10 so both chunk sizes are valid
    rows_small = embed_benchmark_profile(profile, db_small, chunk_size=60, overlap=10)
    rows_large = embed_benchmark_profile(profile, db_large, chunk_size=500, overlap=10)

    assert len(rows_small) > len(rows_large)


# ── retrieve_benchmark_profiles (mock mode) ───────────────────────────────────

def test_retrieve_returns_empty_when_no_candidates():
    db = _mock_db([])
    result = retrieve_benchmark_profiles("unknown_role", "some JD", db)
    assert result == []


def test_retrieve_mock_mode_returns_by_quality_score_descending():
    low = _profile("p1", quality_score=60.0)
    high = _profile("p2", quality_score=95.0)
    mid = _profile("p3", quality_score=75.0)
    db = _mock_db([low, high, mid])

    result = retrieve_benchmark_profiles("project_manager", "some JD text", db)

    assert result[0].quality_score == 95.0
    assert result[1].quality_score == 75.0
    assert result[2].quality_score == 60.0


def test_retrieve_mock_mode_respects_top_k():
    profiles = [_profile(f"p{i}", quality_score=float(i * 10)) for i in range(1, 8)]
    db = _mock_db(profiles)

    result = retrieve_benchmark_profiles("project_manager", "JD", db, top_k=3)

    assert len(result) == 3


def test_retrieve_mock_mode_top_k_larger_than_candidates():
    profiles = [_profile("p1"), _profile("p2")]
    db = _mock_db(profiles)

    result = retrieve_benchmark_profiles("project_manager", "JD", db, top_k=10)

    assert len(result) == 2


def test_retrieve_mock_mode_does_not_call_llm_embed():
    db = _mock_db([_profile()])

    with patch("app.services.benchmark_retrieval.llm.embed") as mock_embed:
        retrieve_benchmark_profiles("project_manager", "JD text", db)

    mock_embed.assert_not_called()


def test_retrieve_handles_none_quality_score():
    profile = _profile()
    profile.quality_score = None
    db = _mock_db([profile])

    result = retrieve_benchmark_profiles("project_manager", "JD", db)

    assert len(result) == 1  # must not raise


def test_retrieve_blank_query_text_uses_quality_fallback():
    low = _profile("p1", quality_score=50.0)
    high = _profile("p2", quality_score=90.0)
    db = _mock_db([low, high])

    result = retrieve_benchmark_profiles("project_manager", "   ", db)

    assert result[0].quality_score == 90.0


def test_retrieve_no_role_key_returns_all_candidates_ranked():
    profiles = [
        _profile("p1", role_key="project_manager", quality_score=70.0),
        _profile("p2", role_key="backend_developer", quality_score=85.0),
    ]
    db = _mock_db(profiles)

    result = retrieve_benchmark_profiles(None, "JD", db)

    assert len(result) == 2
    assert result[0].quality_score == 85.0


# ── real mode fallback (no chunks → quality_score) ────────────────────────────

def test_retrieve_real_mode_falls_back_to_quality_when_no_chunks():
    """When ai_mock_mode=False but no chunks exist, fall back to quality ranking."""
    low = _profile("p1", quality_score=55.0)
    high = _profile("p2", quality_score=88.0)

    db = MagicMock()
    # First execute call → profile list; second → empty chunk rows
    db.execute.side_effect = [
        MagicMock(**{"scalars.return_value.all.return_value": [low, high]}),
        MagicMock(**{"all.return_value": []}),  # no chunk rows
    ]

    with patch("app.services.benchmark_retrieval.settings") as mock_settings:
        mock_settings.ai_mock_mode = False
        with patch("app.services.benchmark_retrieval.llm.embed", return_value=[[0.1] * 1536]):
            result = retrieve_benchmark_profiles("project_manager", "JD text", db, top_k=5)

    assert result[0].quality_score == 88.0
    assert result[1].quality_score == 55.0
