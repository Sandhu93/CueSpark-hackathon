# 03 — Database Design

## Database Choice

Use local Docker Postgres with pgvector.

Change the Postgres image in `docker-compose.yml` from regular Postgres to a pgvector-enabled image, for example:

```yaml
postgres:
  image: pgvector/pgvector:pg16
```

Ensure the vector extension exists:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## Entity Relationship Summary

```text
interview_sessions
  ├── documents
  ├── benchmark_comparisons
  ├── interview_questions
  │     └── candidate_answers
  │             ├── agent_results
  │             └── answer_evaluations
  ├── interview_reports
  └── embedding_chunks

benchmark_profiles
  └── embedding_chunks
```

Optional future table:

```text
interviewer_contexts
  └── interview_sessions
```

## Tables

### interview_sessions

Stores one benchmark-driven interview attempt.

Fields:

```text
id: string/uuid primary key
role_title: string nullable
role_key: string nullable
company_name: string nullable
job_description_text: text
resume_text: text nullable
match_score: integer nullable
benchmark_similarity_score: integer nullable
resume_competitiveness_score: integer nullable
evidence_strength_score: integer nullable
status: draft | preparing | ready | in_progress | evaluating | report_ready | completed | failed
current_question_index: integer default 0
metadata: jsonb
created_at: datetime
updated_at: datetime
completed_at: datetime nullable
```

### documents

Stores JD/resume input metadata and extracted text.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id
document_type: job_description | resume
input_type: paste | upload
object_key: string nullable
filename: string nullable
content_type: string nullable
extracted_text: text nullable
parse_status: pending | parsed | failed | ocr_required
metadata: jsonb
created_at: datetime
updated_at: datetime
```

### benchmark_profiles

Stores curated/anonymized benchmark profiles used for comparison.

```text
id: string/uuid primary key
role_key: string
role_title: string
seniority_level: fresher | junior | mid | senior | lead | mixed
domain: string nullable
profile_name: string
resume_text: text
skills: jsonb
tools: jsonb
project_signals: jsonb
impact_signals: jsonb
ownership_signals: jsonb
source_type: curated | synthetic | public
source_url: string nullable
is_curated: boolean default true
quality_score: integer nullable
created_at: datetime
updated_at: datetime
```

Use curated/synthetic fixtures first. Do not store scraped personal resumes by default.

### benchmark_comparisons

Stores the benchmark gap analysis for a session.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id
role_key: string
benchmark_profile_ids: jsonb
benchmark_similarity_score: integer 0-100
resume_competitiveness_score: integer 0-100
evidence_strength_score: integer 0-100
missing_skills: jsonb
weak_skills: jsonb
missing_metrics: jsonb
weak_ownership_signals: jsonb
missing_project_depth: jsonb nullable
interview_risk_areas: jsonb
recommended_resume_fixes: jsonb
question_targets: jsonb
created_at: datetime
updated_at: datetime
```

This is the main benchmark-intelligence table. It should feed question generation, benchmark-gap scoring, and final report generation.

### interview_questions

Stores planned and adaptive questions.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id
question_number: integer
category: technical | project_experience | behavioral | hr | resume_gap | jd_skill_validation | benchmark_gap_validation
question_text: text
expected_signal: text
source: base_plan | adaptive_followup | manual | benchmark_gap
benchmark_gap_refs: jsonb nullable
why_this_was_asked: text nullable
provenance: jsonb
difficulty: easy | medium | hard
response_mode: spoken_answer | written_answer | code_answer | mixed_answer
requires_audio: boolean default true
requires_video: boolean default false
requires_text: boolean default false
requires_code: boolean default false
tts_object_key: string nullable
tts_status: not_requested | queued | generated | failed
created_at: datetime
updated_at: datetime
```

`provenance` should explain why this question was asked, for example:

```json
{
  "based_on": ["benchmark_gap", "jd_required_skill", "resume_claim"],
  "benchmark_gap_refs": ["missing_metric", "weak_project_ownership"],
  "jd_terms": ["stakeholder management", "risk reporting"],
  "resume_terms": ["project coordination"],
  "risk_area": "candidate claims coordination but lacks measurable outcomes"
}
```

### candidate_answers

Stores candidate response metadata and transcript.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id
question_id: fk interview_questions.id
answer_mode: spoken_answer | written_answer | code_answer | mixed_answer
audio_object_key: string nullable
transcript: text nullable
text_answer: text nullable
code_answer: text nullable
code_language: string nullable
transcription_status: pending | queued | transcribed | failed | not_required
processing_status: pending | processing | evaluated | failed
duration_seconds: float nullable
word_count: integer nullable
words_per_minute: float nullable
filler_word_count: integer nullable
communication_metadata: jsonb
visual_signal_metadata: jsonb nullable
created_at: datetime
updated_at: datetime
```

Rules:

- Audio binary belongs in MinIO, not Postgres.
- Text and code answers can be stored in Postgres.
- Full video should not be stored in MVP; prefer summary metadata.

### agent_results

Stores structured outputs from modality agents and orchestration steps.

```text
id: string/uuid primary key
answer_id: fk candidate_answers.id
agent_type: audio | video_signal | text_answer | code_evaluation | benchmark_gap | final_orchestrator
status: pending | running | succeeded | failed
score: integer nullable
payload: jsonb
error: text nullable
created_at: datetime
updated_at: datetime
```

Examples of `payload`:

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

### answer_evaluations

Stores final benchmark-aware evaluation for one answer after the final evaluation orchestrator combines agent results.

```text
id: string/uuid primary key
answer_id: fk candidate_answers.id
relevance_score: integer 0-10 nullable
role_depth_score: integer 0-10 nullable
evidence_score: integer 0-10 nullable
structure_score: integer 0-10 nullable
jd_alignment_score: integer 0-10 nullable
benchmark_gap_coverage_score: integer 0-10 nullable
communication_signal_score: integer 0-10 nullable
code_quality_score: integer 0-10 nullable
written_answer_score: integer 0-10 nullable
visual_signal_score: integer 0-10 nullable
overall_score: integer 0-10
strengths: jsonb
weaknesses: jsonb
strict_feedback: text
improved_answer: text nullable
red_flags: jsonb
modality_breakdown: jsonb
created_at: datetime
updated_at: datetime
```

### interview_reports

Stores final aggregate benchmark-aware report.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id
readiness_score: integer 0-100
hiring_recommendation: strong_yes | yes | maybe | no | strong_no
summary: text
jd_resume_match_summary: text
benchmark_similarity_score: integer nullable
resume_competitiveness_score: integer nullable
evidence_strength_score: integer nullable
benchmark_gaps: jsonb
interview_risk_areas: jsonb
interview_performance_summary: text
skill_gaps: jsonb
answer_feedback: jsonb
resume_feedback: jsonb
communication_summary: jsonb nullable
visual_signal_summary: jsonb nullable
written_answer_summary: jsonb nullable
code_answer_summary: jsonb nullable
improvement_plan: jsonb
created_at: datetime
updated_at: datetime
```

### embedding_chunks

Stores vector chunks for JD, resume, benchmark profiles, answers, rubrics, and question bank.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id nullable
owner_type: job_description | resume | benchmark_profile | answer | rubric | question_bank
owner_id: string nullable
chunk_type: jd | resume | benchmark_profile | answer | rubric | question_bank
content: text
embedding: vector(1536)
metadata: jsonb
created_at: datetime
```

Use `vector(1536)` for `text-embedding-3-small` unless explicitly changing embedding dimension.

### interviewer_contexts Optional/Future

Stores user-provided interviewer context if the candidate uploads a LinkedIn-exported PDF or pastes profile text.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id
input_type: upload | paste
source_type: linkedin_pdf | public_bio | recruiter_note | manual
object_key: string nullable
filename: string nullable
content_type: string nullable
raw_text: text nullable
extracted_text: text nullable
parse_status: pending | parsed | failed | ocr_required
analysis_status: pending | analyzed | failed
interviewer_name: string nullable
interviewer_title: string nullable
company: string nullable
likely_focus_areas: jsonb
question_bias: jsonb
metadata: jsonb
created_at: datetime
updated_at: datetime
```

Do not scrape LinkedIn. Accept user-provided PDFs/text only.

## Indexing Guidance

Suggested indexes:

```text
interview_sessions.status
interview_sessions.role_key
benchmark_profiles.role_key
benchmark_profiles.quality_score
benchmark_comparisons.session_id
interview_questions.session_id
interview_questions.session_id + question_number
interview_questions.response_mode
candidate_answers.question_id
candidate_answers.session_id
candidate_answers.answer_mode
agent_results.answer_id
agent_results.agent_type
agent_results.status
answer_evaluations.answer_id
interview_reports.session_id
embedding_chunks.session_id
embedding_chunks.chunk_type
embedding_chunks.owner_type
embedding_chunks.owner_id
embedding_chunks.embedding vector index
```

Vector index can be added after basic functionality works. Do not block early development on index tuning.

## Benchmark Data Rules

- Use curated/anonymized fixtures first.
- Do not store scraped personal resumes by default.
- Do not claim `source_type=public` means hired/selected unless verified.
- Prefer synthetic/curated benchmark archetypes initially.
- Store source attribution if a public source is later used.

## Safety Rules

- Do not store raw full video files in MVP unless explicitly required.
- Store visual signal summaries, not surveillance-style data.
- Do not store emotion, personality, truthfulness, or true-confidence labels.
- Do not execute arbitrary candidate code without a sandboxed runtime.

## Migration Note

The template currently uses `Base.metadata.create_all`. That is acceptable for the early local version.

Later, introduce Alembic migrations before production deployment.
