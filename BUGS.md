# BUGS.md — CueSpark Interview Coach

A learning-focused bug log for tracking issues encountered while building CueSpark Interview Coach.

Use this file to record what broke, why it broke, how it was debugged, how it was fixed, and what you learned. Keep entries practical and specific so they are useful when revisiting the project later.

---

## How to Use This File

For every meaningful issue, add a new numbered entry.

Use this naming format:

```txt
BUG-001 — Short bug title
BUG-002 — Short bug title
BUG-003 — Short bug title
```

Recommended workflow:

1. Add the bug when you first encounter it.
2. Fill in the symptoms and suspected cause immediately.
3. Update the root cause after debugging.
4. Record the exact fix.
5. Add prevention notes after the issue is resolved.

---

## Bug Index

| Bug ID | Status | Area | Short Title | Date Found | Date Resolved |
| --- | --- | --- | --- | --- | --- |
| BUG-001 | Template | Example | Example bug entry | YYYY-MM-DD | YYYY-MM-DD |

Status values:

```txt
Open
Investigating
Resolved
Won't Fix
Regression
Template
```

Area examples:

```txt
backend
frontend
database
worker
docker
minio
redis
openai
audio
transcription
embeddings
ui
deployment
testing
docs
```

---

## BUG-001 — Example bug entry

**Status:** Template  
**Area:** backend / worker / frontend / database / etc.  
**Date Found:** YYYY-MM-DD  
**Date Resolved:** YYYY-MM-DD  
**Related Task:** `tasks/<phase>/<task>.md`  
**Related Commit/PR:** `<commit hash or PR link>`

### What Happened

Describe the visible problem.

Example:

```txt
The session preparation job stayed in queued state and never moved to processing or completed.
```

### Expected Behavior

Describe what should have happened.

Example:

```txt
After calling POST /api/sessions/{session_id}/prepare, the worker should process the job and update the session status to ready.
```

### Actual Behavior

Describe what actually happened.

Example:

```txt
The API returned a job_id, but the frontend kept polling and the status never changed.
```

### Error Message / Logs

Paste only relevant logs. Remove secrets, API keys, private candidate data, resumes, transcripts, or signed URLs.

```txt
Paste sanitized logs here.
```

### Steps to Reproduce

1. Start the stack with `docker compose up --build`.
2. Go to `/setup`.
3. Paste the sample JD and resume.
4. Click `Start Interview`.
5. Observe the job status.

### Suspected Cause

Write your first theory.

Example:

```txt
The RQ worker may not have imported the new task module or the task kind may not be registered in the job registry.
```

### Root Cause

Write the confirmed cause after debugging.

Example:

```txt
The task was created but not registered in backend/app/api/jobs.py, so the worker could not resolve the task handler.
```

### Resolution

Describe the exact fix.

Example:

```txt
Registered the prepare_session task in the task registry and restarted the worker container.
```

### Files Changed

- `backend/app/api/jobs.py`
- `backend/app/tasks/prepare_session.py`

### Verification

Describe how you confirmed the fix.

```bash
docker compose restart worker
docker compose logs -f worker
pytest backend/tests/test_prepare_session.py
```

### Learning Notes

What should future-you remember?

Example:

```txt
Whenever adding a new worker task, register it and restart the worker. API container reload is not enough for worker task discovery.
```

### Prevention

Add a small rule, test, or checklist item to avoid repeating it.

Example:

```txt
Add a test that verifies every allowed job kind maps to an importable task handler.
```

---

## New Bug Entry Template

Copy this section for new bugs.

```md
## BUG-XXX — <short title>

**Status:** Open  
**Area:** <backend/frontend/database/worker/docker/minio/redis/openai/audio/etc.>  
**Date Found:** YYYY-MM-DD  
**Date Resolved:** Not resolved yet  
**Related Task:** `tasks/<phase>/<task>.md`  
**Related Commit/PR:** <optional>

### What Happened


### Expected Behavior


### Actual Behavior


### Error Message / Logs

```txt

```

### Steps to Reproduce

1. 
2. 
3. 

### Suspected Cause


### Root Cause

Not confirmed yet.

### Resolution

Not resolved yet.

### Files Changed

- 

### Verification

```bash

```

### Learning Notes


### Prevention


```

---

## Debugging Checklist

Use this before asking Codex to fix a bug.

- [ ] Which phase/task introduced the issue?
- [ ] Is the bug backend, frontend, database, worker, or infrastructure?
- [ ] Can the bug be reproduced with fixture data?
- [ ] Is there a clear error message?
- [ ] Did the API container and worker container both restart if needed?
- [ ] Are environment variables loaded correctly?
- [ ] Are migrations/init scripts applied?
- [ ] Is the MinIO bucket created?
- [ ] Is Redis running?
- [ ] Is pgvector enabled?
- [ ] Are OpenAI calls mocked or real?
- [ ] Are secrets removed from pasted logs?

---

## Common Bug Categories to Watch

### Docker / Local Stack

- Container starts but service cannot connect to database.
- Worker does not pick up jobs.
- MinIO bucket is missing.
- Environment variables differ between API and worker.

### Database / pgvector

- `vector` extension not enabled.
- Embedding dimension mismatch.
- Model imported by API but not by worker.
- Table exists locally but not after clean rebuild.

### Worker / RQ

- Task not registered.
- Worker using old code after task update.
- Job status not updated after failure.
- Exceptions swallowed without useful logs.

### OpenAI / AI Mock Mode

- API key missing.
- Mock mode not respected.
- Model name hardcoded in service.
- LLM output does not match Pydantic schema.

### Audio

- Browser records unsupported MIME type.
- Uploaded audio cannot be transcribed.
- Audio object stored in MinIO but URL generation fails.
- TTS file created but frontend cannot play it.

### Frontend

- API base URL mismatch.
- Polling continues forever.
- UI assumes fields exist before job completes.
- TypeScript types drift from backend schemas.

---

## Rule

Do not use this file as a dumping ground for every tiny typo. Track bugs that teach something about the system, architecture, debugging process, or development workflow.
