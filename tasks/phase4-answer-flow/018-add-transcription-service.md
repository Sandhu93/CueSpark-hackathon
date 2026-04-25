# Task: Add Transcription Service

## Goal

Transcribe uploaded candidate answer audio and store the transcript on the answer record.

## Scope

Implement only:

- `transcription.py` service.
- Mock transcription when `AI_MOCK_MODE=true`.
- Real OpenAI transcription call through centralized OpenAI client if implemented.
- Worker task for transcribing an answer.
- Update `candidate_answers.transcript`.

## Out of Scope

Do not implement:

- Answer evaluation.
- Final report.
- Realtime transcription.
- Speaker diarization.
- Video analysis.

## Files Likely Involved

- `backend/app/services/transcription.py`
- `backend/app/services/openai_client.py`
- `backend/app/tasks/transcribe_answer.py`
- `backend/app/api/jobs.py`
- `backend/app/models/`
- `backend/tests/`

## API Contract

No new public endpoint is required unless the job system needs one.

## Data Model Changes

Use existing `candidate_answers.transcript`.

## Acceptance Criteria

- [ ] Mock mode produces deterministic transcript text.
- [ ] Real mode uses configured transcription model.
- [ ] Worker task reads audio object from MinIO.
- [ ] Worker task stores transcript on answer record.
- [ ] Failed transcription is logged safely and does not expose sensitive data.
- [ ] No answer evaluation is added in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can use uploaded sample audio or mock mode.

## Notes for Codex

- Do not log raw transcript unless explicitly needed in tests.
- Keep transcription service separate from evaluation service.
