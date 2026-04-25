# Task: Add Setup and Match Pages

## Goal

Build the frontend pages for entering the job description, providing the resume, creating a session, preparing it, and showing the match summary.

## Scope

Implement only:

- `/setup` page.
- JD textarea.
- Resume paste input.
- Resume file upload input.
- Session creation call.
- Session preparation trigger.
- `/session/[sessionId]/match` page.
- Basic loading and error states.

## Out of Scope

Do not implement:

- Interview screen.
- Audio recording.
- Report page.
- Authentication.
- Payments.
- Advanced UI redesign.

## Files Likely Involved

- `frontend/src/app/setup/page.tsx`
- `frontend/src/app/session/[sessionId]/match/page.tsx`
- `frontend/src/components/`
- `frontend/src/lib/api.ts`

## API Contract

Use:

- `POST /api/sessions`
- `POST /api/sessions/{session_id}/resume`
- `POST /api/sessions/{session_id}/prepare`
- `GET /api/sessions/{session_id}`

## Data Model Changes

None.

## Acceptance Criteria

- [ ] User can paste a JD.
- [ ] User can paste resume text.
- [ ] User can upload a resume file.
- [ ] User can create a session.
- [ ] User can trigger session preparation.
- [ ] Match page displays session status and match score when available.
- [ ] UI handles loading and error states.
- [ ] No interview UI is implemented in this task.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Manual verification through browser is recommended.

## Notes for Codex

- Keep UI clean but do not spend time on heavy design polish.
- Use existing styling conventions.
