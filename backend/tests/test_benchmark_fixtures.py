"""Validate benchmark fixture JSON files without touching the database."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "benchmarks"
EXPECTED_ROLES = {"project_manager", "backend_developer", "data_analyst"}
REQUIRED_FIELDS = {
    "role_key", "role_title", "seniority_level", "domain", "profile_name",
    "resume_text", "skills", "tools", "project_signals", "impact_signals",
    "ownership_signals", "source_type", "is_curated", "quality_score",
}
EXPECTED_SENIORITY = {"junior", "mid", "senior", "lead", "principal"}


def _load(role_key: str) -> list[dict]:
    path = FIXTURES_DIR / f"{role_key}.json"
    assert path.exists(), f"Fixture file missing: {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list), f"{path.name}: top-level must be a JSON array"
    return data


# ── presence ──────────────────────────────────────────────────────────────────

def test_all_expected_fixture_files_exist():
    for role_key in EXPECTED_ROLES:
        assert (FIXTURES_DIR / f"{role_key}.json").exists()


@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_each_role_has_five_profiles(role_key):
    profiles = _load(role_key)
    assert len(profiles) == 5, f"{role_key}: expected 5 profiles, got {len(profiles)}"


# ── required fields ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_all_required_fields_present(role_key):
    for i, profile in enumerate(_load(role_key)):
        missing = REQUIRED_FIELDS - profile.keys()
        assert not missing, f"{role_key}[{i}] missing fields: {missing}"


# ── field types and values ────────────────────────────────────────────────────

@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_list_fields_are_lists(role_key):
    list_fields = ("skills", "tools", "project_signals", "impact_signals", "ownership_signals")
    for i, profile in enumerate(_load(role_key)):
        for field in list_fields:
            assert isinstance(profile[field], list), (
                f"{role_key}[{i}].{field} must be a list"
            )


@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_list_fields_are_non_empty(role_key):
    list_fields = ("skills", "tools", "project_signals", "impact_signals", "ownership_signals")
    for i, profile in enumerate(_load(role_key)):
        for field in list_fields:
            assert len(profile[field]) > 0, f"{role_key}[{i}].{field} must not be empty"


@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_role_key_matches_filename(role_key):
    for i, profile in enumerate(_load(role_key)):
        assert profile["role_key"] == role_key, (
            f"{role_key}[{i}].role_key mismatch: {profile['role_key']!r}"
        )


@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_seniority_levels_are_valid(role_key):
    for i, profile in enumerate(_load(role_key)):
        assert profile["seniority_level"] in EXPECTED_SENIORITY, (
            f"{role_key}[{i}].seniority_level invalid: {profile['seniority_level']!r}"
        )


@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_source_type_is_curated(role_key):
    for i, profile in enumerate(_load(role_key)):
        assert profile["source_type"] == "curated", (
            f"{role_key}[{i}].source_type must be 'curated'"
        )
        assert profile["is_curated"] is True, (
            f"{role_key}[{i}].is_curated must be true"
        )


@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_quality_score_in_range(role_key):
    for i, profile in enumerate(_load(role_key)):
        score = profile["quality_score"]
        assert isinstance(score, (int, float)), f"{role_key}[{i}].quality_score must be numeric"
        assert 0 <= score <= 100, f"{role_key}[{i}].quality_score out of range: {score}"


@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_profile_names_are_unique_within_role(role_key):
    profiles = _load(role_key)
    names = [p["profile_name"] for p in profiles]
    assert len(names) == len(set(names)), f"{role_key}: duplicate profile_name values"


@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_resume_text_is_non_empty(role_key):
    for i, profile in enumerate(_load(role_key)):
        text = profile.get("resume_text") or ""
        assert len(text.strip()) > 50, (
            f"{role_key}[{i}].resume_text too short or empty"
        )


# ── coverage across seniority levels ─────────────────────────────────────────

@pytest.mark.parametrize("role_key", sorted(EXPECTED_ROLES))
def test_role_covers_at_least_two_seniority_levels(role_key):
    levels = {p["seniority_level"] for p in _load(role_key)}
    assert len(levels) >= 2, (
        f"{role_key}: only one seniority level represented — add variety"
    )
