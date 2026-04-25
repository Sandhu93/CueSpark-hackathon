# Task: Add Benchmark Embedding and Retrieval

## Goal

Embed curated benchmark profiles and retrieve the most relevant benchmark profiles for a session role/JD.

## Scope

Implement only:

- Chunk benchmark profile resume text.
- Store benchmark chunks in `embedding_chunks`.
- Add retrieval service for relevant benchmark profiles.
- Match by inferred role key first, then vector similarity.
- Return top 5 benchmark profiles for a session.

## Out of Scope

Do not implement:

- Live web scraping.
- Candidate-vs-benchmark gap analysis.
- Question generation.
- Frontend UI.
- Final report changes.

## Files Likely Involved

- `backend/app/services/benchmark_retrieval.py`
- `backend/app/services/chunking.py`
- `backend/app/services/embeddings.py`
- `backend/app/models/`
- `backend/app/tasks/`
- `backend/tests/`

## API Contract

No public endpoint is required unless needed for local debugging.

## Data Model Changes

Use existing:

- `benchmark_profiles`
- `embedding_chunks`

Use:

```txt
chunk_type = benchmark_profile
owner_type = benchmark_profile
owner_id = benchmark_profiles.id
```

## Acceptance Criteria

- [ ] Benchmark profile text can be chunked.
- [ ] Benchmark chunks can be embedded and stored.
- [ ] Mock mode works without OpenAI API key.
- [ ] Retrieval returns top 5 profiles for a role/JD.
- [ ] Retrieval prefers matching role keys when available.
- [ ] No candidate comparison is implemented in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can inspect retrieved profiles for `project_manager`, `backend_developer`, and `data_analyst`.

## Notes for Codex

- Keep retrieval simple for hackathon.
- Do not add external crawler dependencies.
