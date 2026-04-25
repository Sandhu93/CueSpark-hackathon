# Task: Add Multimodal Readiness Report

## Goal

Update the final report generation so it can summarize benchmark gaps and multimodal evaluation outputs across the full interview session.

This report should become the product-grade version of CueSpark's final readiness report.

## Scope

Implement only:

- Update final report generator to include multimodal evaluation summaries.
- Aggregate answer evaluations across spoken, written, code, and mixed responses.
- Include benchmark gap coverage across the full session.
- Include audio communication summary.
- Include visual signal summary only if available.
- Include text/code answer quality summaries if available.
- Store report in `interview_reports`.

## Out of Scope

Do not implement:

- New modality agents.
- PDF export.
- Email export.
- Recruiter dashboard.
- Hiring guarantee claims.
- Frontend report redesign unless explicitly assigned.

## Files Likely Involved

- `backend/app/services/report_generator.py`
- `backend/app/services/prompts.py`
- `backend/app/models/report.py`
- `backend/app/models/evaluation.py`
- `backend/app/models/agent_result.py`
- `backend/app/schemas/report.py`
- `backend/app/tasks/generate_report.py`
- `backend/tests/`

## Report Sections

The report should include:

- overall readiness score
- hiring-style recommendation without guarantee
- JD-resume match summary
- benchmark similarity
- resume competitiveness
- evidence strength
- benchmark gap coverage summary
- answer-by-answer feedback
- audio communication summary
- visual presence summary if available
- written answer quality summary if available
- code answer quality summary if available
- resume improvement suggestions
- preparation plan

## Safe Language Rules

Use:

```txt
visual signal summary
communication signal summary
readiness recommendation
interview risk area
```

Do not use:

```txt
emotion analysis
true confidence score
personality score
selection guarantee
```

## Acceptance Criteria

- [ ] Final report aggregates multimodal answer evaluations.
- [ ] Report remains useful if only audio/transcript data exists.
- [ ] Report includes benchmark gap coverage across session.
- [ ] Report includes modality summaries only when data exists.
- [ ] Report avoids unsupported claims.
- [ ] Mock mode works.
- [ ] Existing report API is not broken.

## Verification

Run:

```bash
pytest backend/tests
```

Manual check with mixed mock answers is recommended.

## Notes for Codex

- The report should feel like a serious readiness diagnostic.
- Do not add fake precision.
- Benchmark gap coverage should remain the main scoring theme.
