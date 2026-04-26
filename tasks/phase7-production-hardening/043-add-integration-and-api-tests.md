# Task: Add Integration and API Tests

## Goal

Add integration/API tests for the core CueSpark product flow so future development does not break the benchmark-driven multimodal interview pipeline.

This task should focus on product-critical paths, not exhaustive unit testing.

## Scope

Add tests for:

- session creation
- resume/JD intake
- session preparation in mock mode
- benchmark read API
- question list API
- TTS endpoint in mock mode
- multimodal answer submission
- answer processing orchestration in mock mode
- answer read API with agent results/evaluation
- report generation API
- report read API

## Out of Scope

Do not implement:

- New product features
- Frontend E2E tests with Playwright unless already configured
- Real OpenAI tests
- Load testing
- Security testing
- Production deployment

## Files Likely Involved

- `backend/tests/`
- `backend/tests/conftest.py`
- `backend/tests/test_sessions.py`
- `backend/tests/test_benchmark.py`
- `backend/tests/test_questions.py`
- `backend/tests/test_answers.py`
- `backend/tests/test_reports.py`

## Testing Requirements

Tests should run with:

```env
AI_MOCK_MODE=true
```

Do not depend on real OpenAI calls.

Where possible, use fixtures for:

- sample JD
- sample resume
- sample benchmark profile
- sample question
- sample answer

## Minimum Test Scenarios

### 1. Session Preparation

- Create session.
- Trigger preparation.
- Confirm session becomes ready or preparation output is stored in mock mode.
- Confirm benchmark comparison exists.
- Confirm questions exist.

### 2. Question and TTS

- Fetch questions.
- Generate TTS for one question in mock mode.
- Confirm audio URL/object key is returned or stable mock value is returned.

### 3. Spoken Answer Processing

- Submit spoken answer.
- Confirm answer row exists.
- Run or trigger processing pipeline.
- Confirm audio agent result exists.
- Confirm benchmark gap result exists.
- Confirm final evaluation exists.

### 4. Report

- Generate report.
- Confirm stored report exists.
- Confirm report contains readiness score, benchmark gaps, answer feedback, and modality summaries where available.

## Acceptance Criteria

- [ ] Tests cover the main product happy path.
- [ ] Tests run without OpenAI API key.
- [ ] Tests do not require manual DB state.
- [ ] Tests do not require real audio content unless a lightweight fixture already exists.
- [ ] Tests make failures obvious.
- [ ] Existing tests still pass.

## Verification

Run:

```bash
pytest backend/tests
```

## Notes for Codex

- Prefer reliable tests over broad but fragile tests.
- Use mock mode.
- Avoid network calls.
- Do not test frontend visuals in this task.
