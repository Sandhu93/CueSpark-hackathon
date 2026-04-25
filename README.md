# CueSpark Interview Coach

**CueSpark Interview Coach** is a benchmark-driven AI interview readiness platform.

It helps candidates prepare for a target job by comparing their resume against the job description and a curated role-specific benchmark corpus, finding evidence gaps, and generating a strict interviewer-style mock interview from those gaps.

> Practice against the hiring bar, not just an AI chatbot.

---

## Why This Project Exists

A basic AI mock interview can be done with one good prompt.

CueSpark adds the missing layer: **benchmark comparison**.

Instead of only asking generic questions from a job description, CueSpark compares:

```txt
Candidate Resume ↔ Job Description ↔ Curated Benchmark Profiles ↔ Interview Performance
```

The system answers:

- What do stronger candidates show that this resume does not?
- Which claims are weakly evidenced?
- Where are metrics, ownership, business impact, tool depth, or project scale missing?
- What would a strict interviewer doubt after reading this resume?
- Which interview questions should be asked to test those weak areas?

---

## Current Implementation Target

This repository is being implemented as a **single-session, benchmark-driven, turn-based interview demo**.

The first stable milestone is:

```txt
Candidate pastes JD
  → uploads or pastes resume
  → system parses and embeds JD/resume
  → system creates JD-resume match analysis
  → system retrieves curated benchmark profiles
  → system compares candidate vs benchmark profiles
  → system shows benchmark gaps
  → system generates benchmark-driven interview questions
  → AI interviewer asks questions by voice
  → candidate records answers
  → system transcribes and evaluates answers
  → final benchmark-aware readiness report is generated
```

This is not a full SaaS product yet. The goal is to build a strong, controlled hackathon implementation with a clear novelty layer.

---

## Demo Flow

![Candidate Flow](docs/assets/candidate-flow.svg)

The intended user journey is:

1. Candidate enters the job description.
2. Candidate uploads or pastes the resume.
3. Backend creates an interview session.
4. Backend parses, chunks, and embeds the JD/resume.
5. Backend produces a basic JD-resume match analysis and role key.
6. Backend retrieves curated benchmark profiles for the role.
7. Backend compares candidate resume against benchmark profiles.
8. Frontend shows the **Benchmark Gap Dashboard**.
9. Backend generates questions from benchmark gaps.
10. Candidate completes a turn-based voice interview.
11. Backend transcribes and evaluates each answer.
12. Frontend shows the benchmark-aware final report.

The key demo screen is the benchmark dashboard, not the voice interview alone.

---

## System Architecture

![System Architecture](docs/assets/system-architecture.svg)

| Layer | Responsibility |
| --- | --- |
| Next.js frontend | Setup, match page, benchmark dashboard, interview room, final report |
| FastAPI backend | Session APIs, upload APIs, benchmark read API, question/answer/report APIs |
| Redis + RQ worker | Parsing, embedding, match analysis, benchmark comparison, TTS, transcription, evaluation, reports |
| Postgres + pgvector | Sessions, documents, benchmark profiles, benchmark comparisons, questions, answers, evaluations, reports, embeddings |
| MinIO | Resume uploads, generated interviewer audio, candidate answer recordings |
| OpenAI services | Embeddings, TTS, transcription, structured LLM analysis, question generation, report generation |

---

## Benchmark Engine

![Benchmark Engine Flow](docs/assets/benchmark-engine-flow.svg)

The benchmark engine is the novelty layer.

For the hackathon version, CueSpark uses **curated/anonymized benchmark profiles** stored as local fixtures. It does **not** scrape LinkedIn, Naukri, job boards, or personal resumes.

Initial benchmark roles:

```txt
project_manager
backend_developer
data_analyst
```

Each role should have 5 benchmark profiles:

```txt
1. Strong fresher / entry-level profile
2. Strong 2-3 year profile
3. Strong experienced profile
4. Domain-switcher profile
5. High-impact portfolio profile
```

Benchmark analysis produces:

```txt
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

These outputs feed the benchmark dashboard, question generation, answer evaluation, and final report.

Detailed design: [`docs/13-benchmark-engine-design.md`](docs/13-benchmark-engine-design.md)

---

## Data and Storage Model

![Data Storage Model](docs/assets/data-storage-model.svg)

Core tables:

```txt
interview_sessions
documents
benchmark_profiles
benchmark_comparisons
interview_questions
candidate_answers
answer_evaluations
interview_reports
embedding_chunks
```

Object storage paths:

```txt
resumes/original/{session_id}/{filename}
audio/questions/{question_id}.mp3
audio/answers/{answer_id}.webm
reports/{session_id}.json
```

Rules:

- Store structured data in Postgres.
- Store vectors in pgvector using `embedding_chunks`.
- Store binary files in MinIO.
- Store object keys in the database, not file bytes.
- Use local curated benchmark fixtures for the hackathon version.

---

## AI Voice and Transcription Pipeline

![AI Audio Pipeline](docs/assets/ai-audio-pipeline.svg)

The first version uses a reliable turn-based audio flow:

```txt
Benchmark-driven question text
  → OpenAI TTS
  → store interviewer audio in MinIO
  → frontend plays question audio
  → candidate records answer
  → upload answer audio
  → transcription
  → communication signal analysis
  → benchmark-aware answer evaluation
  → save scores and feedback
```

This avoids realtime WebRTC complexity while still giving a polished voice-interview experience.

---

## What Is In Scope

Version 1 includes:

- Single-session demo without login.
- Manual job description input.
- Resume upload and paste fallback.
- PDF/DOCX/TXT text extraction.
- OCR-ready parse status, but no OCR implementation.
- JD/resume chunking.
- OpenAI/mock embeddings.
- Postgres + pgvector vector storage.
- Basic JD-resume match analysis.
- Curated benchmark profile fixtures.
- Benchmark profile seeding.
- Benchmark profile embedding and retrieval.
- Candidate-vs-benchmark analysis.
- Benchmark read API for dashboard.
- Benchmark gap dashboard.
- Benchmark-driven interview question generation.
- On-demand interviewer TTS.
- Browser audio recording.
- Candidate audio upload.
- Transcription.
- Communication signal analysis.
- Benchmark-aware answer evaluation.
- Benchmark-aware final report.

Interview categories:

```txt
technical
project_experience
behavioral
hr
resume_gap
jd_skill_validation
benchmark_gap_validation
```

For non-software jobs, `technical` means role-specific competency, not programming.

---

## What Is Out of Scope

Do not build these in version 1 unless explicitly moved into scope:

- User login.
- Multi-user accounts.
- Payments or subscriptions.
- Recruiter/admin dashboard.
- Full WebRTC video interview.
- Realtime AI conversation.
- Monaco editor.
- Code compiler.
- Full OCR pipeline.
- Live scraping of LinkedIn/Naukri/job-board/personal resumes.
- Claims that benchmark profiles are verified hired-candidate resumes.
- Video confidence analysis.
- Emotion detection.
- Personality detection.
- Voice cloning.

Use safe wording:

```txt
benchmark profiles
curated top-candidate archetypes
role benchmark corpus
```

Avoid unsupported wording:

```txt
hired resumes
selected resumes
LinkedIn selected profiles
true confidence detection
emotion detection
```

---

## Tech Stack

| Area | Technology |
| --- | --- |
| Frontend | Next.js App Router, TypeScript, Tailwind |
| Backend API | FastAPI |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Queue | Redis + RQ |
| Object Storage | MinIO |
| AI Provider | OpenAI, with mock mode for local development |
| Interviewer Voice | OpenAI TTS |
| Transcription | OpenAI transcription / Whisper-compatible flow |
| Local Runtime | Docker Compose |

---

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

| Service | URL |
| --- | --- |
| Web | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MinIO Console | http://localhost:9001 |
| Postgres | localhost:5432 |
| Redis | localhost:6379 |

Default MinIO credentials:

```txt
minioadmin / minioadmin
```

---

## Required Environment Variables

The exact `.env.example` is the source of truth. The core variables are:

```env
AI_PROVIDER=openai
AI_MOCK_MODE=true
OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TTS_VOICE=marin
OPENAI_TRANSCRIBE_MODEL=gpt-4o-transcribe
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_DB=app
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

MINIO_ENDPOINT=minio:9000
MINIO_PUBLIC_ENDPOINT=http://localhost:9000
MINIO_BUCKET=uploads
MINIO_USE_SSL=false

NEXT_PUBLIC_API_URL=http://localhost:8000
```

Keep `AI_MOCK_MODE=true` during most local development so the full flow can be built without real AI calls.

---

## Backend Module Direction

Expected backend modules:

```txt
backend/app/api/
├── sessions.py
├── documents.py
├── benchmark.py
├── interview.py
├── audio.py
├── reports.py

backend/app/services/
├── openai_gateway.py
├── document_parser.py
├── chunking.py
├── embeddings.py
├── match_analyzer.py
├── benchmark_seed.py
├── benchmark_retrieval.py
├── benchmark_analyzer.py
├── question_generator.py
├── tts.py
├── transcription.py
├── communication_analysis.py
├── answer_evaluator.py
├── report_generator.py
├── prompts.py
```

Rules:

- Keep FastAPI routes thin.
- Put business logic in services.
- Put slow work in RQ tasks.
- Do not call OpenAI from frontend.
- Do not call OpenAI directly from route handlers.
- Store AI prompts in a prompt registry.
- Keep LLM outputs structured with Pydantic schemas.

---

## Frontend Route Direction

Expected frontend routes:

```txt
/
  Landing / start page

/setup
  Job description and resume input

/session/[sessionId]/match
  JD-resume match and preparation status

/session/[sessionId]/benchmark
  Benchmark gap dashboard

/session/[sessionId]/interview
  Turn-based benchmark-driven interview

/session/[sessionId]/report
  Benchmark-aware readiness report
```

The benchmark dashboard should be treated as the main novelty screen.

---

## Task Execution Order

Implementation tasks live in `tasks/` and should be executed one at a time.

Phase 0 is the foundation layer. After Phase 0, use this order:

```txt
PHASE 1 — Session + Documents
004 core session/document models
005 session API
006 resume upload/paste
007 document text extraction

PHASE 2 — Embeddings + Match
008 question/answer/evaluation/report/embedding models
009 chunking service
010 embedding service
011 match analysis service

PHASE 2.5 — Benchmark Engine
012 benchmark models
013 benchmark fixtures
014 benchmark seeding
015 benchmark embedding/retrieval
016 candidate-vs-benchmark analysis
017 benchmark read API
018 update question generation with benchmark gaps

PHASE 3 — Interview Engine
012 session preparation job
013 question generation service
014 question list API
015 on-demand TTS

PHASE 4 — Answer Flow
016 browser recording UI
017 answer upload API
018 transcription service
019 communication analysis

PHASE 5 — Evaluation + Report Backend
020 answer evaluation service
021 answer read API
022 final report service
023 report API

PHASE 6 — Frontend
024 frontend API client
025 setup and match pages
026 benchmark dashboard page
027 interview page
028 report page
029 loading/error/demo polish
```

When using Codex:

```txt
Read AGENTS.md, docs/00-project-overview.md, docs/01-architecture.md,
docs/08-implementation-sequence.md, docs/13-benchmark-engine-design.md,
and only the selected task file.

Implement only the selected task.
Do not add out-of-scope features.
Report changed files and verification steps.
```

---

## Scoring and Report Direction

The final report should include:

```txt
1. Overall readiness score
2. JD-resume match score
3. Benchmark similarity score
4. Resume competitiveness score
5. Evidence strength score
6. Missing benchmark signals
7. Interview risk areas
8. Answer-by-answer performance
9. Resume fixes based on benchmark gaps
10. Preparation plan
```

Each answer should be evaluated using:

| Metric | Description |
| --- | --- |
| Relevance | Did the answer address the question directly? |
| Role-specific depth | Did the candidate demonstrate actual competency? |
| Evidence/examples | Did the candidate provide concrete proof, examples, metrics, or ownership? |
| Benchmark gap coverage | Did the answer address the benchmark gap being tested? |
| JD alignment | Did the answer connect to the job requirements? |
| Clarity and structure | Was the answer organized and easy to follow? |
| Communication signal | Was the speech clear, concise, and low in avoidable hesitation? |

---

## Development Commands

```bash
make dev
make logs
make shell-api
make worker-restart
```

If Makefile commands are unavailable:

```bash
docker compose up --build
docker compose logs -f
docker compose restart worker
```

---

## Current Build Principle

Build the product in thin, verifiable layers.

Do not jump directly to the frontend or voice interview before the benchmark backend is working. The judge-facing value is:

```txt
Benchmark Gap Dashboard
  → Benchmark-driven questions
  → Benchmark-aware evaluation
  → Benchmark-aware final report
```
