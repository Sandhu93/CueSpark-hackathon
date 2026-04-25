# Task: Add Interviewer Context Upload and Parser

## Goal

Allow the candidate to provide optional interviewer context using a LinkedIn-exported PDF or pasted text.

This task parses and stores interviewer context text only. It must not call AI or change interview questions yet.

## Scope

Implement only:

- `POST /api/sessions/{session_id}/interviewer-context`.
- Accept pasted interviewer text.
- Accept uploaded PDF file.
- Store uploaded PDF in MinIO.
- Extract text from LinkedIn-exported PDF using existing document parser patterns where possible.
- Create/update `interviewer_contexts` row.
- Mark weak/empty extraction as `ocr_required`.
- Add `GET /api/sessions/{session_id}/interviewer-context` if useful for debugging/UI.

## Out of Scope

Do not implement:

- LinkedIn scraping.
- Automatic LinkedIn login.
- AI interviewer-lens analysis.
- Question generation changes.
- Frontend UI.
- URL crawling.

## Files Likely Involved

- `backend/app/api/interviewer_context.py`
- `backend/app/services/document_parser.py`
- `backend/app/services/storage.py`
- `backend/app/models/interviewer_context.py`
- `backend/app/schemas/interviewer_context.py`
- Router registration file
- `backend/tests/`

## API Contract

### POST `/api/sessions/{session_id}/interviewer-context`

Supports either multipart upload or JSON paste input depending on the existing API style.

Suggested JSON request for pasted text:

```json
{
  "source_type": "manual",
  "raw_text": "Interviewer profile text pasted by candidate"
}
```

Suggested multipart fields for PDF upload:

```txt
file: PDF
source_type: linkedin_pdf
```

Response:

```json
{
  "id": "uuid",
  "session_id": "uuid",
  "source_type": "linkedin_pdf",
  "parse_status": "parsed",
  "analysis_status": "pending"
}
```

## Acceptance Criteria

- [ ] Candidate can upload a LinkedIn-exported PDF as interviewer context.
- [ ] Candidate can paste interviewer context text.
- [ ] Uploaded PDF is stored in MinIO.
- [ ] Extracted text is stored in `interviewer_contexts.extracted_text`.
- [ ] Weak/empty extraction sets `parse_status=ocr_required`.
- [ ] Unknown session returns 404.
- [ ] Endpoint does not scrape LinkedIn.
- [ ] Endpoint does not call OpenAI.
- [ ] Full interviewer context text is not logged.

## Verification

Run:

```bash
pytest backend/tests
```

Manual:

```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/interviewer-context
```

## Notes for Codex

- Treat this as user-provided context.
- Do not call it scraped data.
- Do not infer sensitive attributes.
- Do not generate questions in this task.
