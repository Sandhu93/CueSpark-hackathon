# Task: Add Resume Upload and Paste Support

## Goal

Allow a session to receive resume content either as pasted text or as an uploaded file stored in MinIO.

This task only prepares resume data for later parsing, embedding, and benchmark comparison.

## Scope

Implement only:

- Resume upload endpoint for PDF/DOCX/TXT files.
- Resume paste support if not already handled by session creation.
- Store uploaded file in MinIO.
- Create/update a `documents` row for the resume.
- Store object key, input type, and parse status.

## Out of Scope

Do not implement:

- Full OCR.
- AI analysis.
- Embeddings.
- Benchmark retrieval.
- Benchmark comparison.
- Question generation.
- Frontend upload UI unless explicitly small and necessary.

## Files Likely Involved

- `backend/app/api/documents.py`
- `backend/app/services/storage.py`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/main.py` or router registration file

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

### POST `/api/sessions/{session_id}/resume`

Accepts multipart file upload.

## Data Model Changes

Use the existing `documents` table.

## Acceptance Criteria

- [ ] Resume file upload stores the file in MinIO.
- [ ] Database stores the MinIO object key.
- [ ] Upload creates a `documents` row with `document_type=resume`.
- [ ] Upload creates a `documents` row with `input_type=upload`.
- [ ] Parse status starts as `pending` or appropriate local status.
- [ ] Unsupported file type returns validation error.
- [ ] Unknown session returns 404.
- [ ] No OCR is implemented.
- [ ] No AI, embedding, or benchmark logic is implemented.

## Verification

Run:

```bash
docker compose up --build
```

Then upload a sample TXT/PDF/DOCX file through the API docs or curl.

## Notes for Codex

- Do not store raw files in Postgres.
- Do not expose permanent MinIO credentials or unsigned private object URLs.
- Benchmark comparison will use extracted resume text in later phases, not this task.
