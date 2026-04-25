# Task: Add Interviewer Context Model

## Goal

Add the database model and schemas required to store optional interviewer context for a session.

This task creates storage only. It must not parse PDFs, call AI, or change question generation.

## Scope

Implement only:

- `interviewer_contexts` model.
- Pydantic schemas for create/read use cases.
- Relationship to `interview_sessions`.
- Model imports required for database initialization.
- Status fields for extraction and analysis.

## Out of Scope

Do not implement:

- LinkedIn scraping.
- PDF parsing.
- AI analysis.
- Question generation changes.
- Frontend UI.
- File upload endpoint.

## Files Likely Involved

- `backend/app/models/interviewer_context.py`
- `backend/app/schemas/interviewer_context.py`
- `backend/app/models/__init__.py`
- `backend/app/core/db.py`

## Data Model Changes

Create `interviewer_contexts`.

Recommended fields:

- `id`
- `session_id`
- `input_type`: `upload | paste`
- `source_type`: `linkedin_pdf | public_bio | recruiter_note | manual`
- `object_key`
- `filename`
- `content_type`
- `raw_text`
- `extracted_text`
- `parse_status`: `pending | parsed | failed | ocr_required`
- `analysis_status`: `pending | analyzed | failed`
- `interviewer_name`
- `interviewer_title`
- `company`
- `top_skills`
- `likely_focus_areas`
- `likely_interview_style`
- `question_bias`
- `metadata`
- `created_at`
- `updated_at`

## Acceptance Criteria

- [ ] `interviewer_contexts` model exists.
- [ ] Model links to `interview_sessions`.
- [ ] Model supports upload and paste input.
- [ ] Model supports LinkedIn-exported PDF as `source_type=linkedin_pdf`.
- [ ] Pydantic schemas exist.
- [ ] App starts and imports model successfully.
- [ ] No scraping, PDF parsing, AI analysis, or frontend UI is added.

## Verification

Run:

```bash
docker compose up --build
```

If tests exist:

```bash
pytest backend/tests
```

## Notes for Codex

- Do not store assumptions as facts.
- Use safe wording: `interviewer context`, not `interviewer profiling`.
- This is optional personalization; the app must still work without interviewer context.
