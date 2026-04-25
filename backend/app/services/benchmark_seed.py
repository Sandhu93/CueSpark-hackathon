"""Benchmark profile seeding service.

Loads curated fixture JSON files and upserts them into the benchmark_profiles
table.  Idempotent: profiles that already exist (matched by role_key +
profile_name) are skipped.  Resume text is never written to logs.

Run directly:
    docker compose exec api python -m app.services.benchmark_seed
    docker compose exec api python -m app.services.benchmark_seed --dry-run
"""
from __future__ import annotations

import argparse
import asyncio
import json
import uuid
from pathlib import Path

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.benchmark_profile import BenchmarkProfile

FIXTURES_DIR = Path(__file__).parent.parent.parent / "fixtures" / "benchmarks"

REQUIRED_FIELDS: frozenset[str] = frozenset(
    {
        "role_key",
        "role_title",
        "seniority_level",
        "profile_name",
        "skills",
        "tools",
        "project_signals",
        "impact_signals",
        "ownership_signals",
        "source_type",
        "is_curated",
    }
)


# ── pure helpers ──────────────────────────────────────────────────────────────

def validate_profile(profile: dict, source_file: str = "<unknown>", index: int = 0) -> None:
    """Raise ValueError if a required field is absent or has the wrong type."""
    missing = REQUIRED_FIELDS - profile.keys()
    if missing:
        raise ValueError(f"{source_file}[{index}]: missing fields {missing}")
    if not isinstance(profile["skills"], list):
        raise ValueError(f"{source_file}[{index}]: 'skills' must be a list")
    if not isinstance(profile["tools"], list):
        raise ValueError(f"{source_file}[{index}]: 'tools' must be a list")


def load_fixtures(fixtures_dir: Path = FIXTURES_DIR) -> list[dict]:
    """Read every *.json file in fixtures_dir, validate each profile, return flat list.

    Logs per-file profile counts.  Never logs resume_text content.
    """
    if not fixtures_dir.exists():
        raise FileNotFoundError(f"Fixtures directory not found: {fixtures_dir}")

    profiles: list[dict] = []
    for path in sorted(fixtures_dir.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError(f"{path.name}: top-level must be a JSON array")
        for i, p in enumerate(raw):
            validate_profile(p, path.name, i)
        profiles.extend(raw)
        logger.info(
            "benchmark_seed: loaded {} profile(s) from {}",
            len(raw),
            path.name,
        )
    return profiles


def build_profile_row(p: dict) -> BenchmarkProfile:
    """Construct a BenchmarkProfile ORM object from a fixture dict."""
    return BenchmarkProfile(
        id=str(uuid.uuid4()),
        role_key=p["role_key"],
        role_title=p["role_title"],
        seniority_level=p["seniority_level"],
        domain=p.get("domain"),
        profile_name=p["profile_name"],
        resume_text=p.get("resume_text"),
        skills=p.get("skills", []),
        tools=p.get("tools", []),
        project_signals=p.get("project_signals", []),
        impact_signals=p.get("impact_signals", []),
        ownership_signals=p.get("ownership_signals", []),
        source_type=p.get("source_type", "curated"),
        source_url=p.get("source_url"),
        is_curated=p.get("is_curated", True),
        quality_score=p.get("quality_score"),
    )


# ── DB-dependent logic ────────────────────────────────────────────────────────

async def seed_profiles(
    session: AsyncSession,
    profiles: list[dict],
    *,
    dry_run: bool = False,
) -> dict[str, tuple[int, int]]:
    """Upsert profiles grouped by role_key.

    Returns {role_key: (inserted, skipped)}.
    Commits on success; rolls back in dry-run mode.
    Logs counts per role — never logs resume text.
    """
    by_role: dict[str, list[dict]] = {}
    for p in profiles:
        by_role.setdefault(p["role_key"], []).append(p)

    counts: dict[str, tuple[int, int]] = {}

    for role_key, role_profiles in sorted(by_role.items()):
        inserted = skipped = 0
        for p in role_profiles:
            result = await session.execute(
                select(BenchmarkProfile).where(
                    BenchmarkProfile.role_key == p["role_key"],
                    BenchmarkProfile.profile_name == p["profile_name"],
                )
            )
            if result.scalar_one_or_none() is not None:
                skipped += 1
            else:
                session.add(build_profile_row(p))
                inserted += 1

        logger.info(
            "benchmark_seed: role={} inserted={} skipped={}",
            role_key,
            inserted,
            skipped,
        )
        counts[role_key] = (inserted, skipped)

    if dry_run:
        await session.rollback()
        logger.info("benchmark_seed: dry-run — changes rolled back")
    else:
        await session.commit()

    return counts


async def run(
    *,
    dry_run: bool = False,
    fixtures_dir: Path = FIXTURES_DIR,
) -> dict[str, tuple[int, int]]:
    """Load fixtures and seed the database.  Returns per-role (inserted, skipped) counts."""
    from app.core.db import SessionLocal  # local import — avoids circular at module level

    profiles = load_fixtures(fixtures_dir)
    logger.info("benchmark_seed: {} total profile(s) to process", len(profiles))

    async with SessionLocal() as session:
        counts = await seed_profiles(session, profiles, dry_run=dry_run)

    total_inserted = sum(v[0] for v in counts.values())
    total_skipped = sum(v[1] for v in counts.values())
    logger.info(
        "benchmark_seed: complete — total_inserted={} total_skipped={}",
        total_inserted,
        total_skipped,
    )
    return counts


# ── CLI entrypoint ────────────────────────────────────────────────────────────

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Seed benchmark profile fixtures into Postgres"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and count without writing to the database",
    )
    args = parser.parse_args()
    asyncio.run(run(dry_run=args.dry_run))


if __name__ == "__main__":
    _cli()
