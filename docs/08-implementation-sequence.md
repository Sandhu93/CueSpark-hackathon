# 08 — Implementation Sequence

Build the project in thin, verifiable layers.

CueSpark is no longer only a hackathon mock demo. The target product is:

```txt
benchmark-driven + multimodal interview readiness platform
```

Do not jump ahead to advanced modalities before the spoken-answer loop is stable.

---

## Phase 0 — Foundation

1. Verify Docker stack boots.
2. Replace Postgres image with a pgvector-compatible image.
3. Add database extension setup for `vector`.
4. Add settings for OpenAI model names.
5. Add basic health checks.

Do not build interview features yet.

---

## Phase 1 — Session and Document Intake

1. Create interview session model.
2. Add JD paste input.
3. Add resume upload.
4. Add resume paste fallback.
5. Store uploaded resume in MinIO.
6. Extract text from PDF/DOCX/TXT.
7. Store parse status.

Do not add AI generation yet.

---

## Phase 2 — Embeddings and Match Analysis

1. Add chunking service.
2. Add embedding service.
3. Add `embedding_chunks` table.
4. Embed JD and resume chunks.
5. Generate basic JD-resume match analysis.

Do not build interview UI yet.

---

## Phase 2.5 — Benchmark Engine

This is the first product differentiator.

1. Add curated benchmark profile models.
2. Add benchmark profile fixtures per initial role.
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
9. Expose benchmark read API.
10. Feed benchmark gaps into question generation.

Do not add live web scraping. Use curated/anonymized benchmark fixtures first.

---

## Phase 3 — Benchmark-Driven Interview Question Engine

1. Generate 10 base questions using JD, resume, match analysis, and benchmark gap analysis.
2. Store question category, difficulty, expected signal, provenance, and benchmark gap reference where applicable.
3. Add response-mode fields to generated questions if this is already in scope.
4. Add question fetch endpoint.
5. Add on-demand TTS generation for one question.

Do not add adaptive follow-up yet unless explicitly requested.

---

## Phase 4 — Multimodal Response Capture and Modality Agents

This phase replaces the older simple answer-flow phase.

Recommended execution order:

```txt
024-add-response-modality-model.md
025-update-answer-upload-for-multimodal.md
026-add-audio-transcription-agent.md
027-add-text-answer-agent.md
028-add-code-evaluation-agent.md
029-add-video-signal-agent-mvp.md
```

### 4A — Response Modality Model

Add support for:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
```

Questions should declare:

```txt
response_mode
requires_audio
requires_video
requires_text
requires_code
```

Answers should support:

```txt
audio_object_key
transcript
text_answer
code_answer
code_language
communication_metadata
visual_signal_metadata
```

### 4B — Multimodal Answer Upload

Support answer submission based on response mode:

- spoken answer: audio
- written answer: text
- code answer: code + language
- mixed answer: relevant combination

Do not evaluate answers inside the upload endpoint.

### 4C — Audio Agent

First real product milestone after TTS.

The audio agent should:

- transcribe audio
- compute word count
- compute speaking pace
- detect filler words
- identify hesitation markers
- summarize answer structure
- store safe communication metrics

### 4D — Text Answer Agent

Analyze written answers for:

- relevance
- structure
- specificity
- evidence
- completeness
- clarity

### 4E — Code Evaluation Agent

Analyze code answers for:

- correctness
- edge cases
- complexity
- readability
- testability
- explanation quality

Do not execute arbitrary code on the main backend. Future execution requires a sandbox.

### 4F — Video Signal Agent MVP

Analyze safe observable visual signals only:

- face in frame
- lighting quality
- eye contact proxy
- posture stability
- camera presence

Do not implement emotion detection, personality scoring, truthfulness detection, or true confidence detection.

---

## Phase 5 — Multimodal Evaluation and Report

Recommended execution order:

```txt
030-add-agent-result-storage.md
031-add-benchmark-gap-agent.md
032-add-final-evaluation-orchestrator.md
033-add-multimodal-readiness-report.md
```

### 5A — Agent Result Storage

Add a durable table for modality-agent outputs:

```txt
agent_results
```

This lets agents run independently and allows the final evaluator to combine available outputs.

### 5B — Benchmark Gap Coverage Agent

Evaluate whether the candidate response addressed the benchmark gap that caused the question to be asked.

This is the core CueSpark scoring idea:

```txt
Did the candidate prove the gap CueSpark identified?
```

### 5C — Final Evaluation Orchestrator

Combine agent outputs into answer-level evaluation.

Scoring should change by response mode.

Spoken answer example:

```txt
benchmark gap coverage: 30%
answer relevance: 20%
evidence/examples: 20%
communication clarity: 15%
role-specific depth: 10%
visual/audio professionalism: 5%
```

Code answer example:

```txt
code correctness: 35%
reasoning/explanation: 20%
complexity: 15%
edge cases: 15%
readability/testability: 10%
benchmark relevance: 5%
```

### 5D — Multimodal Readiness Report

Aggregate:

- benchmark comparison
- questions
- answers
- transcripts
- agent results
- answer evaluations

Generate a final readiness report with:

- readiness score
- hiring-style recommendation without guarantee
- benchmark gap coverage
- communication summary
- written-answer summary if available
- code-quality summary if available
- visual-signal summary if available
- resume improvements
- preparation plan

---

## Phase 6 — Product Frontend

Build the production frontend around the real backend flow:

1. Frontend API client.
2. Setup and match pages.
3. Benchmark dashboard.
4. Response-mode-aware interview page.
5. Multimodal answer submission UI.
6. Evaluation status UI.
7. Multimodal readiness report page.
8. Loading, retry, and failure states.

The old hackathon `/demo` routes may remain for product preview only, but production development should focus on real `/session/[sessionId]/*` routes.

---

## Future Scope

Do not implement until explicitly approved:

- Login
- Subscriptions
- Recruiter dashboard
- Realtime WebRTC
- Full video recording storage
- OCR implementation
- Monaco editor production integration
- Sandboxed code execution
- Live scraping of personal resumes from LinkedIn, Naukri, or similar platforms
- Emotion detection
- Personality scoring
- True confidence detection
- Truthfulness detection

---

## Important Product Positioning

CueSpark is not a mock interview chatbot.

CueSpark is a benchmark-driven, multimodal interview readiness engine.

It compares a candidate against role-specific benchmark profiles, finds evidence gaps, asks questions focused on those gaps, captures the candidate's response through the relevant modality, and evaluates whether the candidate actually proved the gap.
