# Task 031 — Communication Signals and Answer Evaluation

## Goal

Evaluate each candidate answer using strict interviewer scoring and measurable communication signals.

## Read First

- `docs/00-project-overview.md`
- `docs/04-ai-audio-rag-design.md`
- `docs/07-codex-development-rules.md`

## Requirements

1. Add `backend/app/services/communication_analysis.py`.
2. Add `backend/app/services/answer_evaluator.py`.
3. Add `backend/app/tasks/evaluate_answer.py`.
4. Register `evaluate_answer` in `TASK_REGISTRY`.
5. Trigger evaluation after transcription completes.
6. Store result in `answer_evaluations`.

## Communication Signals

Compute deterministic signals:

- `word_count`
- `words_per_minute` if duration is available
- `filler_word_count`
- hesitation markers

Do not claim true confidence detection.

## Evaluation Rubric

Scores from 0 to 10:

- relevance_score
- role_depth_score
- evidence_score
- structure_score
- jd_alignment_score
- communication_signal_score
- overall_score

Feedback must be strict but professional.

## Acceptance Criteria

- Evaluation is created for transcribed answer.
- Strict feedback is saved.
- Scores are numeric and bounded.
- Evaluation does not run if transcript is empty.
- Answer API can return evaluation details.

## Out of Scope

- Final report aggregation.
- Adaptive follow-up questions.
