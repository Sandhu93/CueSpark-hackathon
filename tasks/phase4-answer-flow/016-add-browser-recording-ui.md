# Task: Add Browser Audio Recording UI

## Goal

Add a frontend component that records candidate answers from the browser microphone during the turn-based interview.

## Scope

Implement only:

- Audio recording component using browser APIs.
- Start/stop recording controls.
- Display basic recording state.
- Produce an audio blob suitable for upload.
- Graceful handling when microphone permission is denied.

## Out of Scope

Do not implement:

- Full interview screen polish.
- Answer upload endpoint.
- Transcription.
- Evaluation.
- Realtime WebRTC conversation.
- Video recording.

## Files Likely Involved

- `frontend/src/components/`
- `frontend/src/hooks/`
- `frontend/src/lib/`

## API Contract

No new backend endpoint is required in this task.

## Data Model Changes

None.

## Acceptance Criteria

- [ ] User can start recording.
- [ ] User can stop recording.
- [ ] Component exposes the recorded audio blob to parent code.
- [ ] UI shows recording state.
- [ ] Microphone permission failure is handled clearly.
- [ ] No backend changes are made unless strictly necessary.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- Use TypeScript types; avoid `any`.
- Keep the component reusable.
- Do not add heavy recording libraries unless necessary.
