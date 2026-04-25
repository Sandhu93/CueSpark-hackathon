# 02 — Backend Design

## Backend Goal

Create a reliable benchmark-driven interview readiness engine, not a chatbot API.

The backend is responsible for:

- Session state.
- Document ingestion.
- Vector indexing.
- JD-resume match analysis.
- Curated benchmark profile management.
- Benchmark retrieval.
- Candidate-vs-benchmark comparison.
- Benchmark gap analysis.
- Benchmark-driven interview planning.
- Question audio generation.
- Candidate answer storage.
- Transcription.
- Benchmark-aware strict answer evaluation.
- Final benchmark-aware report generation.

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
  benchmark.py
  question.py
  answer.py
  evaluation.py
  report.py
  embedding.py

backend/app/schemas/
  session.py
  document.py
  benchmark.py
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
  benchmark_seed.py
  benchmark_retrieval.py
  benchmark_analyzer.py
  question_generator.py
  tts.py
  transcription.py
  communication_analysis.py
  answer_evaluator.py
  report_generator.py
  prompts.py

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
- Generate benchmark comparisons inline if it may be slow.

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

Use the existing task pattern in the repository. Do not invent a second job framework.

## Core Domain Concepts

### Interview Session

A single benchmark-driven mock interview attempt. No login is required in v1.

### Document

A JD or resume input. Can come from paste or upload.

### Embedding Chunk

A chunk of text stored with vector embedding and metadata.

Used for:

- JD chunks.
- Resume chunks.
- Benchmark profile chunks.
- Candidate answer chunks.
- Rubric/question-bank chunks if needed.

### Benchmark Profile

A curated/anonymized strong candidate archetype for a role.

For the hackathon version, benchmark profiles come from local fixtures, not live scraping.

### Benchmark Comparison

The structured output comparing the candidate resume against retrieved benchmark profiles.

It should include:

```text
benchmark_similarity_score
resume_competitiveness_score
evidence_strength_score
missing_skills
weak_skills
missing_metrics
weak_ownership_signals
interview_risk_areas
recommended_resume_fixes
question_targets
```

### Interview Question

A planned question with category, difficulty, expected signal, source/provenance, and optional benchmark gap reference.

If benchmark gaps exist, questions should not be generic.

### Candidate Answer

A candidate audio response and transcript for a specific question.

### Answer Evaluation

Strict rubric-based assessment of one answer, including whether the candidate addressed the benchmark gap being tested.

### Interview Report

Aggregated final benchmark-aware report for the session.

## OpenAI Model Configuration

Model names should be settings, not scattered constants.

Add to settings:

```text
AI_PROVIDER=openai
AI_MOCK_MODE=true
OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TTS_VOICE=marin
OPENAI_TRANSCRIBE_MODEL=gpt-4o-transcribe
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

If a model is changed later, implementation should not require editing multiple feature modules.

## Session Preparation Pipeline

`prepare_session` should eventually perform:

```text
1. Load session.
2. Parse resume if needed.
3. Normalize JD and resume text.
4. Chunk JD and resume.
5. Generate/store embeddings.
6. Generate JD-resume match analysis.
7. Infer/normalize role key.
8. Retrieve relevant benchmark profiles.
9. Generate benchmark comparison.
10. Generate benchmark-driven questions.
11. Mark session ready.
```

If benchmark comparison fails, session should be recoverable and should not silently fall back to generic questions without logging/state.

## Benchmark Rules

For v1:

- Use curated/anonymized benchmark fixtures.
- Do not scrape LinkedIn, Naukri, or personal websites.
- Do not claim benchmark profiles are verified hired-candidate resumes.
- Use safe wording: `benchmark profiles`, `curated top-candidate archetypes`, or `role benchmark corpus`.
- Store benchmark comparison as structured JSON fields, not only prose.
- Feed benchmark gaps into question generation and report generation.

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

For benchmark failures:

- Preserve session and match analysis.
- Store a clear failed/pending benchmark status where supported.
- Do not claim benchmark-driven results if no benchmark comparison exists.

For parsing failures:

- Preserve original file in MinIO.
- Mark document as `failed` or `ocr_required`.
- Return actionable frontend status.
