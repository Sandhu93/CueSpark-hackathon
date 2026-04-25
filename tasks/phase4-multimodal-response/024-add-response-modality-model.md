# Task: Add Response Modality Model

## Goal

Extend the interview question and answer model so CueSpark can support multiple response modes:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
```

This task prepares the data model for multimodal interview evaluation. It must not implement recording, transcription, text analysis, code analysis, or video analysis.

## Scope

Implement only:

- Add response modality fields to question and/or answer models.
- Add schemas/enums for response mode.
- Add fields needed to store written answers and code answers later.
- Keep backward compatibility with existing spoken-answer flow.
- Update generated question schema if needed so questions can declare expected response mode.

## Out of Scope

Do not implement:

- Audio recording
- Transcription
- Video analysis
- Text evaluation
- Code evaluation
- Monaco editor
- Final evaluation orchestrator
- Report generation

## Files Likely Involved

- `backend/app/models/question.py`
- `backend/app/models/answer.py`
- `backend/app/schemas/question.py`
- `backend/app/schemas/answer.py`
- `backend/app/services/question_generator.py` only if default response mode is needed
- `backend/tests/`

## Data Model Guidance

Recommended question fields:

```txt
response_mode: spoken_answer | written_answer | code_answer | mixed_answer
requires_audio: boolean
requires_video: boolean
requires_text: boolean
requires_code: boolean
```

Recommended answer fields:

```txt
text_answer: text nullable
code_answer: text nullable
code_language: string nullable
answer_mode: spoken_answer | written_answer | code_answer | mixed_answer
```

Default behavior:

```txt
response_mode = spoken_answer
requires_audio = true
requires_video = false for production MVP unless explicitly enabled
requires_text = false
requires_code = false
```

## Acceptance Criteria

- [ ] Response mode enum/schema exists.
- [ ] Questions can define expected response mode.
- [ ] Answers can store spoken, written, code, or mixed response metadata.
- [ ] Existing spoken-answer question generation still works.
- [ ] Existing tests still pass.
- [ ] No new evaluation logic is added.

## Verification

Run:

```bash
pytest backend/tests
```

## Notes for Codex

- Keep this as a data-model foundation task.
- Do not attempt to implement agents here.
- Use `spoken_answer` as the default mode to avoid breaking existing flow.
