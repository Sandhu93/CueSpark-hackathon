# Deprecated Task: Add Report API

## Status

Deprecated as a standalone task for the current product roadmap.

The report API is still required, but it must now return the multimodal readiness report contract defined in:

```txt
docs/09-api-contracts-detailed.md
tasks/phase5-multimodal-evaluation/033-add-multimodal-readiness-report.md
tasks/phase6-product-frontend/039-add-multimodal-readiness-report-page.md
```

## Why This Is Deprecated

The old task exposes a simpler benchmark-aware report. The current report must include multimodal sections:

- communication summary
- visual signal summary if available
- written answer summary if available
- code answer summary if available
- benchmark gap coverage summary
- final orchestrator scoring output

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use the active Phase 5 multimodal report task and the API contract document instead.

## Historical Scope

The original intent was:

- `POST /api/sessions/{session_id}/report`
- `GET /api/sessions/{session_id}/report`
- enqueue report generation
- return stored benchmark-aware report

These endpoints are still valid, but their implementation must follow the multimodal report contract.
