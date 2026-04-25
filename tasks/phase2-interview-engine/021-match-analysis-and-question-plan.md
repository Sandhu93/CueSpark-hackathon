# Task 021 — Match Analysis and Question Plan

## Goal

Generate JD-resume match analysis and a 10-question interview plan.

## Read First

- `docs/00-project-overview.md`
- `docs/04-ai-audio-rag-design.md`
- `docs/06-api-contracts.md`

## Requirements

1. Add typed AI output schemas in `backend/app/schemas/ai_outputs.py`.
2. Add `backend/app/services/match_analyzer.py`.
3. Add `backend/app/services/question_generator.py`.
4. Update `prepare_session` to:
   - generate match analysis
   - save `match_score`, `role_title`, and metadata on session
   - generate 10 base questions
   - save questions to `interview_questions`
   - mark session `ready`
5. Add `GET /sessions/{session_id}/questions`.

## Question Plan Requirements

Questions must cover:

- `technical`
- `project_experience`
- `behavioral`
- `hr`
- `resume_gap`
- `jd_skill_validation`

Every question must include:

- question number
- category
- question text
- expected signal
- difficulty
- provenance

## Acceptance Criteria

- Preparing a valid session creates 10 questions.
- Questions are role-agnostic and do not assume software unless JD/resume is software-related.
- Match score is stored.
- Session status becomes `ready`.
- `GET /sessions/{id}/questions` returns the question list.

## Out of Scope

- Adaptive follow-up logic.
- TTS audio generation.
- Candidate answer evaluation.
