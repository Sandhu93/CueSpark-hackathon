# Task: Add Product Polish, Error States, and Retry States

## Goal

Add production-grade polish across the real CueSpark frontend flow so the product is usable beyond a hackathon demo.

This task should improve reliability, clarity, and trust without adding new product scope.

## Scope

Implement only frontend polish for the real app routes:

- `/setup`
- `/session/[sessionId]/match`
- `/session/[sessionId]/benchmark`
- `/session/[sessionId]/interview`
- `/session/[sessionId]/report`

Add or improve:

- loading states
- empty states
- error states
- retry buttons
- disabled states
- progress indicators
- safe explanatory copy
- consistent navigation between session pages
- clear distinction between unavailable data and failed processing

## Out of Scope

Do not implement:

- Backend changes.
- New API endpoints.
- Authentication.
- Payments.
- Recruiter dashboard.
- PDF/email export.
- Demo mock UI changes.
- New AI features.

## Files Likely Involved

- `frontend/src/app/setup/page.tsx`
- `frontend/src/app/session/[sessionId]/match/page.tsx`
- `frontend/src/app/session/[sessionId]/benchmark/page.tsx`
- `frontend/src/app/session/[sessionId]/interview/page.tsx`
- `frontend/src/app/session/[sessionId]/report/page.tsx`
- `frontend/src/components/`
- `frontend/src/lib/api.ts`

## UX Requirements

The frontend should clearly handle:

```txt
preparing session
benchmark unavailable
questions unavailable
TTS generation failed
answer upload failed
agent processing pending
agent processing failed
report not generated
report generation failed
```

Use action-oriented language:

```txt
Retry preparation
Retry TTS
Retry upload
Refresh status
Generate report
Back to benchmark dashboard
Continue interview
```

## Safety Copy Requirements

Where visual or communication signals appear, include safe wording:

```txt
Observable communication and visual presence signals only. CueSpark does not detect emotion, personality, truthfulness, or true confidence.
```

Where readiness recommendation appears, include:

```txt
This is preparation guidance, not a hiring guarantee.
```

## Acceptance Criteria

- [ ] Main real product routes have loading states.
- [ ] Main real product routes have actionable error states.
- [ ] Retry/refresh behavior exists where useful.
- [ ] Navigation between match, benchmark, interview, and report is clear.
- [ ] Safety copy appears where modality signals or recommendations are shown.
- [ ] No backend files are modified.
- [ ] Build succeeds.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

Manual:

1. Test with missing/invalid session ID.
2. Test with session preparing.
3. Test with benchmark missing.
4. Test with no report generated.
5. Test with failed answer/report status if fixtures or API responses allow.

## Notes for Codex

- Do not redesign the entire app.
- Improve reliability and clarity.
- Keep the app serious and product-grade.
