# Deprecated Task: Add Frontend API Client

## Status

Deprecated for the current product roadmap.

This older frontend-polish task has been superseded by the active product frontend task:

```txt
tasks/phase6-product-frontend/034-update-frontend-api-client-for-multimodal.md
```

## Why This Is Deprecated

The old task was written for a simpler benchmark-aware flow and mentions the previous frontend-polish phase. The current product direction is now:

```txt
benchmark-driven + multimodal AI interview readiness platform
```

The frontend API client must now support:

- response modes: `spoken_answer`, `written_answer`, `code_answer`, `mixed_answer`
- multimodal answer submission
- agent results
- final orchestrator evaluation
- multimodal readiness report
- communication, visual, text, and code summaries where available

The active replacement task already covers this broader API contract.

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use:

```txt
tasks/phase6-product-frontend/034-update-frontend-api-client-for-multimodal.md
```

## Historical Scope

The original intent was:

- Centralized frontend API client.
- TypeScript request/response types for current endpoints.
- Helpers for session creation, preparation, benchmark read, questions, TTS, answer upload, answer read, and report read.
- Basic error handling.

This functionality remains necessary, but it belongs inside the active multimodal API client task.
