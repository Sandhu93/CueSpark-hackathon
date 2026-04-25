# Task: Add Spoken Answer Recording Flow

## Goal

Implement the production spoken-answer capture flow inside the response-mode-aware interview room.

This task handles browser microphone recording, candidate retry, answer upload, and polling/reading processing status.

## Scope

Implement only:

- Reusable audio recording hook/component using browser MediaRecorder.
- Spoken answer capture UI.
- Start/stop/retry recording controls.
- Recording timer and basic waveform/progress indicator if simple.
- Microphone permission error handling.
- Submit recorded answer through the API client.
- Poll or refresh answer details after submission.
- Show transcript, communication metrics, agent results, and final evaluation when available.

## Out of Scope

Do not implement:

- Written answer UI.
- Code answer UI.
- Real video capture.
- Backend changes.
- New transcription/evaluation logic.
- Report page.
- WebRTC conversation.

## Files Likely Involved

- `frontend/src/components/interview/SpokenAnswerCapture.tsx`
- `frontend/src/hooks/useAudioRecorder.ts`
- `frontend/src/app/session/[sessionId]/interview/page.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/types.ts`

## UI States

Support:

```txt
idle
recording
recorded_not_submitted
uploading
processing
transcribing
running_agents
evaluated
failed
```

## Acceptance Criteria

- [ ] User can start recording.
- [ ] User can stop recording.
- [ ] User can retry before submitting.
- [ ] User can submit the spoken answer.
- [ ] Audio answer upload uses the production API client.
- [ ] UI handles microphone permission denial.
- [ ] UI shows transcript and communication metrics when available.
- [ ] UI shows final feedback when available.
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

1. Open `/session/{sessionId}/interview`.
2. Select/current question with `spoken_answer`.
3. Record audio.
4. Retry once.
5. Submit answer.
6. Confirm answer status is displayed.

## Notes for Codex

- Use browser APIs directly unless the project already has a recorder utility.
- Keep the component reusable for `mixed_answer` later.
- Do not claim emotion or true-confidence detection in the UI.
