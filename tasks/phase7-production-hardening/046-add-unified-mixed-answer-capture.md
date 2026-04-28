# Task: Add Unified Mixed Answer Capture

## Goal

Make `mixed_answer` questions submit one candidate answer containing the required modalities together.

## Current Issue

For `mixed_answer` questions, the production interview room currently renders separate spoken, written, and code capture panels. Each panel submits its own answer mode separately:

```txt
spoken_answer
written_answer
code_answer
```

A mixed question should instead produce one `candidate_answers` row with:

```txt
answer_mode=mixed_answer
audio/text/code/visual metadata as required by the question flags
```

## Scope

- Add a frontend `MixedAnswerCapture` component.
- For `response_mode=mixed_answer`, render `MixedAnswerCapture` instead of separate spoken/written/code capture panels.
- Use the existing `api.submitMixedAnswer` client.
- Support required modalities from question flags:
  - `requires_audio`
  - `requires_text`
  - `requires_code`
  - `requires_video`
- Collect audio only when audio is required.
- Collect text only when text is required.
- Collect code and code language only when code is required.
- Include safe visual-signal metadata mock/input only when `requires_video=true`.
- Show one Answer ID and one polling/evaluation result.

## Strict Limits

- Do not redesign the interview room.
- Do not request real camera access.
- Do not add video recording.
- Do not add code execution.
- Do not add emotion detection, personality scoring, truthfulness detection, or true-confidence detection.
- Do not change backend unless the existing mixed answer API has a clear bug.
- Do not add authentication, payments, recruiter dashboard, PDF export, or email export.

## Acceptance Criteria

- [ ] Mixed questions render one unified mixed answer panel.
- [ ] Mixed answer submission sends `answer_mode=mixed_answer`.
- [ ] Required audio/text/code fields are enforced in the frontend before submit.
- [ ] Visual signal metadata remains safe and mock/manual only.
- [ ] One mixed answer submission creates one Answer ID.
- [ ] One polling/evaluation result is shown for the mixed answer.
- [ ] Non-mixed spoken/written/code questions keep their existing capture components.
- [ ] Frontend build passes.

## Verification

Run:

```bash
npm.cmd --prefix frontend run build
```

If backend is touched, also run:

```bash
docker compose exec api pytest -q
```

Manual validation:

1. Start with `AI_MOCK_MODE=true`.
2. Prepare a fresh session.
3. Open the interview room.
4. Navigate to a `mixed_answer` question.
5. Confirm one mixed capture panel appears.
6. Record audio if required.
7. Fill text/code fields when required.
8. If visual metadata is required, confirm only safe mock/manual visual fields appear.
9. Submit once.
10. Confirm one Answer ID appears and processing/evaluation polling works.
