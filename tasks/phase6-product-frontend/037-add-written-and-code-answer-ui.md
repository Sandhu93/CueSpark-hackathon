# Task: Add Written and Code Answer UI

## Goal

Add production UI components for written-answer and code-answer response modes inside the interview room.

This enables CueSpark to support non-spoken tasks such as case answers, pseudocode, stakeholder communication, and coding interview questions.

## Scope

Implement only:

- Written answer capture component.
- Code answer capture component.
- Language selector for code answers.
- Optional explanation textarea for code answers if supported by API types.
- Submission through frontend API client.
- Display processing/evaluation status after submission.
- Integrate components into `/session/[sessionId]/interview` based on `response_mode` and modality flags.

## Out of Scope

Do not implement:

- Monaco editor unless already installed and simple to use.
- Code execution.
- Online judge.
- Backend changes.
- Real video capture.
- Report page.
- Text/code evaluation logic.

## Files Likely Involved

- `frontend/src/components/interview/WrittenAnswerCapture.tsx`
- `frontend/src/components/interview/CodeAnswerCapture.tsx`
- `frontend/src/app/session/[sessionId]/interview/page.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/types.ts`

## UI Requirements

### Written Answer

Show:

- question reminder
- textarea/editor
- character/word count if simple
- submit button
- processing status
- feedback when available

### Code Answer

Show:

- code textarea or lightweight code editor
- language selector
- optional explanation textarea
- submit button
- processing status
- code-quality feedback when available

### Mixed Answer

If question mode is `mixed_answer`, show the relevant combination of:

- spoken answer capture
- written answer capture
- code answer capture

## Acceptance Criteria

- [ ] Written answer UI works for `written_answer` questions.
- [ ] Code answer UI works for `code_answer` questions.
- [ ] Mixed answer UI can render text/code capture where required.
- [ ] Submissions use production API client.
- [ ] No code execution is implemented.
- [ ] No backend files are modified.
- [ ] Build succeeds.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- Keep it simple first. Monaco can be added later.
- Code evaluation is static backend analysis, not local execution.
- Do not add fake evaluation results in the production UI.
