# Task: Add Audio Transcription and Fluency Agent

## Goal

Create the first real modality analyzer: an audio agent that transcribes spoken answers and computes safe observable communication signals.

This task builds the foundation for spoken-answer evaluation.

## Scope

Implement only:

- `audio_agent.py` or `audio_transcription_agent.py` service.
- Transcription service wrapper using configured OpenAI transcription model or mock mode.
- Communication signal extraction from transcript/audio metadata.
- Worker task to process an answer audio file.
- Store transcript and communication metrics on `candidate_answers`.
- Safe structured output schema.

## Out of Scope

Do not implement:

- Final answer evaluation.
- Benchmark-aware scoring.
- Video analysis.
- Text answer analysis.
- Code answer analysis.
- Final report.
- Frontend recording UI polish.

## Files Likely Involved

- `backend/app/services/audio_agent.py`
- `backend/app/services/transcription.py`
- `backend/app/services/communication_analysis.py`
- `backend/app/tasks/process_audio_answer.py`
- `backend/app/models/answer.py`
- `backend/app/schemas/answer.py`
- `backend/app/api/jobs.py`
- `backend/tests/`

## Output Schema

The audio agent should return structured data like:

```json
{
  "transcript": "string",
  "word_count": 120,
  "duration_seconds": 72.4,
  "words_per_minute": 99.4,
  "filler_word_count": 8,
  "filler_words": ["um", "like"],
  "hesitation_markers": [],
  "structure_observations": [],
  "communication_signal_score": 7
}
```

## Safe Language Rules

Use:

```txt
communication signal score
speaking pace
filler words
pause markers
answer structure
clarity
```

Do not use:

```txt
true confidence detection
emotion detection
personality detection
truthfulness detection
```

## Acceptance Criteria

- [ ] Audio agent service exists.
- [ ] Mock mode works without OpenAI API key.
- [ ] Real transcription path uses configured transcription model.
- [ ] Transcript is stored on candidate answer.
- [ ] Communication metrics are stored on candidate answer.
- [ ] No unsupported confidence/emotion/personality claims are made.
- [ ] No final evaluation or report generation is added.

## Verification

Run:

```bash
pytest backend/tests
```

Manual check:

1. Upload spoken answer audio.
2. Run audio processing task.
3. Confirm transcript and communication metrics are stored.

## Notes for Codex

- This is the first real agent in the multimodal system.
- Keep its output typed and deterministic in mock mode.
- Do not evaluate answer correctness here; that belongs to the final evaluation orchestrator.
