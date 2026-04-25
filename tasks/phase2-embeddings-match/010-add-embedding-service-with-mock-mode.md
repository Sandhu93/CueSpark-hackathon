# Task: Add Embedding Service with Mock Mode

## Goal

Add a backend service that can generate embeddings in real mode or deterministic placeholder embeddings in mock mode.

## Scope

Implement only:

- `embeddings.py` service.
- Mock embedding generation when `AI_MOCK_MODE=true`.
- Real OpenAI embedding call only if configuration and client structure already support it.
- Store embeddings in `embedding_chunks` for JD and resume chunks.

## Out of Scope

Do not implement:

- Match analysis.
- Question generation.
- TTS.
- Transcription.
- Frontend changes.

## Files Likely Involved

- `backend/app/services/embeddings.py`
- `backend/app/services/openai_client.py`
- `backend/app/models/`
- `backend/app/tasks/`
- `backend/tests/`

## API Contract

No new public endpoint is required in this task.

## Data Model Changes

Use existing `embedding_chunks` table.

## Acceptance Criteria

- [ ] Embedding service returns deterministic mock vectors when mock mode is enabled.
- [ ] Embedding dimension matches the configured database vector dimension.
- [ ] JD and resume chunks can be stored as `embedding_chunks`.
- [ ] Service does not call OpenAI when `AI_MOCK_MODE=true`.
- [ ] OpenAI model name comes from settings, not hardcoded values.
- [ ] No frontend changes are made.

## Verification

Run:

```bash
pytest backend/tests
```

If running manually, verify mock mode works without `OPENAI_API_KEY`.

## Notes for Codex

- Mock mode is mandatory for local development.
- Do not log raw resume/JD text.
