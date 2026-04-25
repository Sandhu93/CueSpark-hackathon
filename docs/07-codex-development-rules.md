# 07 — Codex Development Rules

Use this file as the implementation control document.

## Golden Rule

Implement only the current task file. Do not add adjacent features just because they seem useful.

## Product Constraints

The app is:

- Turn-based.
- Single-session.
- Strict interviewer style.
- Role-agnostic.
- Audio-enabled.
- Postgres + pgvector backed.

The app is not:

- A generic chatbot.
- A recruiter ATS.
- A video conferencing app.
- A coding challenge platform.
- A resume builder.
- A production multi-tenant SaaS yet.

## Before Writing Code

Read:

1. `AGENTS.md`
2. `docs/00-project-overview.md`
3. `docs/01-architecture.md`
4. The current task file

Then summarize the files you will change.

## Backend Rules

- Add schemas before routes.
- Add models before task persistence.
- Keep routes thin.
- Keep AI calls inside services.
- Long-running operations must be tasks.
- Do not block API responses waiting for transcription/evaluation.
- Do not log sensitive raw data.

## Frontend Rules

- Keep one API client file.
- Keep interview state explicit.
- Use typed API responses.
- Do not build authentication.
- Do not add global state libraries unless needed.
- Do not build dashboards outside the requested flow.

## AI Rules

- No untyped AI JSON parsing.
- Use Pydantic schemas for AI outputs.
- Store prompt version.
- Store question provenance.
- Separate transcription from evaluation.
- Evaluation must be strict and actionable.

## Database Rules

- Use pgvector for embeddings.
- Store audio/document files in MinIO, not Postgres.
- Store text, scores, and metadata in Postgres.
- Use JSONB for flexible AI metadata.
- Keep schema simple for v1.

## Testing Expectations

At minimum, add or update tests for:

- Health endpoint remains working.
- Session creation.
- Question listing once generated or seeded.
- Pure services where practical.

Do not block the full build on exhaustive test coverage, but avoid untested critical transformations.

## Definition of Done for a Task

A task is done only when:

- Relevant docs are followed.
- Code compiles/imports.
- New models/schemas/routes are wired.
- Job kinds are registered if needed.
- Basic tests or manual verification notes are provided.
- No out-of-scope feature was added.
