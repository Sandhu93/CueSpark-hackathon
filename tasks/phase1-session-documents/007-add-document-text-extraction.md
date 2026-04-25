# Task: Add Document Text Extraction

## Goal

Extract text from uploaded resume files and store the extracted text for later AI processing.

## Scope

Implement only:

- Text extraction service for TXT.
- Text extraction service for PDF.
- Text extraction service for DOCX.
- Update document parse status after extraction.
- Mark weak/empty extraction as `ocr_required`.

## Out of Scope

Do not implement:

- OCR.
- AI analysis.
- Embeddings.
- Question generation.
- Advanced resume structuring.

## Files Likely Involved

- `backend/app/services/document_parser.py`
- `backend/app/tasks/`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/tests/`

## API Contract

No new public endpoint is required unless the existing job system requires one.

## Data Model Changes

Use existing `documents.extracted_text` and `documents.parse_status`.

## Acceptance Criteria

- [ ] TXT extraction works.
- [ ] PDF extraction works for text-based PDFs.
- [ ] DOCX extraction works.
- [ ] Empty or very weak extraction sets `parse_status=ocr_required`.
- [ ] Failed extraction sets `parse_status=failed` with safe metadata.
- [ ] Extracted text is stored in the document row.
- [ ] No OCR implementation is added.

## Verification

Run:

```bash
pytest backend/tests
```

If no tests exist, add a minimal parser test using fixture files or simple temp files.

## Notes for Codex

- Keep extraction deterministic and local.
- Do not call OpenAI in this task.
- Do not log full resume text.
