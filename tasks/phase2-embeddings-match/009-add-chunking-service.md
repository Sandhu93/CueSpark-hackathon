# Task: Add Text Chunking Service

## Goal

Create a deterministic text chunking service for job descriptions, resumes, rubrics, questions, and candidate answers.

## Scope

Implement only:

- A reusable chunking service.
- Sensible defaults for chunk size and overlap.
- Metadata support for chunk type and source.
- Unit tests for chunking behavior where practical.

## Out of Scope

Do not implement:

- Embedding API calls.
- Vector database writes.
- Match analysis.
- Question generation.
- Frontend changes.

## Files Likely Involved

- `backend/app/services/chunking.py`
- `backend/tests/`

## API Contract

No new public endpoint is required in this task.

## Data Model Changes

None.

## Acceptance Criteria

- [ ] Chunking service accepts raw text and returns ordered chunks.
- [ ] Empty input returns an empty list or validation error consistently.
- [ ] Chunk metadata includes chunk index and chunk type when provided.
- [ ] Chunking does not lose text unexpectedly.
- [ ] Tests or simple verification cover normal and short text.
- [ ] No OpenAI call is added in this task.

## Verification

Run:

```bash
pytest backend/tests
```

## Notes for Codex

- Prefer simple deterministic chunking over complex dependencies.
- Do not add LangChain unless explicitly required by a later task.
