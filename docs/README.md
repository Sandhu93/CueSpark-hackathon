# CueSpark Interview Coach Documentation

This folder defines the controlled implementation plan for CueSpark Interview Coach.

Use these docs to prevent scope creep while converting the existing FastAPI + Next.js hackathon template into a strong mock interview product foundation.

## Read Order

1. `docs/00-project-overview.md`
2. `docs/01-architecture.md`
3. `docs/02-backend-design.md`
4. `docs/03-database-design.md`
5. `docs/04-ai-audio-rag-design.md`
6. `docs/05-frontend-flow.md`
7. `docs/06-api-contracts.md`
8. `docs/07-codex-development-rules.md`
9. Relevant file from `tasks/`

## Product Rule

The first version must be a **turn-based strict mock interviewer** for any job role. It should not become a generic chat app, video meeting clone, or coding-only interview platform.

## Current Implementation Target

Single-session demo:

```text
JD + Resume
  -> parse
  -> chunk + embed
  -> match analysis
  -> 10-question plan
  -> turn-based voice interview
  -> transcription
  -> strict evaluation
  -> final report
```
