# Data Model Contract

Use UUID primary keys.

## `interview_sessions`

Required fields:

- `id`
- `role_title`
- `company_name`
- `job_description_text`
- `resume_text`
- `match_score`
- `status`
- `created_at`
- `completed_at`

Valid statuses:

```txt
draft
preparing
ready
in_progress
evaluating
report_ready
completed
failed
```

## `documents`

Required fields:

- `id`
- `session_id`
- `document_type`: `resume | job_description`
- `input_type`: `paste | upload`
- `object_key`
- `extracted_text`
- `parse_status`: `pending | parsed | failed | ocr_required`
- `metadata`
- `created_at`

## `interview_questions`

Required fields:

- `id`
- `session_id`
- `question_number`
- `category`
- `question_text`
- `expected_signal`
- `difficulty`
- `source`: `base_plan | adaptive_followup`
- `tts_object_key`
- `created_at`

Valid categories:

```txt
technical
project_experience
behavioral
hr
resume_gap
jd_skill_validation
```

For non-software jobs, `technical` means role-specific competency, not programming.

## `candidate_answers`

Required fields:

- `id`
- `session_id`
- `question_id`
- `audio_object_key`
- `transcript`
- `duration_seconds`
- `word_count`
- `words_per_minute`
- `filler_word_count`
- `communication_metrics`
- `created_at`

## `answer_evaluations`

Required fields:

- `id`
- `answer_id`
- `relevance_score`
- `role_depth_score`
- `evidence_score`
- `clarity_score`
- `jd_alignment_score`
- `communication_score`
- `overall_score`
- `strengths`
- `weaknesses`
- `strict_feedback`
- `improved_answer`
- `created_at`

## `interview_reports`

Required fields:

- `id`
- `session_id`
- `readiness_score`
- `hiring_recommendation`
- `summary`
- `skill_gaps`
- `answer_feedback`
- `resume_feedback`
- `improvement_plan`
- `created_at`

Valid hiring recommendations:

```txt
strong_yes
yes
maybe
no
```

## `embedding_chunks`

Required fields:

- `id`
- `session_id`
- `owner_type`
- `owner_id`
- `chunk_type`
- `content`
- `embedding`
- `metadata`
- `created_at`

Valid chunk types:

```txt
jd
resume
answer
rubric
question_bank
```

## Notes

- Store large files in MinIO, not Postgres.
- Store MinIO object keys in the database.
- Store JSON-like evaluation details in JSONB fields.
- Use `vector(1536)` if using OpenAI `text-embedding-3-small` with default dimensions.
