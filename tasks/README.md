# Tasks

This folder contains phase-based implementation tasks for CueSpark Interview Coach.

Each task is intended to be given to Codex or another coding agent one at a time.

## Current Product Direction

CueSpark is now a:

```txt
benchmark-driven + multimodal AI interview readiness platform
```

The current product loop is:

```txt
JD + Resume + Benchmark Profiles
  -> Benchmark Gaps
  -> Gap-Driven Questions
  -> Multimodal Candidate Response
  -> Specialized Evaluation Agents
  -> Benchmark-Aware Readiness Report
```

## Rule

Do not ask an agent to implement the whole project at once. Use one task file at a time.

Recommended prompt:

```text
Read AGENTS.md, README.md, docs/00-project-overview.md, docs/01-architecture.md,
docs/02-backend-design.md, docs/13-benchmark-engine-design.md,
docs/16-multimodal-evaluation-orchestrator.md, and this task file.
Implement only this task. Do not add out-of-scope features.
Report changed files and verification steps.
```

## Active Product Phases

```text
phase0-foundation
phase1-session-documents
phase2-embeddings-match
phase2-benchmark-engine
phase2-demo-frontend          optional early benchmark demo slice
phase3-interview-engine
phase4-multimodal-response
phase5-multimodal-evaluation
phase6-product-frontend
phase7-production-hardening
```

## Deprecated / Superseded Phases

The following older phases are retained only for historical reference and should not be executed for the current product roadmap:

```text
phase4-answer-flow            superseded by phase4-multimodal-response
phase5-evaluation-report      superseded by phase5-multimodal-evaluation
phase4-report-frontend        superseded by phase5-multimodal-evaluation + phase6-product-frontend
phase-demo-ui                 hackathon preview only, not production product path
phase6-frontend-polish        superseded by phase6-product-frontend
```

## Recommended Current Execution Order

If Phase 6 is complete through product polish, stop adding major features and move to validation/hardening:

```text
phase7-production-hardening/042-end-to-end-product-validation.md
phase7-production-hardening/043-add-integration-and-api-tests.md
phase7-production-hardening/044-add-security-privacy-review.md
```

Then, before production or serious deployment, add formal migrations:

```text
phase7-production-hardening/041-add-alembic-migrations.md
```

## Previous Build Sequence

If rebuilding from Phase 3 onward, use:

```text
phase4-multimodal-response/024-add-response-modality-model.md
phase4-multimodal-response/025-update-answer-upload-for-multimodal.md
phase4-multimodal-response/026-add-audio-transcription-agent.md
phase5-multimodal-evaluation/030-add-agent-result-storage.md
phase5-multimodal-evaluation/031-add-benchmark-gap-agent.md
phase5-multimodal-evaluation/032-add-final-evaluation-orchestrator.md
phase5-multimodal-evaluation/034-add-answer-processing-orchestrator.md
phase5-multimodal-evaluation/033-add-multimodal-readiness-report.md
phase6-product-frontend/034-update-frontend-api-client-for-multimodal.md
phase6-product-frontend/035-build-response-mode-aware-interview-room.md
phase6-product-frontend/036-add-spoken-answer-recording-flow.md
phase6-product-frontend/037-add-written-and-code-answer-ui.md
phase6-product-frontend/038-add-agent-status-and-feedback-ui.md
phase6-product-frontend/039-add-multimodal-readiness-report-page.md
phase6-product-frontend/040-add-product-polish-error-retry-states.md
```

## Product Milestone Rule

The current milestone is not “more features.”

The current milestone is:

```txt
setup -> benchmark -> interview -> answer processing -> evaluation -> report
```

This must work end-to-end in mock mode and local Docker before adding new advanced features.
