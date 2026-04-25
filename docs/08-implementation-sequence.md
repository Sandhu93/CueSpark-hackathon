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
5. Generate basic JD-resume match analysis.

Do not build interview UI yet.

## Phase 2.5 — Benchmark Engine

This is the hackathon novelty layer.

1. Add curated benchmark profile models.
2. Add 5 benchmark profile fixtures per demo role.
3. Seed benchmark profiles into Postgres.
4. Chunk and embed benchmark profile content.
5. Retrieve the most relevant benchmark profiles for a session role/JD.
6. Compare:
   - JD vs candidate resume
   - JD vs benchmark profiles
   - candidate resume vs benchmark profiles
7. Generate benchmark gap analysis:
   - missing skills
   - weak evidence
   - missing metrics
   - weak ownership signals
   - interview risk areas
8. Store benchmark comparison results.

Do not add live web scraping in the hackathon version. Use curated/anonymized benchmark fixtures first.

## Phase 3 — Benchmark-Driven Interview Question Engine

1. Generate 10 base questions using JD, resume, match analysis, and benchmark gap analysis.
2. Store question category, difficulty, expected signal, provenance, and benchmark gap reference where applicable.
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

## Phase 5 — Benchmark-Aware Evaluation and Report

1. Evaluate each answer against the question, JD, resume, and benchmark gap being tested.
2. Store category scores.
3. Generate final readiness report.
4. Include benchmark similarity, resume evidence gaps, answer quality, and readiness score.
5. Build report UI.

## Phase 6 — Polish

1. Improve UI consistency.
2. Add loading states.
3. Add error states.
4. Add retry behavior for failed jobs.
5. Add demo data.
6. Add clear benchmark explanation for judges.

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
- Live scraping of personal resumes from LinkedIn, Naukri, or similar platforms

## Important Hackathon Positioning

CueSpark is not just a mock interview chatbot.

CueSpark is a benchmark-driven interview readiness engine. It compares a candidate against a role-specific benchmark set of stronger candidate profiles, finds the evidence gaps, and generates an interview focused on those gaps.
