# Task: Add Benchmark Demo Frontend Slice

## Goal

Create a small frontend slice that makes the completed Phase 2 and Phase 2.5 backend work demoable before building the full interview, audio, evaluation, and report flow.

This task exists because the benchmark engine is the main novelty layer. Judges should be able to see the benchmark gap dashboard as soon as the benchmark backend is working.

## Scope

Implement only:

- Minimal frontend API client helpers needed for this slice.
- `/setup` page or update existing setup page.
- JD textarea.
- Resume paste input.
- Resume file upload input if upload backend already exists.
- Create session call.
- Resume upload call if available.
- Session preparation call.
- Poll/read session status.
- `/session/[sessionId]/match` page or section.
- `/session/[sessionId]/benchmark` page or section.
- Display benchmark comparison returned by `GET /api/sessions/{session_id}/benchmark`.
- Basic loading, pending, and error states.

## Out of Scope

Do not implement:

- Full interview page.
- TTS audio playback.
- Browser audio recording.
- Answer upload.
- Transcription UI.
- Answer evaluation UI.
- Final report UI.
- Authentication.
- Payments.
- Live scraping.
- Large UI redesign.

## Files Likely Involved

- `frontend/src/lib/api.ts`
- `frontend/src/lib/types.ts`
- `frontend/src/app/setup/page.tsx`
- `frontend/src/app/session/[sessionId]/match/page.tsx`
- `frontend/src/app/session/[sessionId]/benchmark/page.tsx`
- `frontend/src/components/`

## API Contract

Use existing or planned APIs:

- `POST /api/sessions`
- `POST /api/sessions/{session_id}/resume`
- `POST /api/sessions/{session_id}/prepare`
- `GET /api/sessions/{session_id}`
- `GET /api/sessions/{session_id}/benchmark`

## Data Model Changes

None.

## Benchmark Dashboard Must Show

At minimum:

- Benchmark similarity score.
- Resume competitiveness score.
- Evidence strength score.
- Missing skills.
- Weak skills.
- Missing metrics.
- Weak ownership signals.
- Interview risk areas.
- Recommended resume fixes.
- Question targets.

## Acceptance Criteria

- [ ] User can create a session from the frontend.
- [ ] User can provide JD and resume input.
- [ ] User can trigger preparation.
- [ ] Frontend can show preparation status.
- [ ] Frontend can show match score and role key when available.
- [ ] Frontend can fetch and display benchmark comparison.
- [ ] Benchmark dashboard clearly explains why this is not a generic AI mock interview.
- [ ] Loading and error states are handled.
- [ ] No interview/audio/report functionality is added.
- [ ] No unsupported claims about hired resumes, selected profiles, confidence detection, or emotion detection are shown.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Manual demo path:

```txt
setup -> prepare session -> match -> benchmark dashboard
```

## Notes for Codex

- This is a tactical demo slice, not full frontend implementation.
- Keep it simple and focused on the benchmark novelty.
- Reuse this work later when executing the full Phase 6 frontend tasks.
- Do not duplicate API helper logic if `frontend/src/lib/api.ts` already exists.
