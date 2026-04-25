# Task: Update Answer Upload for Multimodal Responses

## Goal

Extend candidate answer submission so a response can include audio, text, code, or mixed response data depending on the question's expected response mode.

This task should build on the existing candidate answer upload direction, but make it product-ready for multimodal evaluation.

## Scope

Implement only:

- Update or create answer submission endpoint to support multimodal payloads.
- Support audio upload for spoken and mixed answers.
- Support text answer submission for written and mixed answers.
- Support code answer submission for code and mixed answers.
- Store files in MinIO and structured response content in Postgres.
- Validate submitted fields against the question response mode.
- Return `answer_id` and processing status.

## Out of Scope

Do not implement:

- Audio transcription.
- Text analysis.
- Code analysis.
- Video signal analysis.
- Final scoring.
- Final report.
- Monaco editor UI.
- Real video upload.

## Files Likely Involved

- `backend/app/api/interview.py`
- `backend/app/api/audio.py` if audio endpoints are separated
- `backend/app/models/answer.py`
- `backend/app/schemas/answer.py`
- `backend/app/services/storage.py`
- `backend/tests/`

## API Direction

Prefer one flexible endpoint:

```txt
POST /api/questions/{question_id}/answers
```

Supported forms:

### Spoken answer

```txt
audio: file
answer_mode: spoken_answer
```

### Written answer

```json
{
  "answer_mode": "written_answer",
  "text_answer": "..."
}
```

### Code answer

```json
{
  "answer_mode": "code_answer",
  "code_answer": "...",
  "code_language": "python"
}
```

### Mixed answer

```txt
audio: file
answer_mode: mixed_answer
text_answer: optional
code_answer: optional
code_language: optional
```

Implementation can use separate JSON and multipart endpoints if the existing FastAPI structure makes that cleaner, but the API contract must remain easy for the frontend to consume.

## Validation Rules

- If question requires audio, audio must be present.
- If question requires text, text answer must be present.
- If question requires code, code answer and language must be present.
- Unknown question returns 404.
- Unsupported file type returns validation error.
- Do not store audio binary in Postgres.

## Acceptance Criteria

- [ ] Spoken answer upload still works.
- [ ] Written answer submission works.
- [ ] Code answer submission works.
- [ ] Mixed answer submission works where supported.
- [ ] Answer row stores response mode and relevant fields.
- [ ] Audio files are stored in MinIO when provided.
- [ ] Endpoint validates response mode requirements.
- [ ] No transcription, analysis, or evaluation is implemented in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual checks through API docs are acceptable.

## Notes for Codex

- Keep this endpoint focused on capture/storage only.
- Do not start agent evaluation here.
- The next tasks will process each modality separately.
