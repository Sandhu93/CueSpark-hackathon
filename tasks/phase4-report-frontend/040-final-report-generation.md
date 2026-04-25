# Task 040 — Final Report Generation

## Goal

Generate a strict final interview report from match analysis, questions, transcripts, and answer evaluations.

## Read First

- `docs/00-project-overview.md`
- `docs/04-ai-audio-rag-design.md`
- `docs/06-api-contracts.md`

## Requirements

1. Add `backend/app/services/report_generator.py`.
2. Add `backend/app/tasks/generate_report.py`.
3. Register `generate_report` in `TASK_REGISTRY`.
4. Add `POST /sessions/{session_id}/report`.
5. Add `GET /sessions/{session_id}/report`.
6. Save report in `interview_reports`.

## Report Sections

Final report must include:

1. Overall readiness score.
2. Hiring recommendation.
3. JD-resume match summary.
4. Interview performance summary.
5. Answer-by-answer feedback.
6. Skill gaps.
7. Resume improvement suggestions.
8. Preparation plan.

## Hiring Recommendation Enum

Use:

```text
strong_yes
yes
maybe
no
strong_no
```

## Acceptance Criteria

- Report generation works after at least one evaluated answer.
- Report improves as more evaluated answers exist.
- Report is strict and actionable.
- Report endpoint returns structured JSON.

## Out of Scope

- PDF export.
- Email report.
- User account history.
