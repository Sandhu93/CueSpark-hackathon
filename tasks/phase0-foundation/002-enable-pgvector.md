# Task: Enable pgvector in Local Postgres

## Goal

Prepare the local Postgres database to store vector embeddings using pgvector.

## Scope

Implement only:

- Update the Postgres Docker image to a pgvector-compatible image if needed.
- Add database initialization for `CREATE EXTENSION IF NOT EXISTS vector;`.
- Ensure the API and worker can still connect to Postgres.
- Document any required database reset command if the local volume must be recreated.

## Out of Scope

Do not implement:

- Embedding generation.
- `embedding_chunks` model.
- AI/OpenAI calls.
- Interview features.

## Files Likely Involved

- `docker-compose.yml`
- `infra/`
- `.env.example`
- `backend/app/core/db.py`
- `README.md`

## API Contract

No new API endpoint is required in this task.

## Data Model Changes

Only the `vector` extension should be enabled.

## Acceptance Criteria

- [ ] Local Postgres supports the `vector` extension.
- [ ] `CREATE EXTENSION IF NOT EXISTS vector;` is applied during initialization or startup.
- [ ] Existing API DB connectivity still works.
- [ ] Existing worker DB connectivity still works.
- [ ] No embedding table is created in this task.
- [ ] No AI features are implemented in this task.

## Verification

Run:

```bash
docker compose up --build
```

Then verify inside Postgres:

```bash
docker compose exec postgres psql -U postgres -d cuespark_interview -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

## Notes for Codex

- If a clean database volume is required, document the command but do not delete data automatically.
- Keep this task focused on infrastructure readiness only.
