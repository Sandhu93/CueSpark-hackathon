# Task 042 — Frontend Interview Room

## Goal

Build the turn-based interview room UI with question audio playback and candidate answer recording.

## Read First

- `docs/05-frontend-flow.md`
- `docs/06-api-contracts.md`

## Requirements

1. Create `/session/[sessionId]/interview` page.
2. Fetch questions for the session.
3. Show one question at a time.
4. Generate/fetch TTS audio for the current question.
5. Play interviewer audio.
6. Record candidate audio using browser MediaRecorder.
7. Allow retry before submit.
8. Submit audio answer.
9. Poll transcription/evaluation status.
10. Show transcript and strict feedback once available.
11. Move to next question.

## Required UI States

```text
loading_question
ready_to_play
playing_question
ready_to_record
recording
recorded_not_submitted
uploading
transcribing
evaluating
evaluated
failed
```

## Acceptance Criteria

- User can complete at least one full question-answer-evaluation cycle.
- Audio player works for generated TTS.
- MediaRecorder records and submits audio.
- Transcript and feedback are visible.
- No future questions are shown upfront.

## Out of Scope

- Realtime conversation.
- Video recording.
- Monaco editor.
