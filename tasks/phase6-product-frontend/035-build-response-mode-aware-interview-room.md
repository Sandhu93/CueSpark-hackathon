# Task: Build Response-Mode-Aware Interview Room

## Goal

Build the production interview room page that can render the correct answer-capture UI based on each question's `response_mode` and required modality flags.

This task should create the main interview room structure. It should not fully implement every capture component yet.

## Scope

Implement only:

- `/session/[sessionId]/interview` route if it does not already exist.
- Question loading using the frontend API client.
- Current question display.
- Question category, difficulty, expected signal.
- `why_this_was_asked` panel.
- Benchmark gap reference chips.
- TTS audio play/generate controls using the API client.
- Response-mode indicator.
- Conditional placeholders/components for:
  - spoken answer
  - written answer
  - code answer
  - mixed answer
- Basic previous/next/current-question navigation if available.
- Clear processing/status areas for answer submission and evaluation.

## Out of Scope

Do not implement:

- Full audio recording logic.
- Monaco editor integration.
- Full report page.
- Backend changes.
- Real video capture.
- Evaluation logic.
- Demo mock UI.

## Files Likely Involved

- `frontend/src/app/session/[sessionId]/interview/page.tsx`
- `frontend/src/components/interview/`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/types.ts`

## UI Requirements

The page should show:

1. Header:
   - session/interview progress
   - current question number
   - response mode

2. Question panel:
   - question text
   - category
   - difficulty
   - expected signal
   - why this was asked
   - benchmark gap references

3. AI interviewer voice panel:
   - play TTS audio if available
   - generate TTS if missing
   - loading/error states

4. Response capture area:
   - spoken answer component placeholder
   - written answer component placeholder
   - code answer component placeholder
   - mixed answer layout when multiple modalities are required

5. Evaluation status area:
   - submitted
   - processing
   - running agents
   - evaluated
   - failed

## Acceptance Criteria

- [ ] Interview room route exists.
- [ ] Questions are fetched using API client.
- [ ] TTS audio can be requested/played using API client.
- [ ] UI changes based on `response_mode`.
- [ ] `why_this_was_asked` and benchmark gap refs are visible.
- [ ] No backend files are modified.
- [ ] No fake demo-data route is used.
- [ ] Build succeeds.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- This is the production interview route, not `/demo/interview`.
- Keep the page modular; capture components will be expanded in later tasks.
- Use safe labels: benchmark gap, expected signal, response mode.
