# Task: Add Session Preparation Job

## Goal

Create the background job that prepares a session by parsing available text, chunking, embedding, generating match analysis, running benchmark comparison, and preparing the session for benchmark-driven questions.

## Scope

Implement only:

- `POST /api/sessions/{session_id}/prepare` if not already implemented.
- `prepare_session` worker task.
- Session status transitions: `draft` → `preparing` → `ready` or `failed`.
- Use existing parser/chunking/embedding/match services.
- Use benchmark services if they were already implemented in `tasks/phase2-benchmark-engine/`.
- Store benchmark comparison result before question generation if available.
- Return a `job_id` to the frontend.

## Out of Scope

Do not implement:

- Benchmark model creation.
- Benchmark fixture creation.
- Benchmark seeding command.
- New benchmark service logic not already created in the benchmark phase.
- TTS.
- Candidate recording.
- Report generation.
- Frontend interview UI.

## Files Likely Involved

- `backend/app/api/sessions.py`
- `backend/app/api/jobs.py`
- `backend/app/tasks/prepare_session.py`
- `backend/app/tasks/_db.py`
- `backend/app/services/`
- `backend/app/models/`

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

### POST `/api/sessions/{session_id}/prepare`

Response:

```json
{
  "job_id": "string",
  "status": "queued"
}
```

## Data Model Changes

None unless required by previous missing models.

## Preparation Pipeline

The worker should perform this sequence when all previous services exist:

```txt
parse resume if needed
chunk JD/resume
embed JD/resume
generate JD-resume match analysis
infer/store role_key
retrieve benchmark profiles
run candidate-vs-benchmark analysis
store benchmark comparison
generate or trigger benchmark-driven question generation
mark session ready
```

If question generation is still a separate task in the current implementation stage, this task may stop after benchmark comparison and leave the session in a clear prepared state.

## Acceptance Criteria

- [ ] Endpoint enqueues a preparation job.
- [ ] Worker task updates session status to `preparing`.
- [ ] Worker task chunks and embeds JD/resume text.
- [ ] Worker task generates match analysis.
- [ ] Worker task stores/infer role key where supported.
- [ ] Worker task runs benchmark retrieval/comparison if benchmark services exist.
- [ ] Worker task updates session status to `ready` on success.
- [ ] Worker task updates session status to `failed` on failure.
- [ ] Job status can be checked using the existing job system.
- [ ] No TTS, answer upload, transcription, or report generation is implemented in this task.

## Verification

Run:

```bash
docker compose up --build
```

Then:

```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/prepare
```

Check worker logs:

```bash
docker compose logs -f worker
```

## Notes for Codex

- Use `tasks/_db.py:session_scope` if present.
- Do not duplicate DB session handling patterns.
- Do not silently fall back to generic preparation if benchmark services exist but fail; store/log a clear recoverable failure.
