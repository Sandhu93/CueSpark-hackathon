# Task: Add Benchmark Seeding Service

## Goal

Load curated benchmark profile fixtures into Postgres so they can be embedded and retrieved.

## Scope

Implement only:

- Fixture loader service for `fixtures/benchmarks/`.
- Idempotent seeding function or command.
- Insert/update benchmark profiles by stable role/profile identity.
- Safe logs showing counts only, not full resume text.

## Out of Scope

Do not implement:

- Live scraping.
- Embedding generation.
- Candidate comparison logic.
- Frontend UI.
- Admin dashboard.

## Files Likely Involved

- `backend/app/services/benchmark_seed.py`
- `backend/app/models/`
- `backend/app/tasks/`
- `fixtures/benchmarks/`
- `README.md` if a command is added

## API Contract

No public endpoint is required in this task.

## Data Model Changes

Use existing `benchmark_profiles` table.

## Acceptance Criteria

- [ ] Fixture files can be loaded into `benchmark_profiles`.
- [ ] Seeding is idempotent.
- [ ] Seeding does not duplicate profiles on repeated runs.
- [ ] Logs show profile counts per role.
- [ ] No raw full benchmark resume text is logged.
- [ ] No embeddings are generated in this task.

## Verification

Run the seeding command or task, then verify profile counts in Postgres.

Example:

```bash
docker compose exec api python -m app.services.benchmark_seed
```

If the final command differs, document the actual command.

## Notes for Codex

- Prefer a simple local command/module over an admin endpoint.
- Do not expose benchmark seeding through public API.
