# 02 — Backend Design

## Backend Goal

Create a reliable benchmark-driven, multimodal interview readiness engine, not a chatbot API.

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
- Response-mode-aware candidate answer storage.
- Audio transcription and communication signal analysis.
- Written answer analysis.
- Code answer static evaluation.
- Safe video/visual signal summary MVP.
- Benchmark gap coverage analysis.
- Final answer evaluation orchestration.
- Final multimodal benchmark-aware report generation.

## Suggested Backend Files

```text
backend/app/api/
  sessions.py
  documents.py
  benchmark.py
  interview.py
  audio.py
  reports.py

backend/app/models/
  session.py
  document.py
  benchmark_profile.py
  benchmark_comparison.py
  question.py
  answer.py
  agent_result.py
  evaluation.py
  report.py
  embedding_chunk.py

backend/app/schemas/
  session.py
  document.py
  benchmark.py
  question.py
  answer.py
  agent_results.py
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
  audio_agent.py
  text_answer_agent.py
  code_evaluation_agent.py
  video_signal_agent.py
  benchmark_gap_agent.py
  final_evaluation_orchestrator.py
  report_generator.py
  prompts.py

backend/app/tasks/
  prepare_session.py
  generate_question_audio.py
  process_audio_answer.py
  analyze_text_answer.py
  analyze_code_answer.py
  analyze_video_signals.py
  analyze_benchmark_gap_coverage.py
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
- Run modality agents inline if the work is slow.
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

Use the existing RQ/task pattern. Do not invent a second job framework.

## Core Domain Concepts

### Interview Session

A benchmark-driven interview attempt. Login can be added later, but the product flow should not depend on accounts initially.

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

Benchmark profiles should not be described as verified hired-candidate resumes unless that is actually true.

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

A planned question with category, difficulty, expected signal, source/provenance, benchmark gap references, and response-mode requirements.

Each question should include:

```text
response_mode: spoken_answer | written_answer | code_answer | mixed_answer
requires_audio
requires_video
requires_text
requires_code
```

If benchmark gaps exist, questions should not be generic.

### Candidate Answer

A candidate response to a question.

It can include:

- audio object key
- transcript
- text answer
- code answer
- code language
- visual signal metadata
- response mode

### Agent Result

A structured output from one modality or evaluation agent.

Agent types:

```text
audio
text_answer
code_evaluation
video_signal
benchmark_gap
final_orchestrator
```

### Answer Evaluation

Final answer-level scoring produced by the final evaluation orchestrator. It combines relevant agent outputs based on response mode.

### Interview Report

Aggregated final multimodal benchmark-aware report for the session.

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

`prepare_session` should perform:

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
11. Add default response mode and modality flags to questions.
12. Mark session ready.
```

If benchmark comparison fails, session should be recoverable and should not silently fall back to generic questions without logging/state.

## Multimodal Answer Pipeline

After question delivery and TTS:

```text
1. Candidate submits response based on question.response_mode.
2. Backend validates required modalities.
3. Backend stores audio in MinIO if present.
4. Backend stores text/code content in Postgres if present.
5. Backend creates candidate_answers row.
6. Backend enqueues relevant modality-agent jobs.
7. Agents write agent_results rows.
8. Benchmark gap agent checks whether the response addressed the tested gap.
9. Final evaluation orchestrator writes answer_evaluations row.
10. Report generator aggregates evaluations into interview_reports.
```

## Benchmark Rules

For v1:

- Use curated/anonymized benchmark fixtures.
- Do not scrape LinkedIn, Naukri, or personal websites by default.
- Do not claim benchmark profiles are verified hired-candidate resumes.
- Use safe wording: `benchmark profiles`, `curated top-candidate archetypes`, or `role benchmark corpus`.
- Store benchmark comparison as structured JSON fields, not only prose.
- Feed benchmark gaps into question generation, agent scoring, and report generation.

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

## Communication and Visual Signal Rules

Use measurable or observable signals only:

- Transcript word count.
- Approximate words per minute.
- Filler word count.
- Hesitation markers.
- Answer structure.
- Relevance to question.
- Face in frame.
- Lighting quality.
- Eye contact proxy.
- Posture stability.
- Camera presence.

Do not claim true emotion detection, true confidence detection, personality scoring, truthfulness detection, or hiring guarantees.

## Code Evaluation Rules

Initial product version should use static review and structured LLM-based analysis.

Evaluate:

- correctness
- edge cases
- complexity
- readability
- testability
- explanation quality

Do not execute arbitrary candidate code on the main backend. Future runtime execution must use a sandboxed worker/container.

## Error Handling

For AI failures:

- Store the error in the job or agent result.
- Keep the session recoverable.
- Allow retrying TTS/transcription/evaluation.
- Do not delete uploaded audio or original documents.

For benchmark failures:

- Preserve session and match analysis.
- Store a clear failed/pending benchmark status where supported.
- Do not claim benchmark-driven results if no benchmark comparison exists.

For modality-agent failures:

- Store failed agent status.
- Let final orchestrator use available agent results.
- Do not block all evaluation because an optional agent failed.

For parsing failures:

- Preserve original file in MinIO.
- Mark document as `failed` or `ocr_required`.
- Return actionable frontend status.
