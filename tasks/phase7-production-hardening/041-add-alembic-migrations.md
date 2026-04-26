# Task: Add Alembic Migrations

## Goal

Introduce a real database migration system before production so schema changes are versioned, repeatable, and safe across machines/environments.

The current `Base.metadata.create_all()` plus compatibility `ALTER TABLE IF NOT EXISTS` patches are acceptable for local development, but they are not enough for a production product.

## Why This Task Exists

`create_all()` can create missing tables, but it does not reliably manage schema evolution.

It does not safely handle:

- column renames
- type changes
- dropping obsolete columns
- index changes over time
- constraint changes
- migration ordering
- cross-machine schema drift
- production rollback planning

Alembic gives the project versioned schema history.

## Scope

Implement only:

- Add Alembic dependency/configuration.
- Add `alembic.ini`.
- Add `backend/alembic/` migration environment.
- Configure Alembic to use the existing SQLAlchemy metadata.
- Create an initial baseline migration that reflects the current models.
- Add documentation for running migrations locally.
- Add Makefile/npm/docker command if the project has conventions for this.
- Keep local `create_all()` behavior only if needed for developer convenience, but production path should use migrations.

## Out of Scope

Do not implement:

- New product tables beyond current model definitions.
- New API endpoints.
- New frontend pages.
- Agent orchestration.
- Data backfill beyond initial schema migration unless required.
- Production deployment automation.

## Files Likely Involved

- `backend/pyproject.toml`
- `backend/alembic.ini` or root `alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/versions/0001_initial_schema.py`
- `backend/app/core/db.py`
- `docker-compose.yml` only if needed
- `Makefile` only if migration commands are centralized there
- `docs/03-database-design.md` only if command documentation needs updating

## Migration Requirements

Initial migration should include current product tables, as applicable:

```txt
interview_sessions
documents
benchmark_profiles
benchmark_comparisons
interview_questions
candidate_answers
agent_results
answer_evaluations
interview_reports
embedding_chunks
jobs if the app has a jobs table
```

It should also create:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

and pgvector fields where applicable.

## Important Compatibility Rule

Do not blindly remove the local compatibility layer if the app currently depends on it for developer boot.

Preferred approach:

- Keep local boot stable.
- Add Alembic as the formal migration path.
- Document that fresh developer databases should run migrations.
- Later remove compatibility patches when the project is stable.

## Acceptance Criteria

- [ ] Alembic is installed/configured.
- [ ] Alembic can connect to the app database settings.
- [ ] Initial migration creates the current schema.
- [ ] pgvector extension is handled.
- [ ] `alembic upgrade head` works on a fresh database.
- [ ] Existing local Docker boot is not broken.
- [ ] Migration commands are documented.
- [ ] No product behavior is changed.

## Verification

Run against a fresh local database:

```bash
cd backend
alembic upgrade head
```

Then run:

```bash
pytest backend/tests
```

If using Docker:

```bash
docker compose down -v
docker compose up --build
# run migration command inside backend/api container depending on project setup
```

## Notes for Codex

- This is production hardening, not an immediate product-feature task.
- Do not mix migrations with new feature implementation.
- Do not invent schema fields outside the current model/docs unless necessary to match existing code.
- If the codebase still uses `Base.metadata.create_all()`, document how it coexists with Alembic.
