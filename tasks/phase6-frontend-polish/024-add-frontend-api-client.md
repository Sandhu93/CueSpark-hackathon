# Task: Add Frontend API Client

## Goal

Create a typed frontend API client for CueSpark backend calls.

## Scope

Implement only:

- Centralized API client in `frontend/src/lib`.
- TypeScript request/response types for current endpoints.
- Helpers for session creation, preparation, questions, TTS, answer upload, answer read, and report read.
- Basic error handling.

## Out of Scope

Do not implement:

- Full UI pages.
- Audio recording component if already separate.
- State management libraries.
- Authentication.

## Files Likely Involved

- `frontend/src/lib/api.ts`
- `frontend/src/lib/types.ts`

## API Contract

Use `docs/09-api-contracts-detailed.md`.

## Data Model Changes

None.

## Acceptance Criteria

- [ ] API client uses `NEXT_PUBLIC_API_BASE_URL`.
- [ ] API response types match backend contracts.
- [ ] File/audio upload helpers support multipart form data.
- [ ] No React component contains raw fetch logic for product APIs.
- [ ] No authentication logic is added.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- Avoid `any` unless justified with a comment.
- Keep the client small and explicit.
