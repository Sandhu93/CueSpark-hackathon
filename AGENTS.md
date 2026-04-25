# AGENTS.md — CueSpark Interview Coach

Instructions for AI coding agents working in this repository.

## Project Identity

This repository is being converted from a generic FastAPI + Next.js hackathon template into **CueSpark Interview Coach**: a benchmark-driven AI interview readiness platform for job seekers and experienced professionals switching roles.

The system must not become a generic chatbot, a coding-only interview tool, or a full video meeting clone. The first version is a single-session demo with a strong benchmark engine foundation.

## Product Differentiation

CueSpark is not just a mock interview generator.

The core novelty is the benchmark layer:

```txt
Candidate Resume ↔ Job Description ↔ Benchmark Profiles ↔ Interview Performance
```

The app compares the candidate against role-specific curated benchmark profiles, identifies what stronger candidates show that this candidate does not, and generates interview questions from those gaps.

## Locked Product Scope

Build only this initial flow:

1. Candidate pastes a job description.
2. Candidate uploads or pastes a resume/CV.
3. Backend parses and stores the resume/JD.
4. Backend chunks and embeds JD/resume data using Postgres + pgvector.
5. Backend generates basic JD-resume match analysis.
6. Backend loads curated/anonymized benchmark profiles for the inferred role.
7. Backend chunks and embeds benchmark profile content.
8. Backend retrieves the most relevant benchmark profiles for the session.
9. Backend compares:
   - JD vs candidate resume
   - JD vs benchmark profiles
   - candidate resume vs benchmark profiles
10. Backend generates benchmark gap analysis:
   - missing skills
   - weak evidence
   - missing metrics
   - weak ownership signals
   - interview risk areas
11. AI generates a 10-question benchmark-driven interview plan.
12. Interview is turn-based: one question at a time.
13. OpenAI TTS generates interviewer audio for each question on demand.
14. Candidate records an audio answer in the browser.
15. Backend stores candidate audio in MinIO.
16. Backend transcribes the answer.
17. Backend evaluates the answer using a strict benchmark-aware interviewer rubric.
18. Backend generates a final benchmark-aware readiness report.

## Explicitly Out of Scope for Initial Version

Do not build these unless a task file explicitly asks for them:

- User accounts, login, organizations, teams, billing, subscriptions.
- Real-time WebRTC interview mode.
- Full Google Meet-like video call experience.
- Facial emotion detection or true confidence detection.
- Monaco editor or code execution.
- LinkedIn/Naukri/job-board scraping.
- Live scraping of personal resumes from the internet.
- Claims that benchmark profiles are verified hired-candidate resumes.
- OCR pipeline implementation.
- Admin dashboard.
- B2B recruiter workflow.
- Microservices or Kubernetes.

## Stack

Use the existing template stack:

- Backend: FastAPI, SQLAlchemy 2, Pydantic v2, RQ, Redis, MinIO, Postgres.
- Frontend: Next.js App Router, TypeScript, Tailwind.
- Database: local Docker Postgres with pgvector.
- Storage: MinIO for resumes, TTS audio, candidate answer audio, and report artifacts.
- AI gateway: centralized OpenAI access through service modules only.

## Architectural Rules

- Keep a modular monolith.
- Keep FastAPI routes thin.
- Put business logic in `backend/app/services/`.
- Put long-running work in `backend/app/tasks/`.
- Do not call OpenAI directly from route handlers.
- Do not call OpenAI directly from frontend.
- Do not put business logic inside React components.
- Every LLM output must have a typed Pydantic schema.
- Every AI prompt must be versioned in code or a prompt registry module.
- Every interview question must record its category and provenance.
- Benchmark-driven questions must record the benchmark gap or risk area they test where supported.
- Every answer evaluation must include category scores and strict feedback.
- Benchmark-aware evaluations must include whether the answer addressed the benchmark gap being tested.
- Do not log raw resumes, transcripts, audio URLs, API keys, or prompts containing sensitive candidate data.

## Benchmark Rules

- Use curated/anonymized benchmark fixtures for the hackathon version.
- Do not scrape LinkedIn, Naukri, job boards, or personal websites in the initial version.
- Do not claim benchmark profiles are real hired-candidate resumes.
- Use safe wording: `benchmark profiles`, `curated top-candidate archetypes`, or `role benchmark corpus`.
- Benchmark comparison must produce structured outputs, not free text only.
- Benchmark gaps should feed question generation and final report generation.

## Coding Rules

### Backend

- Use type hints on public functions.
- Use `from __future__ import annotations` where useful.
- Use `loguru.logger`, not `print()`.
- Use SQLAlchemy models and Pydantic schemas.
- Use `tasks/_db.py:session_scope` from worker tasks when present.
- Register new RQ task kinds in `backend/app/api/jobs.py` when needed.
- Add models to `backend/app/models/__init__.py` or ensure `init_db()` imports them.

### Frontend

- Use strict TypeScript.
- Avoid `any` unless justified with a comment.
- Use a small `frontend/src/lib/api.ts` API client.
- Use focused page components and reusable UI components.
- Do not add heavy UI libraries unless a task explicitly asks.
- Prioritize the benchmark gap dashboard over decorative UI.

## Implementation Method

Work only from the current phase task file.

When implementing a task:

1. Read `docs/00-project-overview.md`.
2. Read `docs/01-architecture.md`.
3. Read `docs/08-implementation-sequence.md`.
4. Read `docs/13-benchmark-engine-design.md` for benchmark-related tasks.
5. Read the relevant task file in `tasks/`.
6. Implement only that task.
7. Add/update tests where practical.
8. Run the smallest relevant validation command.
9. Report changed files and remaining gaps.

## Quality Bar

A task is not complete if:

- It creates endpoints without schemas.
- It stores AI output as unstructured text when a typed schema is expected.
- It bypasses the job system for slow operations.
- It hardcodes OpenAI keys or model choices outside settings.
- It ignores MinIO for audio/file storage.
- It removes existing template functionality without reason.
- It generates generic interview questions when benchmark gaps are available.
- It adds scraping or unsupported claims about selected/hired resumes.
