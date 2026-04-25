# Deprecated Task: Add Benchmark-Aware Answer Evaluation Service

## Status

Deprecated for the current product roadmap.

This older single-service evaluation task has been superseded by the multimodal evaluation phase:

```txt
tasks/phase5-multimodal-evaluation/030-add-agent-result-storage.md
tasks/phase5-multimodal-evaluation/031-add-benchmark-gap-agent.md
tasks/phase5-multimodal-evaluation/032-add-final-evaluation-orchestrator.md
```

## Why This Is Deprecated

The old task assumes one `answer_evaluator.py` evaluates transcript + communication metrics directly.

The current architecture separates evaluation into:

1. modality-agent outputs
2. benchmark-gap coverage agent
3. final evaluation orchestrator

This gives CueSpark support for:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
```

and keeps benchmark-gap coverage central.

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use the active Phase 5 multimodal evaluation task files instead.

## Historical Scope

The original intent was:

- `answer_evaluator.py`
- prompt for benchmark-aware answer evaluation
- worker task for evaluating one answer
- store results in `answer_evaluations`

This now belongs to the final evaluation orchestrator after agent results are available.
