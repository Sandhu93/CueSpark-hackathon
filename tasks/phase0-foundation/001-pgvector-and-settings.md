# Task 001 — pgvector and AI Settings Foundation

## Goal

Prepare local Docker Postgres for pgvector and centralize AI-related settings.

## Read First

- `docs/01-architecture.md`
- `docs/02-backend-design.md`
- `docs/03-database-design.md`
- `docs/04-ai-audio-rag-design.md`

## Requirements

1. Change the Docker Postgres image to a pgvector-enabled image.
2. Ensure the `vector` extension is created during database initialization.
3. Add AI model settings to `backend/app/core/config.py`.
4. Add matching values to `.env.example`.
5. Do not implement OpenAI calls yet.

## Suggested Settings

```text
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TTS_VOICE=marin
OPENAI_TRANSCRIBE_MODEL=gpt-4o-transcribe
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## Files Likely Changed

- `docker-compose.yml`
- `.env.example`
- `backend/app/core/config.py`
- `backend/app/core/db.py`

## Acceptance Criteria

- Postgres starts successfully.
- `CREATE EXTENSION IF NOT EXISTS vector;` is executed during initialization.
- Settings are available via `settings.openai_tts_model`, etc.
- Existing tests still pass.

## Out of Scope

- Creating all product tables.
- Calling OpenAI.
- Embedding generation.
