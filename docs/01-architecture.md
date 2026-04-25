# 01 — Architecture

## Existing Template Base

The repository starts from a FastAPI + Next.js template with:

- FastAPI API service.
- Next.js frontend.
- Postgres.
- Redis.
- RQ worker.
- MinIO object storage.
- Upload endpoints.
- Generic job queue pattern.

Do not replace this architecture. Extend it as a modular monolith.

## Product Architecture

CueSpark is now a benchmark-driven, multimodal interview readiness product.

```text
Next.js frontend
  |-- JD/resume setup
  |-- benchmark gap dashboard
  |-- response-mode-aware interview room
  |-- audio/text/code answer capture
  |-- optional visual signal capture MVP
  |-- final readiness report
  v
FastAPI API
  |-- thin route handlers
  |-- sessions/questions/answers/jobs
  |-- benchmark read APIs
  |-- response capture APIs
  |-- report APIs
  v
Postgres + pgvector
  |-- structured interview state
  |-- benchmark profiles and comparisons
  |-- response metadata and transcripts
  |-- agent results
  |-- final answer evaluations and reports
  |-- vector embeddings
  v
Redis + RQ worker
  |-- prepare session pipeline
  |-- TTS generation
  |-- transcription
  |-- audio/text/code/video-signal agents
  |-- benchmark gap coverage agent
  |-- final evaluation orchestrator
  |-- report generation
  v
MinIO
  |-- original resumes
  |-- generated TTS audio
  |-- candidate answer audio
  |-- optional report artifacts
```

## Modular Monolith Rule

The first product version must remain a modular monolith.

Use modules, not microservices:

```text
backend/app/api/        FastAPI routers
backend/app/models/     SQLAlchemy tables
backend/app/schemas/    Pydantic request/response contracts
backend/app/services/   business logic, agents, and AI gateway wrappers
backend/app/tasks/      RQ background jobs
backend/app/core/       settings, db, redis, storage
```

The architecture should support future extraction into services, but the current product should not pay microservice complexity upfront.

## Benchmark Engine Position

The benchmark engine sits between basic JD-resume analysis and interview question generation.

```text
JD + Resume
  -> role inference / role key normalization
  -> benchmark profile retrieval
  -> candidate vs benchmark comparison
  -> benchmark gap analysis
  -> benchmark-driven question generation
```

Benchmark profiles are curated/anonymized fixtures or user-approved curated data. Do not live-scrape personal resumes by default.

## Multimodal Evaluation Position

The multimodal layer starts after a question is asked.

```text
Benchmark-driven question
  -> expected response mode
  -> candidate response capture
  -> modality-specific agents
  -> benchmark gap coverage agent
  -> final evaluation orchestrator
  -> readiness report
```

Supported response modes:

```text
spoken_answer
written_answer
code_answer
mixed_answer
```

Each mode activates only the relevant analyzers.

## Request Lifecycle

### Session Preparation

```text
POST /api/sessions
  -> create interview_sessions row
  -> store JD text
  -> store resume text and/or resume object key

POST /api/sessions/{session_id}/prepare
  -> enqueue prepare_session job

prepare_session job
  -> parse resume if upload exists
  -> normalize JD/resume text
  -> chunk JD/resume
  -> embed chunks
  -> generate basic match analysis
  -> infer/normalize role key
  -> retrieve top benchmark profiles
  -> compare candidate resume against benchmark profiles
  -> save benchmark_comparisons row
  -> generate benchmark-driven interview plan
  -> save questions with response_mode and required modality flags
  -> mark session ready
```

### Benchmark Retrieval and Comparison

```text
benchmark seed command/task
  -> load curated fixtures
  -> save benchmark_profiles rows
  -> chunk benchmark profile text
  -> save benchmark chunks in embedding_chunks

benchmark retrieval
  -> use role key first
  -> use vector similarity second
  -> return top benchmark profiles

benchmark comparison
  -> compare JD, resume, and benchmark profiles
  -> identify missing skills, weak evidence, missing metrics, weak ownership signals, and interview risk areas
  -> save benchmark_comparisons row
```

### Question Audio

```text
POST /api/questions/{question_id}/tts
  -> generate or retrieve interviewer audio

worker/service
  -> call OpenAI TTS if not in mock mode
  -> store MP3/WAV in MinIO
  -> save tts_object_key on question
```

### Multimodal Candidate Answer

```text
POST /api/questions/{question_id}/answers
  -> validate submitted payload against question response_mode
  -> store audio artifact in MinIO if present
  -> store text/code answer in Postgres if present
  -> create candidate_answers row
  -> enqueue relevant agent jobs
```

Mode examples:

```text
spoken_answer -> audio agent -> benchmark gap agent -> final orchestrator
written_answer -> text answer agent -> benchmark gap agent -> final orchestrator
code_answer -> code evaluation agent -> benchmark gap agent -> final orchestrator
mixed_answer -> relevant modality agents -> benchmark gap agent -> final orchestrator
```

### Audio Agent

```text
audio agent
  -> transcribe answer
  -> save transcript
  -> compute speaking pace, filler words, hesitation markers, answer structure
  -> save agent_results row
```

### Text Answer Agent

```text
text answer agent
  -> evaluate relevance, structure, evidence, completeness, clarity
  -> save agent_results row
```

### Code Evaluation Agent

```text
code evaluation agent
  -> static review of correctness, edge cases, complexity, readability, testability, explanation
  -> save agent_results row
```

Do not run arbitrary candidate code on the main backend. Future code execution requires sandboxing.

### Video Signal Agent MVP

```text
video signal agent
  -> accept frontend-provided or sampled metadata
  -> evaluate face in frame, lighting, camera presence, eye contact proxy, posture stability
  -> save summary in agent_results
```

Do not claim emotion detection, personality detection, truthfulness detection, or true confidence detection.

### Final Answer Evaluation

```text
final evaluation orchestrator
  -> read question metadata
  -> read candidate answer
  -> read available agent_results
  -> apply response-mode-specific scoring weights
  -> store answer_evaluations row
```

### Final Report

```text
POST /api/sessions/{session_id}/report
  -> enqueue generate_report job

worker
  -> aggregate session, match analysis, benchmark comparison, questions, answers, agent results, evaluations
  -> generate multimodal benchmark-aware final report
  -> save interview_reports row
```

## Why Background Jobs

Use jobs for operations that may take more than 1 second or call external AI APIs:

- Parsing files.
- Generating embeddings.
- Benchmark profile embedding.
- Benchmark comparison.
- Generating interview plan.
- TTS generation.
- Transcription.
- Text/code answer analysis.
- Video signal analysis.
- Benchmark gap coverage analysis.
- Final evaluation orchestration.
- Report generation.

Route handlers should return quickly.

## Storage Boundary

Postgres stores structured data and text required for query/evaluation.

MinIO stores binary artifacts:

```text
resumes/original/{session_id}/{filename}
audio/questions/{question_id}.mp3
audio/answers/{answer_id}.webm
reports/{session_id}.json
```

Do not store audio bytes in Postgres.

For video MVP, prefer storing metadata/summaries instead of full video files.

## Vector Storage Boundary

Use `embedding_chunks` for all semantic retrieval content:

```text
chunk_type = jd
chunk_type = resume
chunk_type = benchmark_profile
chunk_type = answer
chunk_type = rubric
chunk_type = question_bank
```

For benchmark chunks:

```text
owner_type = benchmark_profile
owner_id = benchmark_profiles.id
```

## AI Gateway Boundary

Create one OpenAI-facing service module. Suggested file:

```text
backend/app/services/openai_gateway.py
```

All OpenAI calls should go through this service or small wrappers that depend on it:

- `tts.py`
- `transcription.py`
- `embeddings.py`
- `match_analyzer.py`
- `benchmark_analyzer.py`
- `question_generator.py`
- `audio_agent.py`
- `text_answer_agent.py`
- `code_evaluation_agent.py`
- `benchmark_gap_agent.py`
- `final_evaluation_orchestrator.py`
- `report_generator.py`

Do not call OpenAI from FastAPI routes or React.

## Frontend Architecture

Expected screens:

```text
/setup
  -> JD and resume input

/session/[sessionId]/match
  -> basic match status and preparation progress

/session/[sessionId]/benchmark
  -> benchmark similarity
  -> hiring bar gap
  -> evidence gaps
  -> interview risk areas

/session/[sessionId]/interview
  -> AI interviewer question audio
  -> response-mode-aware capture
  -> audio recording, text answer, code answer, or mixed response
  -> transcript/evaluation status

/session/[sessionId]/report
  -> multimodal benchmark-aware readiness report
```

The benchmark dashboard and final report are core product screens, not optional decoration.
