# Task: Add Benchmark Gap Dashboard Page

## Goal

Build the core novelty screen that shows how the candidate compares against curated role benchmark profiles before starting the interview.

This page should make the benchmark-driven value proposition obvious to judges within 10 seconds.

## Scope

Implement only:

- `/session/[sessionId]/benchmark` page.
- Fetch benchmark comparison for the session.
- Display benchmark similarity score.
- Display resume competitiveness score.
- Display evidence strength score.
- Display missing skills and weak skills.
- Display missing metrics and weak ownership signals.
- Display interview risk areas.
- Display recommended resume fixes.
- Display question targets generated from benchmark gaps.
- Add button to start the benchmark-driven interview.
- Basic loading, pending, empty, and error states.

## Out of Scope

Do not implement:

- Interview screen.
- Audio recording.
- Report page.
- Benchmark generation logic.
- Live scraping UI.
- Claims that benchmark profiles are verified hired-candidate resumes.
- Advanced charts requiring new heavy libraries.

## Files Likely Involved

- `frontend/src/app/session/[sessionId]/benchmark/page.tsx`
- `frontend/src/components/`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/types.ts`

## API Contract

Use:

- `GET /api/sessions/{session_id}`
- `GET /api/sessions/{session_id}/benchmark`

## Data Model Changes

None.

## Acceptance Criteria

- [ ] Benchmark page loads by session ID.
- [ ] Page displays benchmark similarity, resume competitiveness, and evidence strength scores.
- [ ] Page displays missing skills, weak skills, missing metrics, weak ownership signals, and interview risk areas.
- [ ] Page displays recommended resume fixes or clear empty state.
- [ ] Page displays question targets or interview strategy summary.
- [ ] Page uses safe wording: `benchmark profiles`, `role benchmark corpus`, or `curated top-candidate archetypes`.
- [ ] Page does not claim profiles are real selected/hired resumes.
- [ ] Page provides a clear CTA to start interview.
- [ ] Loading and error states are handled.
- [ ] No interview recording or report generation is implemented in this task.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Manual browser verification is required.

## Notes for Codex

- This is the most important hackathon novelty screen.
- Prioritize clarity over visual complexity.
- The page should explain why the generated interview will focus on specific gaps.
