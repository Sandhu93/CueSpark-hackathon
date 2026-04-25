# Task 012 — Document Parser, Chunking, and OCR Provision

## Goal

Implement text extraction and chunking for JD/resume documents while leaving clear provision for future OCR.

## Read First

- `docs/02-backend-design.md`
- `docs/03-database-design.md`
- `docs/04-ai-audio-rag-design.md`

## Requirements

1. Add `backend/app/services/document_parser.py`.
2. Add `backend/app/services/chunking.py`.
3. Support:
   - direct pasted text
   - PDF text extraction
   - DOCX text extraction
4. If extracted text is empty or weak, mark document as `ocr_required`.
5. Do not implement OCR.
6. Update `prepare_session` to parse documents and store extracted text.
7. Chunk JD and resume text into manageable chunks with metadata.

## Dependencies

Add parser libraries only if needed:

- `pypdf` or `pdfplumber`
- `python-docx`

Keep dependency choice simple.

## OCR Provision Rule

For scanned PDFs/images:

```text
parse_status = ocr_required
metadata.ocr_reason = "No extractable text found"
```

Frontend can later show paste fallback.

## Acceptance Criteria

- Pasted JD/resume works.
- Uploaded PDF/DOCX resume can be parsed when text is extractable.
- OCR-required files are detected and do not crash the worker.
- Chunking service has unit-testable pure functions.

## Out of Scope

- OCR implementation.
- Embedding generation.
- AI match scoring.
