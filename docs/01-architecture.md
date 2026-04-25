# 01 — Architecture

## Existing Template Base

The repository starts from a FastAPI + Next.js hackathon template with:

- FastAPI API service.
- Next.js frontend.
- Postgres.
- Redis.
- RQ worker.
- MinIO object storage.
- Upload endpoints.
- Generic job queue pattern.

Do not replace this architecture. Extend it.

## System Architecture

```text
Next.js frontend
  |-- paste JD/resume
  |-- upload resume/audio
  |-- show benchmark gap dashboard
  |-- play TTS audio
  |-- record candidate answer
  v
FastAPI API
  |-- thin route handlers
  |-- creates sessions/questions/answers/jobs
  |-- returns current state
  v
Postgres + pgvector
  |-- structured interview state
  |-- benchmark profiles
  |-- benchmark comparisons
  |-- vector embeddings
  |-- reports and evaluations
  v
Redis + RQ worker
  |-- parse documents
  |-- generate embeddings
  |-- generate match analysis
  |-- seed/retrieve benchmark profiles
  |-- generate benchmark gap analysis
  |-- generate benchmark-driven questions
  |-- generate TTS audio
  |-- transcribe answers
  |-- evaluate answers
  |-- generate final report
  v
MinIO
  |-- original resumes
  |-- generated TTS audio
  |-- candidate answer audio
  |-- optional report artifacts
```

## Modular Monolith Rule

The first version must remain a modular monolith.

Use modules, not microservices:

```text
backend/app/api/        FastAPI routers
backend/app/models/     SQLAlchemy tables
backend/app/schemas/    Pydantic request/response contracts
backend/app/services/   business logic and AI gateway wrappers
backend/app/tasks/      RQ background jobs
backend/app/core/       settings, db, redis, storage
```

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

For the hackathon, benchmark profiles are curated/anonymized fixtures. Do not live-scrape personal resumes.

## Request Lifecycle

### Session Preparation

```text
POST /sessions
  -> create interview_sessions row
  -> store JD text
  -> store resume text and/or resume object key

POST /sessions/{session_id}/prepare
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
  -> save questions
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
  -> return top 5 benchmark profiles

benchmark comparison
  -> compare JD, resume, and benchmark profiles
  -> identify missing skills, weak evidence, missing metrics, weak ownership signals, and interview risk areas
  -> save benchmark_comparisons row
```

### Question Audio

```text
POST /questions/{question_id}/tts
  -> generate or retrieve interviewer audio

worker/service
  -> call OpenAI TTS if not in mock mode
  -> store MP3/WAV in MinIO
  -> save tts_object_key on question
```

### Candidate Answer

```text
POST /questions/{question_id}/answers
  -> upload/store candidate audio
  -> create candidate_answers row
  -> enqueue transcribe_answer job

transcribe_answer job
  -> call OpenAI transcription or mock transcription
  -> save transcript and basic audio metadata
  -> compute communication signals
  -> enqueue/trigger evaluate_answer job

evaluate_answer job
  -> retrieve JD/resume/rubric/benchmark context
  -> evaluate answer using strict benchmark-aware rubric
  -> save answer_evaluations row
```

### Final Report

```text
POST /sessions/{session_id}/report
  -> enqueue generate_report job

worker
  -> aggregate session, match analysis, benchmark comparison, questions, answers, evaluations
  -> generate strict benchmark-aware final report
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
- Evaluation.
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
- `answer_evaluator.py`
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
  -> question audio
  -> answer recording
  -> transcript/evaluation status

/session/[sessionId]/report
  -> benchmark-aware readiness report
```

The benchmark dashboard is a core demo screen, not optional decoration.
