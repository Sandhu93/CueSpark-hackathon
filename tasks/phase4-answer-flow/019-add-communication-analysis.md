# Deprecated Task: Add Communication Signal Analysis

## Status

Deprecated for the current product roadmap.

This older standalone task has been superseded by the multimodal audio-agent task:

```txt
tasks/phase4-multimodal-response/026-add-audio-transcription-agent.md
```

## Why This Is Deprecated

The old task computed communication metrics separately from transcription. The current product should treat these as part of the Audio Agent output so the final evaluation orchestrator can read a single structured agent result.

The Audio Agent should produce:

- transcript
- word count
- duration
- speaking pace
- filler words
- hesitation markers
- answer structure observations
- communication signal score

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use:

```txt
tasks/phase4-multimodal-response/026-add-audio-transcription-agent.md
```

## Historical Scope

The original intent was:

- deterministic word count
- estimated words per minute
- filler word count
- hesitation marker count
- communication metrics storage

This functionality remains necessary but belongs inside the active Audio Agent task.
