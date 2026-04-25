"""Tests for app.services.benchmark_seed."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.benchmark_profile import BenchmarkProfile
from app.services.benchmark_seed import (
    FIXTURES_DIR,
    build_profile_row,
    load_fixtures,
    run,
    seed_profiles,
    validate_profile,
)

# ── fixture helpers ───────────────────────────────────────────────────────────

def _valid_profile(**overrides) -> dict:
    base = {
        "role_key": "backend_developer",
        "role_title": "Backend Developer",
        "seniority_level": "mid",
        "domain": "web_services",
        "profile_name": "Test Profile",
        "resume_text": "Five years of Python and FastAPI experience.",
        "skills": ["Python", "FastAPI"],
        "tools": ["Docker", "PostgreSQL"],
        "project_signals": ["built booking API"],
        "impact_signals": ["latency reduced 50%"],
        "ownership_signals": ["sole owner of service"],
        "source_type": "curated",
        "source_url": None,
        "is_curated": True,
        "quality_score": 85.0,
    }
    base.update(overrides)
    return base


# ── validate_profile ──────────────────────────────────────────────────────────

def test_validate_profile_accepts_valid_profile():
    validate_profile(_valid_profile())  # must not raise


def test_validate_profile_raises_on_missing_required_field():
    p = _valid_profile()
    del p["role_key"]
    with pytest.raises(ValueError, match="missing fields"):
        validate_profile(p, "test.json", 0)


def test_validate_profile_raises_on_non_list_skills():
    p = _valid_profile(skills="Python, FastAPI")
    with pytest.raises(ValueError, match="'skills' must be a list"):
        validate_profile(p, "test.json", 0)


def test_validate_profile_raises_on_non_list_tools():
    p = _valid_profile(tools="Docker")
    with pytest.raises(ValueError, match="'tools' must be a list"):
        validate_profile(p, "test.json", 0)


def test_validate_profile_error_message_includes_filename_and_index():
    p = _valid_profile()
    del p["profile_name"]
    with pytest.raises(ValueError, match="fixtures.json\\[2\\]"):
        validate_profile(p, "fixtures.json", 2)


# ── load_fixtures ─────────────────────────────────────────────────────────────

def test_load_fixtures_returns_15_profiles():
    profiles = load_fixtures(FIXTURES_DIR)
    assert len(profiles) == 15  # 3 roles × 5 profiles


def test_load_fixtures_all_three_roles_present():
    profiles = load_fixtures(FIXTURES_DIR)
    role_keys = {p["role_key"] for p in profiles}
    assert role_keys >= {"project_manager", "backend_developer", "data_analyst"}


def test_load_fixtures_each_role_has_five_profiles():
    profiles = load_fixtures(FIXTURES_DIR)
    from collections import Counter
    counts = Counter(p["role_key"] for p in profiles)
    for role_key, count in counts.items():
        assert count == 5, f"{role_key}: expected 5, got {count}"


def test_load_fixtures_raises_on_missing_dir(tmp_path):
    missing = tmp_path / "nonexistent"
    with pytest.raises(FileNotFoundError, match="Fixtures directory not found"):
        load_fixtures(missing)


def test_load_fixtures_raises_on_non_array_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"key": "value"}', encoding="utf-8")
    with pytest.raises(ValueError, match="top-level must be a JSON array"):
        load_fixtures(tmp_path)


def test_load_fixtures_raises_on_invalid_profile_in_file(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('[{"role_key": "x"}]', encoding="utf-8")  # missing required fields
    with pytest.raises(ValueError, match="missing fields"):
        load_fixtures(tmp_path)


# ── build_profile_row ─────────────────────────────────────────────────────────

def test_build_profile_row_returns_benchmark_profile_instance():
    row = build_profile_row(_valid_profile())
    assert isinstance(row, BenchmarkProfile)


def test_build_profile_row_maps_required_fields():
    p = _valid_profile()
    row = build_profile_row(p)
    assert row.role_key == p["role_key"]
    assert row.role_title == p["role_title"]
    assert row.seniority_level == p["seniority_level"]
    assert row.profile_name == p["profile_name"]
    assert row.skills == p["skills"]
    assert row.tools == p["tools"]


def test_build_profile_row_assigns_uuid_id():
    row = build_profile_row(_valid_profile())
    assert row.id is not None
    assert len(row.id) == 36  # UUID string


def test_build_profile_row_optional_fields_default_safely():
    p = _valid_profile()
    del p["domain"]
    del p["source_url"]
    row = build_profile_row(p)
    assert row.domain is None
    assert row.source_url is None


# ── seed_profiles (mock session) ──────────────────────────────────────────────
#
# session.execute() is an AsyncMock (awaitable), but its return value must be
# a plain MagicMock so that result.scalar_one_or_none() is a regular callable
# — not a coroutine — whose return value we can control.

def _mock_session(existing_row=None) -> AsyncMock:
    """Return an AsyncMock session where scalar_one_or_none() returns existing_row.

    session.add is overridden to a plain MagicMock because Session.add() is
    synchronous even in async SQLAlchemy — using AsyncMock would produce
    unawaited-coroutine warnings.
    """
    session = AsyncMock()
    session.add = MagicMock()  # sync in real async sessions
    result = MagicMock()
    result.scalar_one_or_none.return_value = existing_row
    session.execute.return_value = result
    return session


async def test_seed_profiles_inserts_new_profiles():
    session = _mock_session(existing_row=None)

    profiles = [_valid_profile(profile_name="A"), _valid_profile(profile_name="B")]
    counts = await seed_profiles(session, profiles)

    assert counts["backend_developer"] == (2, 0)
    assert session.add.call_count == 2
    session.commit.assert_called_once()


async def test_seed_profiles_skips_existing_profiles():
    session = _mock_session(existing_row=MagicMock())

    profiles = [_valid_profile(profile_name="A"), _valid_profile(profile_name="B")]
    counts = await seed_profiles(session, profiles)

    assert counts["backend_developer"] == (0, 2)
    session.add.assert_not_called()
    session.commit.assert_called_once()


async def test_seed_profiles_dry_run_rolls_back():
    session = _mock_session(existing_row=None)

    await seed_profiles(session, [_valid_profile()], dry_run=True)

    session.rollback.assert_called_once()
    session.commit.assert_not_called()


async def test_seed_profiles_groups_by_role_key():
    session = _mock_session(existing_row=None)

    pm = _valid_profile(role_key="project_manager", role_title="PM", profile_name="X")
    be = _valid_profile(role_key="backend_developer", role_title="BE", profile_name="Y")
    counts = await seed_profiles(session, [pm, be])

    assert "project_manager" in counts
    assert "backend_developer" in counts
    assert counts["project_manager"] == (1, 0)
    assert counts["backend_developer"] == (1, 0)


# ── run() — integration (dry-run, real DB) ────────────────────────────────────

async def test_run_dry_run_returns_per_role_counts():
    counts = await run(dry_run=True)
    assert set(counts.keys()) >= {"project_manager", "backend_developer", "data_analyst"}
    for role_key, (inserted, skipped) in counts.items():
        assert isinstance(inserted, int)
        assert isinstance(skipped, int)
        assert inserted + skipped == 5, f"{role_key}: expected 5 profiles total"
