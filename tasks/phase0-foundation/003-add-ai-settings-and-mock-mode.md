# Task: Add AI Settings and Mock Mode

## Goal

Add centralized settings for OpenAI model configuration and deterministic mock mode so the app can be developed without real API calls.

## Scope

Implement only:

- Add AI-related environment variables to `.env.example`.
- Add backend config fields for AI provider, mock mode, and model names.
- Add a small mock response helper or convention for AI services to use later.
- Ensure API and worker can both read the same settings.

## Out of Scope

Do not implement:

- Real OpenAI client calls.
- TTS generation.
- Transcription.
- Embeddings.
- Question generation.
- Answer evaluation.

## Files Likely Involved

- `.env.example`
- `backend/app/core/config.py`
- `backend/app/services/`
- `README.md`

## API Contract

No new API endpoint is required in this task.

## Data Model Changes

None.

## Required Environment Variables

```env
AI_PROVIDER=openai
AI_MOCK_MODE=true
OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TRANSCRIBE_MODEL=gpt-4o-transcribe
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## Acceptance Criteria

- [ ] `.env.example` includes AI provider and model variables.
- [ ] Backend settings expose AI provider and mock mode.
- [ ] API and worker use the same settings source.
- [ ] Mock mode defaults to safe local-development behavior.
- [ ] No real OpenAI API calls are added in this task.
- [ ] No product feature endpoints are added in this task.

## Verification

Run:

```bash
docker compose up --build
```

Then inspect API logs and confirm configuration loads without crashing.

## Notes for Codex

- Do not hardcode model names inside future service modules.
- This task creates configuration only.
