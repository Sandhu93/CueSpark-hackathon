# Deprecated Task: Add Answer Read API

## Status

Deprecated as a standalone task for the current product roadmap.

The read API is still needed, but it must now expose multimodal answer data and agent results. That work should be handled under the active product frontend/backend integration path and API contracts:

```txt
docs/09-api-contracts-detailed.md
tasks/phase5-multimodal-evaluation/030-add-agent-result-storage.md
tasks/phase5-multimodal-evaluation/032-add-final-evaluation-orchestrator.md
tasks/phase6-product-frontend/034-update-frontend-api-client-for-multimodal.md
```

## Why This Is Deprecated

The old task only returns transcript, communication metrics, and a simple benchmark-aware evaluation.

The current answer read response should include:

- answer mode
- transcript
- text answer
- code answer metadata
- communication metadata
- visual signal metadata
- agent results
- final answer evaluation
- modality breakdown

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Follow `docs/09-api-contracts-detailed.md` and active multimodal tasks instead.
