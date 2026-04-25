# Task 022 — Question TTS Audio

## Goal

Generate human-like strict interviewer audio for each question using OpenAI TTS and store it in MinIO.

## Read First

- `docs/01-architecture.md`
- `docs/04-ai-audio-rag-design.md`
- `docs/06-api-contracts.md`

## Requirements

1. Add `backend/app/services/tts.py`.
2. Add `backend/app/tasks/generate_question_audio.py`.
3. Register `generate_question_audio` in `TASK_REGISTRY`.
4. Add `POST /questions/{question_id}/tts`.
5. Add `GET /questions/{question_id}/tts`.
6. Store generated audio in MinIO under:

```text
audio/questions/{question_id}.mp3
```

7. Store `tts_object_key` and `tts_status` on the question.

## Voice Style

Use this style instruction or equivalent:

```text
Speak like a strict but professional senior interviewer. Use a natural human-like delivery. Avoid cheerfulness, exaggerated emotion, and robotic pacing. Keep the tone calm, precise, and serious.
```

## Acceptance Criteria

- Calling POST creates a job and marks TTS as queued.
- Worker generates audio and stores object key.
- GET returns a presigned playable audio URL when generated.
- Failed TTS does not break the whole session.

## Out of Scope

- Realtime voice conversation.
- Custom voice cloning.
- ElevenLabs integration.
