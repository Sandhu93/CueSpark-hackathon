# Task: Add Text Chunking Service

## Goal

Create a deterministic text chunking service for job descriptions, resumes, benchmark profiles, rubrics, questions, and candidate answers.

## Scope

Implement only:

- A reusable chunking service.
- Sensible defaults for chunk size and overlap.
- Metadata support for chunk type and source.
- Support for known/future chunk types from `docs/10-data-model-contract.md`, including `jd`, `resume`, `benchmark_profile`, `answer`, `rubric`, and `question_bank`.
- Unit tests for chunking behavior where practical.

## Out of Scope

Do not implement:

- Embedding API calls.
- Vector database writes.
- Match analysis.
- Benchmark retrieval.
- Benchmark comparison.
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
- [ ] Chunking supports benchmark profile text as an input type without special-case logic.
- [ ] Chunking does not lose text unexpectedly.
- [ ] Tests or simple verification cover normal and short text.
- [ ] No OpenAI call is added in this task.
- [ ] No benchmark retrieval or comparison is added in this task.

## Verification

Run:

```bash
pytest backend/tests
```

## Notes for Codex

- Prefer simple deterministic chunking over complex dependencies.
- Do not add LangChain unless explicitly required by a later task.
- This service will be reused by the benchmark engine later.
