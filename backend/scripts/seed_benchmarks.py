"""Seed benchmark profile fixtures into the database.

Usage (from repo root inside Docker):
    docker compose exec api python scripts/seed_benchmarks.py

Or dry-run (validate only, no DB writes):
    docker compose exec api python scripts/seed_benchmarks.py --dry-run
"""
from __future__ import annotations

import argparse
import asyncio
import json
import uuid
from pathlib import Path

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.benchmark_profile import BenchmarkProfile

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "benchmarks"

REQUIRED_FIELDS = {
    "role_key", "role_title", "seniority_level", "profile_name",
    "skills", "tools", "project_signals", "impact_signals",
    "ownership_signals", "source_type", "is_curated",
}


def _validate(profile: dict, source_file: str, index: int) -> None:
    missing = REQUIRED_FIELDS - profile.keys()
    if missing:
        raise ValueError(f"{source_file}[{index}]: missing fields {missing}")
    if not isinstance(profile["skills"], list):
        raise ValueError(f"{source_file}[{index}]: 'skills' must be a list")


def load_fixtures() -> list[dict]:
    profiles: list[dict] = []
    for path in sorted(FIXTURES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"{path.name}: top-level must be a JSON array")
        for i, p in enumerate(data):
            _validate(p, path.name, i)
        profiles.extend(data)
        logger.info("Loaded {} profiles from {}", len(data), path.name)
    return profiles


async def seed(profiles: list[dict], dry_run: bool) -> None:
    engine = create_async_engine(settings.database_url, echo=False)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with factory() as session:
        inserted = skipped = 0
        for p in profiles:
            result = await session.execute(
                select(BenchmarkProfile).where(
                    BenchmarkProfile.role_key == p["role_key"],
                    BenchmarkProfile.profile_name == p["profile_name"],
                )
            )
            existing = result.scalar_one_or_none()
            if existing:
                skipped += 1
                continue

            row = BenchmarkProfile(
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
            session.add(row)
            inserted += 1

        if dry_run:
            logger.info("Dry-run: would insert {} rows, skip {} duplicates", inserted, skipped)
        else:
            await session.commit()
            logger.info("Seeded {} benchmark profiles ({} skipped as duplicates)", inserted, skipped)

    await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed benchmark profile fixtures")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, no DB writes")
    args = parser.parse_args()

    profiles = load_fixtures()
    logger.info("Total profiles loaded: {}", len(profiles))

    if args.dry_run:
        logger.info("Dry-run mode — skipping DB writes")
        return

    asyncio.run(seed(profiles, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
