# Deprecated Task: Add Transcription Service

## Status

Deprecated for the current product roadmap.

This older task has been superseded by the multimodal audio-agent task:

```txt
tasks/phase4-multimodal-response/026-add-audio-transcription-agent.md
```

## Why This Is Deprecated

The old task only transcribed audio and stored a transcript. The current product needs an audio agent that does more than transcription:

- transcript generation
- word count
- speaking pace
- filler word count
- hesitation markers
- answer structure observations
- communication signal score
- structured agent output

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use:

```txt
tasks/phase4-multimodal-response/026-add-audio-transcription-agent.md
```

## Historical Scope

The original intent was:

- `transcription.py` service
- mock transcription
- real OpenAI transcription call
- worker task for transcribing an answer
- update `candidate_answers.transcript`

This is now part of the broader audio transcription and fluency agent.
