# Task: Add Security and Privacy Review

## Goal

Review CueSpark for product security, privacy, and safe-claims issues before moving toward public users.

CueSpark handles resumes, job descriptions, audio answers, transcripts, written answers, and possibly code. These are sensitive candidate artifacts.

## Scope

Review and fix only security/privacy issues related to:

- file upload validation
- audio upload validation
- object storage access
- signed URLs or public MinIO access patterns
- API error leakage
- transcript/log leakage
- prompt logging
- frontend claims about confidence/emotion/personality
- data retention assumptions
- code answer execution safety
- benchmark source claims

## Out of Scope

Do not implement:

- Authentication
- Payments
- Recruiter dashboard
- Enterprise compliance workflows
- Full data deletion workflow unless already simple
- Full secrets-management platform
- Production infrastructure changes

## Review Checklist

### Upload Safety

- Resume upload accepts only expected formats.
- Audio upload accepts only expected formats.
- File size limits exist or are documented.
- Uploaded files are stored in MinIO, not Postgres.
- Object keys are not guessable where possible.

### API Safety

- API errors do not expose stack traces in normal responses.
- Unknown resources return 404.
- Validation errors are clear but not overly revealing.
- No permanent MinIO credentials are exposed to frontend.

### AI/Prompt Safety

- Do not log full resumes/transcripts by default.
- Do not expose prompt internals in frontend.
- Mock mode does not leak sensitive fixture assumptions into production.

### Product Claims

The app must not claim:

- emotion detection
- true confidence detection
- personality scoring
- truthfulness detection
- hiring guarantee
- verified hired-candidate resumes unless verified

Preferred wording:

- observable communication signals
- visual presence signals
- eye contact proxy
- posture stability
- readiness recommendation
- benchmark gap coverage

### Code Safety

- Do not execute arbitrary candidate code on the main backend.
- Static code evaluation is allowed.
- Future execution must use sandboxing.

## Acceptance Criteria

- [ ] Upload constraints are clear and enforced where implemented.
- [ ] Frontend does not expose unsafe claims.
- [ ] Backend does not log sensitive candidate content unnecessarily.
- [ ] Object storage access is not dangerously open by default.
- [ ] Code execution is not performed unsafely.
- [ ] Findings are documented in `bugs.md` or a security notes section if issues remain.

## Verification

Run:

```bash
pytest backend/tests
cd frontend && npm run lint && npm run build
```

Manual review required for UI copy and error states.

## Notes for Codex

- This task is a review and tightening task.
- Do not add unrelated product features.
- Be conservative with privacy and claims.
