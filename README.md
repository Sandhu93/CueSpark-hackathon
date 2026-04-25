# CueSpark Interview Coach

**CueSpark Interview Coach** is a benchmark-driven AI interview readiness platform for job seekers and experienced professionals preparing for role transitions.

Instead of only generating mock interview questions from a job description and resume, CueSpark compares the candidate against a role-specific benchmark set of stronger candidate profiles. It identifies missing skills, weak evidence, missing metrics, weak ownership signals, and interview risk areas, then generates a strict interviewer-style mock interview focused on those gaps.

> Practice against the hiring bar, not just an AI chatbot.

This project uses a production-friendly architecture based on **FastAPI**, **Next.js**, **Postgres + pgvector**, **Redis/RQ workers**, **MinIO**, and **OpenAI audio/LLM services**.

---

## Core Product Goal

CueSpark helps candidates understand how far they are from the hiring bar for a target role.

The first version is a **single-session, benchmark-driven, turn-based interview demo**. It does not include accounts, payments, recruiter dashboards, realtime video rooms, live scraping, or WebRTC conversation.

---

## What Makes This Different

A normal LLM prompt can generate interview questions from a JD and resume. CueSpark adds a benchmark layer:

```txt
Candidate Resume ↔ Job Description ↔ Benchmark Profiles ↔ Interview Performance
```

The system answers:

- What do stronger candidates show that this resume does not?
- Which skills are present but weakly evidenced?
- Where are metrics, ownership, business impact, or project depth missing?
- What would a strict interviewer doubt after reading this resume?
- Which questions should be asked to test those weak areas?

---

## Architecture Overview

![System Architecture](docs/assets/system-architecture.svg)

| Layer | Responsibility |
| --- | --- |
| Next.js frontend | Setup flow, benchmark dashboard, interview UI, audio recording, report UI |
| FastAPI backend | Session APIs, upload APIs, job orchestration, AI service coordination |
| Redis + RQ worker | Parsing, embedding, benchmark comparison, transcription, evaluation, report generation |
| Postgres + pgvector | Structured data, interview state, benchmark profiles, embeddings, reports |
| MinIO | Resume files, generated interviewer audio, candidate answer recordings |
| OpenAI services | TTS, transcription, embeddings, benchmark analysis, question generation, answer evaluation |

---

## Candidate Flow

![Candidate Flow](docs/assets/candidate-flow.svg)

The first release should support this flow:

1. Candidate pastes a job description.
2. Candidate uploads or pastes a resume.
3. Backend creates an interview session.
4. Resume and JD are parsed, chunked, and embedded.
5. System generates basic JD-resume match analysis.
6. System retrieves curated benchmark profiles for the inferred role.
7. System compares:
   - JD vs candidate resume
   - JD vs benchmark profiles
   - candidate resume vs benchmark profiles
8. System finds benchmark gaps:
   - missing skills
   - weak evidence
   - missing metrics
   - weak ownership signals
   - interview risk areas
9. System generates benchmark-driven interview questions.
10. AI interviewer asks one question at a time using generated voice.
11. Candidate records an answer.
12. Backend transcribes and evaluates the answer.
13. Final benchmark-aware readiness report is generated.

---

## Benchmark Engine

The benchmark engine is the novelty layer.

For the hackathon version, CueSpark uses curated/anonymized benchmark profiles stored in the repository. It does **not** live-scrape personal resumes from LinkedIn, Naukri, or similar platforms.

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

Benchmark outputs include:

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
benchmark_driven_question_targets
```

Detailed design: [`docs/13-benchmark-engine-design.md`](docs/13-benchmark-engine-design.md)

---

## AI Voice and Transcription Pipeline

![AI Audio Pipeline](docs/assets/ai-audio-pipeline.svg)

The first version uses a reliable turn-based audio pipeline:

```txt
Benchmark-driven question text
  → OpenAI TTS
  → store interviewer audio in MinIO
  → frontend plays question audio
  → candidate records answer
  → upload answer audio
  → OpenAI transcription
  → communication signal analysis
  → benchmark-aware answer evaluation
  → save scores and feedback
```

This avoids realtime WebRTC complexity while still giving a polished voice-interview experience.

---

## Data and Storage Model

![Data Storage Model](docs/assets/data-storage-model.svg)

Use Postgres for structured application data and MinIO for large binary artifacts.

### Core Tables

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

### Object Storage Paths

```txt
resumes/original/{session_id}/{filename}
audio/questions/{question_id}.mp3
audio/answers/{answer_id}.webm
reports/{session_id}.json
```

The database should store object keys, not raw files.

---

## Product Scope

### In Scope for Version 1

- Manual job description input
- Resume upload and paste fallback
- PDF/DOCX/text parsing
- OCR-ready parse status, but no OCR implementation yet
- JD and resume chunking
- Embedding storage using Postgres + pgvector
- Basic JD-resume match scoring
- Curated benchmark profile fixtures
- Benchmark profile seeding
- Benchmark profile embedding and retrieval
- Candidate-vs-benchmark comparison
- Benchmark gap dashboard
- Benchmark-driven mixed interview question generation
- Turn-based interview flow
- OpenAI-generated interviewer voice
- Candidate audio recording and upload
- Candidate audio transcription
- Benchmark-aware answer evaluation
- Communication signal scoring
- Benchmark-aware final readiness report

### Interview Categories

The interview plan should generate questions across these categories:

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

## Out of Scope for Version 1

Do not implement these unless explicitly moved into scope:

- User login
- Multi-user accounts
- Payments or subscriptions
- Recruiter dashboard
- Admin dashboard
- Realtime AI conversation
- Google Meet-style video room
- Monaco editor
- Code compiler
- Full OCR pipeline
- Live scraping of personal resumes from LinkedIn/Naukri/job boards
- Claims that benchmark profiles are verified hired-candidate resumes
- Video-based confidence analysis
- Emotion detection
- Personality detection
- Custom voice cloning

---

## Tech Stack

| Area | Technology |
| --- | --- |
| Frontend | Next.js App Router |
| Backend API | FastAPI |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Queue | Redis + RQ |
| Object Storage | MinIO |
| AI Provider | OpenAI |
| Interviewer Voice | OpenAI TTS |
| Transcription | OpenAI transcription / Whisper-compatible flow |
| Local Runtime | Docker Compose |

---

## Recommended AI Services

| Capability | Recommended Direction |
| --- | --- |
| Interviewer voice | OpenAI TTS with professional interviewer instructions |
| Candidate transcription | OpenAI transcription model or Whisper-compatible flow |
| Embeddings | OpenAI text embeddings |
| Match analysis | LLM service module |
| Benchmark analysis | LLM service module with structured output |
| Question generation | LLM service module using benchmark gaps |
| Answer evaluation | LLM service module with benchmark-aware rubric |
| Final report | LLM service module with strict interviewer tone |

All AI calls should be isolated inside backend service modules. Do not call OpenAI directly from frontend pages or route handlers.

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

```env
AI_PROVIDER=openai
AI_MOCK_MODE=true
OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TRANSCRIBE_MODEL=gpt-4o-transcribe
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=cuespark_interview
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=cuespark
MINIO_SECURE=false

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## Backend Module Direction

Expected backend modules:

```txt
backend/app/api/
├── sessions.py
├── documents.py
├── interview.py
├── audio.py
├── reports.py

backend/app/services/
├── openai_client.py
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

Keep route handlers thin. Business logic should live in services. Slow operations should be run through workers.

---

## Frontend Route Direction

Expected frontend routes:

```txt
/
  Landing / start page

/setup
  Job description and resume input

/session/[sessionId]/match
  JD-resume match and session preparation status

/session/[sessionId]/benchmark
  Benchmark gap dashboard

/session/[sessionId]/interview
  Turn-based benchmark-driven mock interview

/session/[sessionId]/report
  Final benchmark-aware readiness report
```

Frontend API calls should be centralized inside `frontend/src/lib`.

---

## Scoring Rubric

The final report should include:

```txt
1. Overall readiness score
2. JD-resume match score
3. Benchmark similarity score
4. Resume competitiveness score
5. Evidence strength score
6. Missing benchmark signals
7. Interview risk radar
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

## Communication Signal Analysis

The first version may estimate communication quality using measurable signals:

- transcript length
- word count
- speaking speed
- filler words
- repetition
- answer structure
- clarity
- hesitation markers
- relevance to question

Use this language:

```txt
communication signal score
```

Avoid unsupported claims such as:

```txt
emotion detection
true confidence detection
personality detection
```

---

## Development Commands

```bash
make dev
make logs
make shell-api
make worker-restart
```

If Makefile commands are unavailable, use Docker Compose directly:

```bash
docker compose up --build
docker compose logs -f
docker compose restart worker
```

---

## Task-Based Development

Implementation tasks live in `tasks/` and should be executed one at a time.

Recommended order:

```txt
phase0-foundation
phase1-session-documents
phase2-embeddings-match
phase2-benchmark-engine
phase3-interview-engine
phase4-answer-flow
phase5-evaluation-report
phase6-frontend-polish
```

When using Codex or another coding agent:

```txt
Read AGENTS.md, docs/08-implementation-sequence.md, docs/13-benchmark-engine-design.md, and only the selected task file.
Implement only the selected task.
Do not add out-of-scope features.
Report changed files and verification steps.
```

---

## Current Milestone

The first stable milestone is:

```txt
A candidate can paste a JD, upload or paste a resume, compare their resume against curated benchmark profiles, see benchmark evidence gaps, generate a benchmark-driven interview, hear AI-spoken questions, record spoken answers, receive transcriptions, get strict benchmark-aware feedback, and view a final readiness report.
```
