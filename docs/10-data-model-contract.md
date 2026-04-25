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

## `benchmark_profiles`

Required fields:

- `id`
- `role_key`
- `role_title`
- `seniority_level`
- `domain`
- `profile_name`
- `resume_text`
- `skills`
- `tools`
- `project_signals`
- `impact_signals`
- `ownership_signals`
- `source_type`: `curated | public | synthetic`
- `source_url`
- `is_curated`
- `quality_score`
- `created_at`

For the hackathon version, profiles must be curated/anonymized fixtures. Do not store scraped personal resumes.

## `benchmark_comparisons`

Required fields:

- `id`
- `session_id`
- `role_key`
- `benchmark_profile_ids`
- `benchmark_similarity_score`
- `resume_competitiveness_score`
- `evidence_strength_score`
- `missing_skills`
- `weak_skills`
- `missing_metrics`
- `weak_ownership_signals`
- `interview_risk_areas`
- `recommended_resume_fixes`
- `question_targets`
- `created_at`

This table stores the novelty-layer output used by benchmark-driven question generation and final reports.

## `interview_questions`

Required fields:

- `id`
- `session_id`
- `question_number`
- `category`
- `question_text`
- `expected_signal`
- `difficulty`
- `source`: `base_plan | adaptive_followup | benchmark_gap`
- `benchmark_gap_refs`
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
benchmark_gap_validation
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
- `benchmark_gap_coverage_score`
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
- `benchmark_similarity_score`
- `resume_competitiveness_score`
- `evidence_strength_score`
- `skill_gaps`
- `benchmark_gaps`
- `interview_risk_areas`
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
benchmark_profile
answer
rubric
question_bank
```

For benchmark profile chunks:

```txt
owner_type = benchmark_profile
owner_id = benchmark_profiles.id
chunk_type = benchmark_profile
```

## Notes

- Store large files in MinIO, not Postgres.
- Store MinIO object keys in the database.
- Store JSON-like evaluation details in JSONB fields.
- Use `vector(1536)` if using OpenAI `text-embedding-3-small` with default dimensions.
- Do not claim benchmark profiles are verified hired-candidate resumes unless verified source data exists.
