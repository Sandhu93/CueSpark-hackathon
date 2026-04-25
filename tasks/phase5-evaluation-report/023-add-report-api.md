# Task: Add Report API

## Goal

Expose endpoints to generate and retrieve the final benchmark-aware interview report.

## Scope

Implement only:

- `POST /api/sessions/{session_id}/report`.
- `GET /api/sessions/{session_id}/report`.
- Enqueue report generation job.
- Return stored report when available.
- Include benchmark-aware report fields in the response.

## Out of Scope

Do not implement:

- Frontend report page.
- PDF export.
- Email delivery.
- Recruiter workflows.
- Login or accounts.
- Benchmark comparison generation.

## Files Likely Involved

- `backend/app/api/reports.py`
- `backend/app/api/jobs.py`
- `backend/app/tasks/generate_report.py`
- `backend/app/schemas/`
- `backend/app/models/`
- Router registration file

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

## Data Model Changes

None.

## Acceptance Criteria

- [ ] `POST /api/sessions/{session_id}/report` enqueues report generation.
- [ ] Unknown session returns 404.
- [ ] `GET /api/sessions/{session_id}/report` returns report when available.
- [ ] Report response includes benchmark similarity, resume competitiveness, evidence strength, benchmark gaps, and interview risk areas when available.
- [ ] Missing report returns a clear pending/not-found response.
- [ ] No report is generated inside the GET endpoint.
- [ ] No benchmark comparison is generated inside either report endpoint.
- [ ] No frontend changes are made in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual:

```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/report
curl http://localhost:8000/api/sessions/{session_id}/report
```

## Notes for Codex

- Use the existing job system for long-running work.
- Keep endpoints thin.
- The GET endpoint is read-only.
