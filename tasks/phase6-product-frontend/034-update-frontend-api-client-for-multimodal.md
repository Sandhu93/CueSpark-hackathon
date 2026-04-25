# Task: Update Frontend API Client for Multimodal Product Flow

## Goal

Update the frontend API client and shared frontend types so the production UI can consume the benchmark, question, multimodal answer, agent-result, evaluation, and report APIs.

This is the first Phase 6 task. It prepares frontend integration without building the full UI screens yet.

## Scope

Implement only:

- Update `frontend/src/lib/api.ts` or equivalent API client.
- Add/extend frontend TypeScript types for:
  - sessions
  - benchmark comparisons
  - questions
  - response modes
  - candidate answers
  - agent results
  - answer evaluations
  - multimodal reports
- Add API helpers for:
  - list questions
  - generate/get TTS audio
  - submit spoken answer
  - submit written answer
  - submit code answer
  - submit mixed answer
  - get answer details
  - generate report
  - get report
- Keep existing setup/match/benchmark API helpers working.

## Out of Scope

Do not implement:

- Interview page UI.
- Audio recording UI.
- Text/code editor UI.
- Report page UI.
- Backend APIs.
- Real camera/video capture.
- Mock demo pages.

## Files Likely Involved

- `frontend/src/lib/api.ts`
- `frontend/src/lib/types.ts`
- `frontend/src/lib/api-types.ts` if the project already separates types
- `frontend/src/lib/demo/` should not be modified unless only type reuse is needed

## Required Types

Add response modes:

```ts
export type ResponseMode = "spoken_answer" | "written_answer" | "code_answer" | "mixed_answer";
```

Add agent result types:

```ts
export type AgentType =
  | "audio"
  | "video_signal"
  | "text_answer"
  | "code_evaluation"
  | "benchmark_gap"
  | "final_orchestrator";
```

Add answer/evaluation/report types aligned with:

```txt
docs/09-api-contracts-detailed.md
docs/10-data-model-contract.md
```

## Acceptance Criteria

- [ ] Frontend API client supports current setup/match/benchmark flow.
- [ ] Frontend API client supports multimodal question and answer contracts.
- [ ] Frontend API client supports final report contracts.
- [ ] No page UI is implemented in this task.
- [ ] No backend files are modified.
- [ ] TypeScript build succeeds.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- Keep the API client thin and typed.
- Do not scatter `fetch()` calls inside future pages.
- Use `NEXT_PUBLIC_API_URL` consistently.
- Do not add fake API responses in the production API client.
