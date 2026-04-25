# Task: Add Turn-Based Interview Page

## Goal

Build the frontend page where the candidate hears one AI interviewer question at a time and records an answer.

## Scope

Implement only:

- `/session/[sessionId]/interview` page.
- Fetch question list.
- Display current question.
- Request/generate TTS audio for current question.
- Play interviewer audio.
- Use browser recording component.
- Upload answer audio.
- Fetch answer result after processing.
- Move to next question.

## Out of Scope

Do not implement:

- Final report page.
- Adaptive follow-up insertion.
- Realtime conversation.
- Video recording.
- Monaco editor.
- Code compiler.

## Files Likely Involved

- `frontend/src/app/session/[sessionId]/interview/page.tsx`
- `frontend/src/components/`
- `frontend/src/hooks/`
- `frontend/src/lib/api.ts`

## API Contract

Use:

- `GET /api/sessions/{session_id}/questions`
- `POST /api/questions/{question_id}/tts`
- `POST /api/questions/{question_id}/answers`
- `GET /api/answers/{answer_id}`

## Data Model Changes

None.

## Acceptance Criteria

- [ ] User can see one question at a time.
- [ ] User can play interviewer audio.
- [ ] User can record an answer.
- [ ] User can upload the answer.
- [ ] UI shows transcript/evaluation when available.
- [ ] User can move to the next question.
- [ ] Loading and error states are handled.
- [ ] No video or realtime conversation is implemented.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Manual browser verification is required.

## Notes for Codex

- Keep state local and simple.
- Do not introduce global state libraries unless explicitly needed.
