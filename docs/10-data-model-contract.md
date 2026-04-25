# 10 — Data Model Contract

Use UUID primary keys.

This contract reflects the current product direction:

```txt
benchmark-driven + multimodal interview readiness platform
```

The data model must support:

- benchmark preparation
- benchmark-driven questions
- response-mode-aware answers
- modality-agent outputs
- final answer evaluation
- multimodal readiness reports

---

## `interview_sessions`

Required fields:

- `id`
- `role_title`
- `role_key`
- `company_name`
- `job_description_text`
- `resume_text`
- `match_score`
- `benchmark_similarity_score`
- `resume_competitiveness_score`
- `evidence_strength_score`
- `status`
- `current_question_index`
- `metadata`
- `created_at`
- `updated_at`
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

---

## `documents`

Required fields:

- `id`
- `session_id`
- `document_type`: `resume | job_description`
- `input_type`: `paste | upload`
- `object_key`
- `filename`
- `content_type`
- `extracted_text`
- `parse_status`: `pending | parsed | failed | ocr_required`
- `metadata`
- `created_at`
- `updated_at`

---

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
- `updated_at`

Benchmark profiles must be curated/anonymized fixtures or otherwise legally usable sources. Do not store scraped personal resumes by default.

---

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
- `missing_project_depth`
- `interview_risk_areas`
- `recommended_resume_fixes`
- `question_targets`
- `created_at`
- `updated_at`

This table stores the benchmark-intelligence output used by:

- benchmark dashboard
- benchmark-driven question generation
- benchmark gap coverage agent
- final readiness report

---

## `interview_questions`

Required fields:

- `id`
- `session_id`
- `question_number`
- `category`
- `question_text`
- `expected_signal`
- `difficulty`
- `source`: `base_plan | adaptive_followup | manual | benchmark_gap`
- `benchmark_gap_refs`
- `why_this_was_asked`
- `provenance`
- `response_mode`
- `requires_audio`
- `requires_video`
- `requires_text`
- `requires_code`
- `tts_object_key`
- `tts_status`
- `created_at`
- `updated_at`

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

Valid response modes:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
```

Default mode:

```txt
response_mode = spoken_answer
requires_audio = true
requires_video = false
requires_text = false
requires_code = false
```

For non-software jobs, `technical` means role-specific competency, not programming.

---

## `candidate_answers`

Required fields:

- `id`
- `session_id`
- `question_id`
- `answer_mode`: `spoken_answer | written_answer | code_answer | mixed_answer`
- `audio_object_key`
- `transcript`
- `text_answer`
- `code_answer`
- `code_language`
- `transcription_status`: `pending | queued | transcribed | failed | not_required`
- `processing_status`: `pending | processing | evaluated | failed`
- `duration_seconds`
- `word_count`
- `words_per_minute`
- `filler_word_count`
- `communication_metadata`
- `visual_signal_metadata`
- `created_at`
- `updated_at`

Rules:

- Store audio files in MinIO, not Postgres.
- Store written/code answers in Postgres.
- Do not store full video files in MVP unless explicitly required.
- Store visual signal metadata/summaries instead.

---

## `agent_results`

Required fields:

- `id`
- `answer_id`
- `agent_type`
- `status`
- `score`
- `payload`
- `error`
- `created_at`
- `updated_at`

Valid agent types:

```txt
audio
video_signal
text_answer
code_evaluation
benchmark_gap
final_orchestrator
```

Valid statuses:

```txt
pending
running
succeeded
failed
```

`payload` should store the structured output of each agent as JSONB.

Examples:

```json
{
  "word_count": 130,
  "words_per_minute": 142,
  "filler_word_count": 6,
  "communication_signal_score": 7
}
```

```json
{
  "correctness_score": 8,
  "edge_case_score": 6,
  "complexity_score": 7,
  "readability_score": 8
}
```

---

## `answer_evaluations`

Required fields:

- `id`
- `answer_id`
- `relevance_score`
- `role_depth_score`
- `evidence_score`
- `structure_score`
- `jd_alignment_score`
- `benchmark_gap_coverage_score`
- `communication_signal_score`
- `code_quality_score`
- `written_answer_score`
- `visual_signal_score`
- `overall_score`
- `strengths`
- `weaknesses`
- `strict_feedback`
- `improved_answer`
- `red_flags`
- `modality_breakdown`
- `created_at`
- `updated_at`

`answer_evaluations` should store the final answer-level evaluation after the final evaluation orchestrator combines available agent outputs.

---

## `interview_reports`

Required fields:

- `id`
- `session_id`
- `readiness_score`
- `hiring_recommendation`
- `summary`
- `jd_resume_match_summary`
- `benchmark_similarity_score`
- `resume_competitiveness_score`
- `evidence_strength_score`
- `skill_gaps`
- `benchmark_gaps`
- `interview_risk_areas`
- `answer_feedback`
- `resume_feedback`
- `communication_summary`
- `visual_signal_summary`
- `written_answer_summary`
- `code_answer_summary`
- `improvement_plan`
- `created_at`
- `updated_at`

Valid hiring recommendations:

```txt
strong_yes
yes
maybe
no
strong_no
```

The report must not claim hiring guarantees.

---

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

Use `vector(1536)` if using OpenAI `text-embedding-3-small` with default dimensions.

---

## Optional/Future `interviewer_contexts`

Used only when user provides interviewer context by upload or paste.

Required fields if implemented:

- `id`
- `session_id`
- `input_type`: `upload | paste`
- `source_type`: `linkedin_pdf | public_bio | recruiter_note | manual`
- `object_key`
- `filename`
- `content_type`
- `raw_text`
- `extracted_text`
- `parse_status`: `pending | parsed | failed | ocr_required`
- `analysis_status`: `pending | analyzed | failed`
- `interviewer_name`
- `interviewer_title`
- `company`
- `likely_focus_areas`
- `question_bias`
- `metadata`
- `created_at`
- `updated_at`

Do not scrape LinkedIn. Accept user-provided PDFs/text only.

---

## Notes

- Store large files in MinIO, not Postgres.
- Store MinIO object keys in the database.
- Store JSON-like evaluation details in JSONB fields.
- Store agent outputs in `agent_results` so the final evaluator can combine them later.
- Store final answer-level evaluation in `answer_evaluations`.
- Store final session-level report in `interview_reports`.
- Do not store unsupported emotion, personality, truthfulness, or true-confidence labels.
- Do not execute arbitrary candidate code without a sandboxed runtime.
- Do not claim benchmark profiles are verified hired-candidate resumes unless verified source data exists.
