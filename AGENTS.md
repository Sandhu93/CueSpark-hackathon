# AGENTS.md — CueSpark Interview Coach

Instructions for AI coding agents working in this repository.

## Project Identity

This repository is being converted from a generic FastAPI + Next.js hackathon template into **CueSpark Interview Coach**: a turn-based AI mock interview platform for job seekers and experienced professionals switching roles.

The system must not become a generic chatbot, a coding-only interview tool, or a full video meeting clone. The first version is a single-session demo with strong backend foundations.

## Locked Product Scope

Build only this initial flow:

1. Candidate pastes a job description.
2. Candidate uploads or pastes a resume/CV.
3. Backend parses and stores the resume/JD.
4. Backend chunks and embeds JD/resume/rubric/question-bank data using Postgres + pgvector.
5. AI generates a JD-resume match analysis and a 10-question interview plan.
6. Interview is turn-based: one question at a time.
7. OpenAI TTS generates interviewer audio for each question on demand.
8. Candidate records an audio answer in the browser.
9. Backend stores candidate audio in MinIO.
10. Backend transcribes the answer.
11. Backend evaluates the answer using a strict interviewer rubric.
12. Backend generates a final report.

## Explicitly Out of Scope for Initial Version

Do not build these unless a task file explicitly asks for them:

- User accounts, login, organizations, teams, billing, subscriptions.
- Real-time WebRTC interview mode.
- Full Google Meet-like video call experience.
- Facial emotion detection or true confidence detection.
- Monaco editor or code execution.
- LinkedIn/Naukri/job-board scraping.
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
- Every answer evaluation must include category scores and strict feedback.
- Do not log raw resumes, transcripts, audio URLs, API keys, or prompts containing sensitive candidate data.

## Coding Rules

### Backend

- Use type hints on public functions.
- Use `from __future__ import annotations` where useful.
- Use `loguru.logger`, not `print()`.
- Use SQLAlchemy models and Pydantic schemas.
- Use `tasks/_db.py:session_scope` from worker tasks.
- Register new RQ task kinds in `backend/app/api/jobs.py`.
- Add models to `backend/app/models/__init__.py` or ensure `init_db()` imports them.

### Frontend

- Use strict TypeScript.
- Avoid `any` unless justified with a comment.
- Use a small `frontend/src/lib/api.ts` API client.
- Use focused page components and reusable UI components.
- Do not add heavy UI libraries unless a task explicitly asks.

## Implementation Method

Work only from the current phase task file.

When implementing a task:

1. Read `docs/00-project-overview.md`.
2. Read `docs/01-architecture.md`.
3. Read `docs/02-backend-design.md`.
4. Read the relevant task file in `tasks/`.
5. Implement only that task.
6. Add/update tests where practical.
7. Run the smallest relevant validation command.
8. Report changed files and remaining gaps.

## Quality Bar

A task is not complete if:

- It creates endpoints without schemas.
- It stores AI output as unstructured text when a typed schema is expected.
- It bypasses the job system for slow operations.
- It hardcodes OpenAI keys or model choices outside settings.
- It ignores MinIO for audio/file storage.
- It removes existing template functionality without reason.
