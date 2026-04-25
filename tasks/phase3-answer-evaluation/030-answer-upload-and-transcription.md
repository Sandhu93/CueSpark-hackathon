# Task 030 — Answer Upload and Transcription

## Goal

Allow candidate answer audio upload, then transcribe it using OpenAI transcription.

## Read First

- `docs/02-backend-design.md`
- `docs/04-ai-audio-rag-design.md`
- `docs/06-api-contracts.md`

## Requirements

1. Add `backend/app/api/interview.py` or appropriate question/answer router.
2. Add `POST /questions/{question_id}/answers`.
3. Store answer audio in MinIO under:

```text
audio/answers/{answer_id}.webm
```

4. Create `candidate_answers` row.
5. Add `backend/app/services/transcription.py`.
6. Add `backend/app/tasks/transcribe_answer.py`.
7. Register `transcribe_answer` in `TASK_REGISTRY`.
8. Transcription result should update:
   - `transcript`
   - `transcription_status`
   - `word_count`
   - optional duration fields if available

## Input Options

Support at least one:

- multipart file upload through API
- JSON object key after presigned upload

For speed, multipart is acceptable first.

## Acceptance Criteria

- Candidate answer audio is stored.
- Answer row is created.
- Transcription job is queued.
- Transcript is saved after job completes.
- `GET /answers/{answer_id}` returns answer and transcript status.

## Out of Scope

- Answer evaluation.
- Video analysis.
- Emotion analysis.
