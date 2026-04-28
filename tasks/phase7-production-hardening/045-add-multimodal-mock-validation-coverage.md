# Task: Add Multimodal Mock Validation Coverage

## Goal

Make local/mock-mode validation cover all response modalities that CueSpark claims to support:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
optional visual signal metadata
```

The current product flow mostly exercises spoken answers because mock/generated questions default to `spoken_answer`. This makes it hard to validate written, code, mixed, and visual-signal paths through the production interview room.

## Why This Task Exists

CueSpark is a multimodal interview product, but manual local validation currently shows only the spoken-answer path in the interview room.

This task should make mock mode produce a representative interview plan so developers can test:

- audio recording and spoken answer submission
- written answer UI and text answer submission
- code answer UI and code answer submission
- mixed answer UI and mixed submission
- safe visual signal metadata handling where supported

This is product validation, not a demo-only mock page.

## Scope

Implement only minimal changes needed for mock/local validation:

- Update mock question generation so AI mock mode returns a mix of response modes.
- Ensure at least one question is `written_answer`.
- Ensure at least one question is `code_answer`.
- Ensure at least one question is `mixed_answer`.
- Optionally mark one mixed/spoken question with `requires_video=true` to test the visual signal placeholder/metadata path.
- Ensure generated/persisted questions store correct modality flags:
  - `requires_audio`
  - `requires_text`
  - `requires_code`
  - `requires_video`
- Ensure existing frontend renders the correct capture panels for these mock-mode questions.
- Add/update tests proving mock question generation contains multiple response modes.
- Add/update product-flow tests for written/code/mixed answer submission if reasonable.

## Out of Scope

Do not implement:

- Real video recording.
- Real camera access.
- Full WebRTC.
- Emotion detection.
- True confidence detection.
- Personality scoring.
- Sandboxed code execution.
- Monaco editor unless already present and trivial to enable.
- Major UI redesign.
- New backend agents beyond existing architecture.

## Files Likely Involved

- `backend/app/services/question_generator.py`
- `backend/app/schemas/question.py` only if needed
- `backend/tests/test_question_generator.py`
- `backend/tests/test_core_product_flow_api.py`
- `frontend/src/app/session/[sessionId]/interview/page.tsx` only if render logic has a small bug
- `frontend/src/components/interview/` only if existing components fail for mock-mode questions

## Suggested Mock Distribution

For AI mock mode, use a deterministic 10-question distribution such as:

```txt
1. spoken_answer       benchmark gap validation
2. spoken_answer       metrics/evidence validation
3. written_answer      structured case or stakeholder response
4. code_answer         coding / technical implementation prompt for software roles or generic pseudocode-style prompt in mock mode
5. mixed_answer        code/text + spoken explanation
6. spoken_answer       project ownership
7. spoken_answer       behavioral
8. written_answer      resume bullet rewrite or case response
9. spoken_answer       HR/motivation
10. mixed_answer       final summary with optional visual signal metadata
```

Keep the questions generic enough that the mock flow works for local validation.

## UI Clutter Note

This task may include only small UI fixes needed to test all modes. Do not redesign the interview room here.

If the page is too cluttered, create a separate follow-up task for interview room UX simplification.

## Acceptance Criteria

- [ ] Mock mode generates at least one spoken question.
- [ ] Mock mode generates at least one written question.
- [ ] Mock mode generates at least one code question.
- [ ] Mock mode generates at least one mixed question.
- [ ] Each mode has correct `requires_*` flags.
- [ ] Interview room renders the correct capture UI for each mode.
- [ ] Written/code/mixed submission can be tested locally in mock mode.
- [ ] Tests cover the mock question mode distribution.
- [ ] No unsafe visual/emotion/personality claims are added.
- [ ] No major UI redesign is included.

## Verification

Run:

```bash
docker compose exec api pytest backend/tests/test_question_generator.py -q
docker compose exec api pytest backend/tests/test_core_product_flow_api.py -q
docker compose exec api pytest -q
npm.cmd --prefix frontend run build
```

Manual browser validation:

1. Start a fresh session in `AI_MOCK_MODE=true`.
2. Prepare the session.
3. Open the interview room.
4. Confirm the 10 questions include spoken, written, code, and mixed modes.
5. Submit at least one answer for each mode.
6. Confirm answer status/agent feedback appears where supported.
7. Confirm report generation still works.

## Notes for Codex

- This is a validation coverage task.
- Keep changes deterministic in mock mode.
- Do not fake production claims.
- Do not add new major features.
