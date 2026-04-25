# Task: Add Match Analysis Service

## Goal

Generate a structured JD-resume match analysis for an interview session.

This task must also infer a normalized `role_key` that later benchmark retrieval can use.

## Scope

Implement only:

- Match analysis Pydantic output schema.
- `match_analyzer.py` service.
- Mock match analysis when `AI_MOCK_MODE=true`.
- Optional real LLM call through centralized OpenAI client if available.
- Store match score and structured metadata on the session or related record.
- Infer/store `role_title`, `seniority_level`, and `role_key` where supported by the data model.

## Out of Scope

Do not implement:

- Benchmark profile retrieval.
- Benchmark comparison.
- Question generation.
- TTS.
- Transcription.
- Final report generation.
- Frontend match page unless explicitly requested by another task.

## Files Likely Involved

- `backend/app/services/match_analyzer.py`
- `backend/app/services/prompts.py`
- `backend/app/schemas/`
- `backend/app/models/`
- `backend/app/tasks/`

## API Contract

No new public endpoint is required unless needed by the existing preparation job.

## Data Model Changes

Use existing session fields and metadata fields if available. Do not create unnecessary new tables.

## Required Output Fields

Match analysis should include:

- role title
- normalized role key, for example `project_manager`, `backend_developer`, or `data_analyst`
- seniority level
- match score
- matched skills
- missing skills
- risk areas
- interview focus areas

## Acceptance Criteria

- [ ] Match analysis returns structured JSON/Pydantic output.
- [ ] Output includes role title, normalized role key, seniority, match score, matched skills, missing skills, risk areas, and interview focus areas.
- [ ] Mock mode works without OpenAI API key.
- [ ] Real mode, if added, uses prompt registry and centralized OpenAI client.
- [ ] Session match score is updated.
- [ ] Session role key is updated if the field exists.
- [ ] No benchmark retrieval or comparison is implemented.
- [ ] No questions are generated in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification can use fixture JD and resume.

## Notes for Codex

- Keep the tone strict and interviewer-like.
- Do not make unsupported hiring/legal claims.
- The `role_key` is important because benchmark retrieval depends on it in the next phase.
