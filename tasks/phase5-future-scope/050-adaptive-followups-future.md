# Task 050 — Adaptive Follow-Ups Future Scope

## Status

Future scope. Do not implement in the initial build unless explicitly requested.

## Future Goal

Generate adaptive follow-up questions when a candidate gives a weak, vague, or risky answer.

## Rule

Adaptive follow-ups should not replace the full planned interview. They should be inserted sparingly.

Recommended constraints:

```text
max_adaptive_followups_per_session = 2
trigger only when answer overall_score <= 5 or evidence_score <= 4
```

## Required Future Fields

Existing `interview_questions.source` already supports:

```text
base_plan
adaptive_followup
manual
```

No schema redesign should be needed.
