# Deprecated Task: Add Benchmark-Aware Final Report Service

## Status

Deprecated for the current product roadmap.

This older report service task has been superseded by the multimodal readiness report task:

```txt
tasks/phase5-multimodal-evaluation/033-add-multimodal-readiness-report.md
```

## Why This Is Deprecated

The old task generates a report from match analysis, benchmark comparison, questions, answers, evaluations, and communication metrics.

The current product report must additionally aggregate:

- modality-agent outputs
- benchmark-gap coverage across the session
- audio communication summary
- written-answer summary if available
- code-quality summary if available
- safe visual-signal summary if available
- final orchestrator evaluations

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use:

```txt
tasks/phase5-multimodal-evaluation/033-add-multimodal-readiness-report.md
```

## Historical Scope

The original intent was:

- `report_generator.py`
- final benchmark-aware report prompt
- report generation worker task
- store report in `interview_reports`

This now belongs to the multimodal readiness report task.
