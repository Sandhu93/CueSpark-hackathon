# 02 — Backend Design

## Backend Goal

Create a reliable interview engine, not a chatbot API.

The backend is responsible for:

- Session state.
- Document ingestion.
- Vector indexing.
- Interview planning.
- Question audio generation.
- Candidate answer storage.
- Transcription.
- Strict answer evaluation.
- Final report generation.

## Suggested Backend Files

```text
backend/app/api/
  sessions.py
  documents.py
  interview.py
  audio.py
  reports.py

backend/app/models/
  session.py
  document.py
  question.py
  answer.py
  evaluation.py
  report.py
  embedding.py

backend/app/schemas/
  session.py
  document.py
  question.py
  answer.py
  evaluation.py
  report.py
  ai_outputs.py

backend/app/services/
  openai_gateway.py
  document_parser.py
  chunking.py
  embeddings.py
  match_analyzer.py
  question_generator.py
  tts.py
  transcription.py
  communication_analysis.py
  answer_evaluator.py
  report_generator.py

backend/app/tasks/
  prepare_session.py
  generate_question_audio.py
  transcribe_answer.py
  evaluate_answer.py
  generate_report.py
```

## Route Handler Rules

Routes should:

- Validate request.
- Create or read database records.
- Enqueue jobs when work is long-running.
- Return typed response.

Routes should not:

- Build prompts.
- Call OpenAI.
- Parse large documents inline.
- Transcribe audio inline.
- Evaluate answers inline.

## Task Lifecycle Pattern

Every worker task should follow this lifecycle:

```text
1. Read job/session/entity from DB.
2. Mark job running where applicable.
3. Do the work.
4. Save durable output.
5. Mark status succeeded.
6. On failure, store error and mark failed.
```

Use the existing `backend/app/tasks/dummy.py` as the pattern.

## Core Domain Concepts

### Interview Session

A single mock interview attempt. No login is required in v1.

### Document

A JD or resume input. Can come from paste or upload.

### Embedding Chunk

A chunk of text stored with vector embedding and metadata.

### Interview Question

A planned or adaptive question with category, difficulty, expected signal, and optional TTS audio.

### Candidate Answer

A candidate audio response and transcript for a specific question.

### Answer Evaluation

Strict rubric-based assessment of one answer.

### Interview Report

Aggregated final report for the session.

## OpenAI Model Configuration

Model names should be settings, not scattered constants.

Add to settings:

```text
OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TTS_VOICE=marin
OPENAI_TRANSCRIBE_MODEL=gpt-4o-transcribe
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

If a model is changed later, implementation should not require editing multiple feature modules.

## Document Parsing Rules

Supported now:

- Manual pasted text.
- PDF text extraction.
- DOCX text extraction.

Provision for later:

- OCR for scanned PDFs/images.

Parsing output should include:

```text
extracted_text
parse_status: parsed | failed | ocr_required
metadata: file type, page count if available, character count
```

If a resume upload has little or no extractable text, mark `ocr_required` and let the frontend show a paste fallback.

## Communication Analysis Rules

Use measurable signals only:

- Transcript word count.
- Approximate words per minute.
- Filler word count.
- Hesitation markers.
- Answer structure.
- Relevance to question.

Do not claim true emotion detection or true confidence detection. Use `communication_signal_score`, not `confidence_detection_score`.

## Error Handling

For AI failures:

- Store the error in the job.
- Keep the session recoverable.
- Allow retrying TTS/transcription/evaluation.
- Do not delete uploaded audio or original documents.

For parsing failures:

- Preserve original file in MinIO.
- Mark document as `failed` or `ocr_required`.
- Return actionable frontend status.
