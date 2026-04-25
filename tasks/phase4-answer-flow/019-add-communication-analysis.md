# Task: Add Communication Signal Analysis

## Goal

Compute simple, defensible communication metrics from the candidate transcript and audio metadata.

## Scope

Implement only:

- `communication_analysis.py` service.
- Word count.
- Estimated words per minute when duration is available.
- Filler word count.
- Basic hesitation marker count.
- Store metrics on `candidate_answers.communication_metrics` and related fields.

## Out of Scope

Do not implement:

- Emotion detection.
- True confidence detection.
- Personality detection.
- Video analysis.
- Answer evaluation.
- Final report.

## Files Likely Involved

- `backend/app/services/communication_analysis.py`
- `backend/app/tasks/`
- `backend/app/models/`
- `backend/tests/`

## API Contract

No new public endpoint is required in this task.

## Data Model Changes

Use existing candidate answer metrics fields.

## Acceptance Criteria

- [ ] Word count is computed.
- [ ] Filler word count is computed using a documented list.
- [ ] Words per minute is computed when duration exists.
- [ ] Communication metrics are stored in structured form.
- [ ] Service does not claim emotional or biometric inference.
- [ ] No LLM call is required in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Use `fixtures/sample_transcript.txt` for a simple test.

## Notes for Codex

- Use the term `communication signal`, not `true confidence`.
- Keep metrics deterministic and explainable.
