# Task 020 — OpenAI Gateway and Embeddings

## Goal

Create centralized OpenAI access and implement embedding generation/storage for JD/resume chunks.

## Read First

- `docs/01-architecture.md`
- `docs/04-ai-audio-rag-design.md`
- `docs/07-codex-development-rules.md`

## Requirements

1. Add `backend/app/services/openai_gateway.py`.
2. Add `backend/app/services/embeddings.py`.
3. Implement embedding generation using configured embedding model.
4. Store embedding chunks in `embedding_chunks`.
5. Update `prepare_session` to embed JD and resume chunks.
6. Do not call OpenAI from routes or frontend.
7. Add graceful error handling if `OPENAI_API_KEY` is missing.

## Behavior

When `prepare_session` runs:

```text
parse documents
  -> chunk text
  -> call embedding service
  -> store embedding_chunks
```

## Acceptance Criteria

- Embeddings are stored for JD chunks.
- Embeddings are stored for resume chunks when resume text exists.
- Missing API key produces a controlled failure or stub behavior suitable for local development.
- Existing session preparation status is updated correctly.

## Out of Scope

- Match scoring.
- Question generation.
- TTS.
- Transcription.
