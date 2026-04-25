# Deprecated Task: Add Candidate Answer Upload API

## Status

Deprecated for the current product roadmap.

This older task only supports uploading recorded audio answers. It has been superseded by the multimodal answer submission task:

```txt
tasks/phase4-multimodal-response/025-update-answer-upload-for-multimodal.md
```

## Why This Is Deprecated

CueSpark now supports multiple response modes:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
```

The answer submission API must support audio, text, code, and mixed payloads. An audio-only endpoint is no longer sufficient.

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use:

```txt
tasks/phase4-multimodal-response/025-update-answer-upload-for-multimodal.md
```

## Historical Scope

The original intent was:

- `POST /api/questions/{question_id}/answers`
- Store uploaded audio in MinIO.
- Create `candidate_answers` row.
- Return answer ID for later processing.

This is now part of the broader multimodal answer submission task.
