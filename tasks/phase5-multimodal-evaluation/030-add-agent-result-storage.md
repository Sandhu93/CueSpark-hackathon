# Task: Add Agent Result Storage

## Goal

Add a durable storage layer for modality-agent outputs so audio, video, text, code, and benchmark-gap analysis can be combined later by the final evaluation orchestrator.

This task creates shared storage for agent outputs. It must not implement final scoring or report generation.

## Scope

Implement only:

- `agent_results` model or equivalent reusable storage structure.
- Pydantic schemas for agent result create/read.
- Fields to link agent results to `candidate_answers`.
- Fields to identify agent type and status.
- JSONB payload for structured agent output.
- Model imports for database initialization.

## Out of Scope

Do not implement:

- Audio transcription.
- Text analysis.
- Code analysis.
- Video analysis.
- Final scoring.
- Final report.
- Frontend UI.

## Files Likely Involved

- `backend/app/models/agent_result.py`
- `backend/app/schemas/agent_results.py`
- `backend/app/models/__init__.py`
- `backend/tests/`

## Data Model Guidance

Recommended table:

## `agent_results`

Fields:

```txt
id
answer_id
agent_type: audio | video_signal | text_answer | code_evaluation | benchmark_gap | final_orchestrator
status: pending | running | succeeded | failed
score
payload
error
created_at
updated_at
```

`payload` should store the typed output from each agent as JSONB.

## Acceptance Criteria

- [ ] `agent_results` model exists.
- [ ] Agent result links to candidate answer.
- [ ] Agent type enum/schema exists.
- [ ] Status enum/schema exists.
- [ ] JSONB payload field exists.
- [ ] Existing answer/evaluation models are not broken.
- [ ] No agent analysis or final scoring is implemented.

## Verification

Run:

```bash
pytest backend/tests
```

## Notes for Codex

- This table allows agents to run independently and be combined later.
- Keep payload flexible but typed at service/schema boundaries.
