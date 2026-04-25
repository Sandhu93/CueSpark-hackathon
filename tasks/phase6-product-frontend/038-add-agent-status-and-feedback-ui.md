# Task: Add Agent Status and Feedback UI

## Goal

Show the candidate how their submitted answer is being processed by the multimodal evaluation pipeline.

This task makes agent processing transparent without exposing confusing internal implementation details.

## Scope

Implement only:

- Agent status panel for the interview room.
- Display available agent results from answer read API.
- Show status for relevant agents:
  - audio
  - text_answer
  - code_evaluation
  - video_signal
  - benchmark_gap
  - final_orchestrator
- Show final answer feedback once available.
- Show safe communication and visual signal labels.
- Add retry/refresh affordance if useful.

## Out of Scope

Do not implement:

- Backend changes.
- Agent execution logic.
- Report page.
- PDF export.
- Demo mock pages.
- Emotion/personality/true-confidence UI.

## Files Likely Involved

- `frontend/src/components/interview/AgentStatusPanel.tsx`
- `frontend/src/components/interview/AnswerFeedbackPanel.tsx`
- `frontend/src/app/session/[sessionId]/interview/page.tsx`
- `frontend/src/lib/types.ts`

## UI Requirements

Show a simple pipeline such as:

```txt
Answer uploaded
→ Audio agent
→ Benchmark gap agent
→ Final evaluation
```

For written/code answers, show relevant agents only.

Feedback sections should include:

- final answer score
- strict feedback
- strengths
- weaknesses
- benchmark gap summary
- communication summary if available
- code/text summary if available

## Safe Language Rules

Use:

```txt
communication signal
visual signal
face in frame
lighting quality
eye contact proxy
posture stability
```

Do not use:

```txt
emotion score
true confidence score
personality score
truthfulness score
```

## Acceptance Criteria

- [ ] Agent status panel renders from answer read API data.
- [ ] Only relevant/available agent results are shown.
- [ ] Final answer evaluation is shown when available.
- [ ] UI handles pending/running/failed/succeeded states.
- [ ] No unsupported claims appear.
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

- Keep the UI understandable to candidates.
- Avoid exposing raw JSON unless in a developer-only debug panel.
- This is production UI, not demo mock UI.
