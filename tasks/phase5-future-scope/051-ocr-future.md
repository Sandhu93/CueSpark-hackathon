# Task 051 — OCR Future Scope

## Status

Future scope. Do not implement OCR in initial build.

## Current Provision

The document parser should mark scanned/unreadable resumes as:

```text
parse_status = ocr_required
```

Frontend should allow paste fallback.

## Future OCR Options

Possible services/tools:

- Tesseract for local OCR.
- Google Vision API.
- AWS Textract.
- Azure Document Intelligence.

## Future Flow

```text
resume upload
  -> normal text extraction fails
  -> mark ocr_required
  -> OCR job runs
  -> extracted text saved
  -> chunks regenerated
  -> embeddings regenerated
```
