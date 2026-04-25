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
  |-- vector embeddings
  |-- reports and evaluations
  v
Redis + RQ worker
  |-- parse documents
  |-- generate embeddings
  |-- generate match analysis
  |-- generate questions
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

## Request Lifecycle

### Session Preparation

```text
POST /sessions
  -> create interview_sessions row
  -> store JD text
  -> store resume text and/or resume object key
  -> enqueue prepare_session job

prepare_session job
  -> parse resume if upload exists
  -> normalize JD/resume text
  -> chunk JD/resume
  -> embed chunks
  -> generate match analysis
  -> generate base interview plan
  -> save questions
  -> mark session ready
```

### Question Audio

```text
POST /questions/{question_id}/tts
  -> enqueue generate_question_audio job

worker
  -> call OpenAI TTS
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
  -> call OpenAI transcription
  -> save transcript and basic audio metadata
  -> enqueue/trigger evaluate_answer job

evaluate_answer job
  -> retrieve JD/resume/rubric context
  -> evaluate answer using strict rubric
  -> save answer_evaluations row
```

### Final Report

```text
POST /sessions/{session_id}/report
  -> enqueue generate_report job

worker
  -> aggregate session, match analysis, questions, answers, evaluations
  -> generate strict final report
  -> save interview_reports row
```

## Why Background Jobs

Use jobs for operations that may take more than 1 second or call external AI APIs:

- Parsing files.
- Generating embeddings.
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

## AI Gateway Boundary

Create one OpenAI-facing service module. Suggested file:

```text
backend/app/services/openai_gateway.py
```

All OpenAI calls should go through this service or small wrappers that depend on it:

- `tts.py`
- `transcription.py`
- `embeddings.py`
- `question_generator.py`
- `answer_evaluator.py`
- `report_generator.py`

Do not call OpenAI from FastAPI routes or React.
