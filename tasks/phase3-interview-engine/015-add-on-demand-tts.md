# Task: Add On-Demand Interviewer TTS

## Goal

Generate interviewer voice audio for a question only when the candidate reaches that question.

## Scope

Implement only:

- `tts.py` service.
- Mock TTS behavior when `AI_MOCK_MODE=true`.
- Real OpenAI TTS call through centralized OpenAI client if implemented.
- Store generated audio in MinIO.
- Save question `tts_object_key`.
- `POST /api/questions/{question_id}/tts` endpoint.

## Out of Scope

Do not implement:

- Candidate audio recording.
- Transcription.
- Answer evaluation.
- Realtime voice conversation.
- Voice cloning.

## Files Likely Involved

- `backend/app/api/audio.py`
- `backend/app/services/tts.py`
- `backend/app/services/openai_client.py`
- `backend/app/services/storage.py`
- `backend/app/models/`
- `backend/app/schemas/`

## API Contract

Follow `docs/09-api-contracts-detailed.md`.

## Data Model Changes

Use existing `interview_questions.tts_object_key`.

## Acceptance Criteria

- [ ] Endpoint generates or retrieves interviewer audio for one question.
- [ ] TTS audio is stored in MinIO.
- [ ] Question row stores `tts_object_key`.
- [ ] Mock mode works without OpenAI API key.
- [ ] Real mode uses configured TTS model and voice settings.
- [ ] Repeated calls should not regenerate audio unnecessarily if already available.
- [ ] No candidate transcription or evaluation is added.

## Verification

Run:

```bash
pytest backend/tests
```

Manual:

```bash
curl -X POST http://localhost:8000/api/questions/{question_id}/tts
```

## Notes for Codex

- Use a professional, strict interviewer tone.
- Do not expose permanent object storage credentials.
