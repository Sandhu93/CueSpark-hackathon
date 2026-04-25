# Task 041 — Frontend Setup and Match Pages

## Goal

Build the initial frontend flow for creating a session and viewing match/interview readiness.

## Read First

- `docs/05-frontend-flow.md`
- `docs/06-api-contracts.md`
- `docs/07-codex-development-rules.md`

## Requirements

1. Update `frontend/src/lib/api.ts` with typed session/question/report calls.
2. Create `/setup` page.
3. Support JD paste textarea.
4. Support resume paste fallback.
5. Support resume file upload using existing upload/direct upload flow.
6. Create session and trigger preparation.
7. Poll job/session status.
8. Create `/session/[sessionId]/match` page.
9. Show:
   - match score
   - role title/domain if available
   - strengths/gaps if available
   - button to start interview

## Acceptance Criteria

- User can create a session from UI.
- User can paste JD and resume.
- User can upload resume.
- User sees preparation progress.
- User lands on match summary when session is ready.

## Out of Scope

- Recording audio.
- Playing TTS.
- Report UI.
- Authentication.
