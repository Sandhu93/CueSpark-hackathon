# Deprecated Task: Final Report Generation

## Status

Deprecated for the current product roadmap.

This older report-generation task has been superseded by the multimodal evaluation and product frontend phases:

```txt
tasks/phase5-multimodal-evaluation/033-add-multimodal-readiness-report.md
tasks/phase6-product-frontend/039-add-multimodal-readiness-report-page.md
```

## Why This Is Deprecated

The old task generates a strict final interview report from match analysis, questions, transcripts, and answer evaluations.

The current product report must be multimodal and benchmark-aware. It should aggregate:

- benchmark comparison
- benchmark gap coverage
- audio communication results
- written answer results if available
- code evaluation results if available
- safe visual signal summaries if available
- final orchestrator answer evaluations
- resume improvement suggestions
- preparation plan

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use the active Phase 5 and Phase 6 tasks instead.

## Historical Scope

The original intent was:

- add `backend/app/services/report_generator.py`
- add `backend/app/tasks/generate_report.py`
- add report endpoints
- save report in `interview_reports`

This functionality now belongs to the multimodal report pipeline.
