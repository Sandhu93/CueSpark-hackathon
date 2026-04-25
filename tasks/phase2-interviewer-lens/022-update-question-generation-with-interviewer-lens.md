# Task: Update Question Generation with Interviewer Lens

## Goal

Use optional interviewer lens analysis to personalize benchmark-driven questions.

The core question strategy must remain benchmark-driven. Interviewer Lens should sharpen question style and focus, not replace benchmark gaps.

## Scope

Implement only:

- Update question generation input to include interviewer lens when available.
- Modify prompt/schema usage to include likely interviewer focus areas.
- Store interviewer-lens references in question provenance where supported.
- Keep total interview plan at 10 base questions.
- Preserve benchmark-gap-driven generation as the primary strategy.

## Out of Scope

Do not implement:

- LinkedIn scraping.
- Interviewer context upload.
- Interviewer context analysis.
- Frontend UI.
- TTS changes.
- Report changes.
- Adaptive follow-up generation.

## Files Likely Involved

- `backend/app/services/question_generator.py`
- `backend/app/services/prompts.py`
- `backend/app/schemas/question.py`
- `backend/app/models/question.py`
- `backend/app/tasks/prepare_session.py`

## Generation Rule

Question generation should use this priority order:

```txt
1. JD requirements
2. Candidate resume gaps
3. Benchmark comparison gaps
4. Interviewer Lens focus areas
```

## Acceptance Criteria

- [ ] Question generation still works without interviewer context.
- [ ] If interviewer lens exists, question generation uses likely focus areas.
- [ ] Questions do not claim exact prediction of what the interviewer will ask.
- [ ] Questions remain tied to benchmark gaps when benchmark data exists.
- [ ] Question provenance includes interviewer lens references where supported.
- [ ] Mock mode works without OpenAI API key.
- [ ] No frontend changes are made.

## Verification

Run:

```bash
pytest backend/tests
```

Manual verification:

1. Create session.
2. Add JD/resume.
3. Add interviewer context.
4. Run interviewer lens analysis.
5. Generate questions.
6. Confirm questions combine benchmark gaps and likely interviewer focus areas.

## Notes for Codex

- Do not generate generic interviewer-personalized questions.
- Do not make the interviewer lens the main product.
- The benchmark dashboard remains the core novelty.
