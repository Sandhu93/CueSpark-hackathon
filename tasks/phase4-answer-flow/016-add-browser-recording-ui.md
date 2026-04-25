# Deprecated Task: Add Browser Audio Recording UI

## Status

Deprecated for the current product roadmap.

This older audio-only task has been superseded by the multimodal product path:

```txt
tasks/phase4-multimodal-response/024-add-response-modality-model.md
tasks/phase4-multimodal-response/025-update-answer-upload-for-multimodal.md
tasks/phase4-multimodal-response/026-add-audio-transcription-agent.md
tasks/phase6-product-frontend/035-build-response-mode-aware-interview-room.md
tasks/phase6-product-frontend/036-add-spoken-answer-recording-flow.md
```

## Why This Is Deprecated

This task only adds a reusable browser microphone recording component. That was useful for the old audio-only answer flow, but the current product must support response modes:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
```

The current frontend should be built around a response-mode-aware interview room, not a standalone audio recorder.

## Do Not Execute This Task

Do not give this file to Codex for the current product implementation.

Use the active Phase 4 and Phase 6 task files instead.

## Historical Scope

The original intent was:

- Audio recording component using browser APIs.
- Start/stop recording controls.
- Display basic recording state.
- Produce an audio blob suitable for upload.
- Graceful handling when microphone permission is denied.

This functionality is still needed, but it should be implemented inside the active product task:

```txt
tasks/phase6-product-frontend/036-add-spoken-answer-recording-flow.md
```
