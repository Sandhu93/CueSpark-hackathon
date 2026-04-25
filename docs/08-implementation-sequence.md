# Implementation Sequence

Build the project in this order only.

## Phase 0 — Foundation

1. Verify Docker stack boots.
2. Replace Postgres image with a pgvector-compatible image.
3. Add database extension setup for `vector`.
4. Add settings for OpenAI model names.
5. Add basic health checks.

Do not build interview features yet.

## Phase 1 — Session and Document Intake

1. Create interview session model.
2. Add JD paste input.
3. Add resume upload.
4. Add resume paste fallback.
5. Store uploaded resume in MinIO.
6. Extract text from PDF/DOCX/TXT.
7. Store parse status.

Do not add AI generation yet.

## Phase 2 — Embeddings and Match Analysis

1. Add chunking service.
2. Add embedding service.
3. Add `embedding_chunks` table.
4. Embed JD and resume chunks.
5. Generate JD-resume match analysis.

Do not build interview UI yet.

## Phase 3 — Interview Question Engine

1. Generate 10 base questions.
2. Store question category, difficulty, expected signal, and provenance.
3. Add question fetch endpoint.
4. Add on-demand TTS generation for one question.

Do not add adaptive follow-up yet unless explicitly requested.

## Phase 4 — Candidate Answer Flow

1. Record answer in frontend.
2. Upload answer audio to backend.
3. Store answer audio in MinIO.
4. Transcribe answer.
5. Store transcript.
6. Compute basic communication signals.

Do not generate final report yet.

## Phase 5 — Evaluation and Report

1. Evaluate each answer.
2. Store category scores.
3. Generate final readiness report.
4. Build report UI.

## Phase 6 — Polish

1. Improve UI consistency.
2. Add loading states.
3. Add error states.
4. Add retry behavior for failed jobs.
5. Add demo data.

## Future Scope

Do not implement until explicitly approved:

- Login
- Subscriptions
- Realtime WebRTC
- OCR
- Monaco editor
- Code compiler
- Recruiter dashboard
- Video confidence analysis
