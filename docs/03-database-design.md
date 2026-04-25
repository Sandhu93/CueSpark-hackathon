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
  ├── interview_questions
  │     └── candidate_answers
  │             └── answer_evaluations
  ├── interview_reports
  └── embedding_chunks
```

## Tables

### interview_sessions

Stores one interview attempt.

Fields:

```text
id: string/uuid primary key
role_title: string nullable
company_name: string nullable
job_description_text: text
resume_text: text nullable
match_score: integer nullable
status: created | preparing | ready | in_progress | completed | failed
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

### interview_questions

Stores planned and adaptive questions.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id
question_number: integer
category: technical | project_experience | behavioral | hr | resume_gap | jd_skill_validation
question_text: text
expected_signal: text
source: base_plan | adaptive_followup | manual
provenance: jsonb
difficulty: easy | medium | hard
tts_object_key: string nullable
tts_status: not_requested | queued | generated | failed
created_at: datetime
updated_at: datetime
```

`provenance` should explain why this question was asked, for example:

```json
{
  "based_on": ["jd_required_skill", "resume_claim"],
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
audio_object_key: string
transcript: text nullable
transcription_status: pending | queued | transcribed | failed
duration_seconds: float nullable
word_count: integer nullable
words_per_minute: float nullable
filler_word_count: integer nullable
communication_metadata: jsonb
created_at: datetime
updated_at: datetime
```

### answer_evaluations

Stores strict evaluation for one answer.

```text
id: string/uuid primary key
answer_id: fk candidate_answers.id
relevance_score: integer 0-10
role_depth_score: integer 0-10
evidence_score: integer 0-10
structure_score: integer 0-10
jd_alignment_score: integer 0-10
communication_signal_score: integer 0-10
overall_score: integer 0-10
strengths: jsonb
weaknesses: jsonb
strict_feedback: text
improved_answer: text nullable
red_flags: jsonb
created_at: datetime
updated_at: datetime
```

### interview_reports

Stores final aggregate report.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id
readiness_score: integer 0-100
hiring_recommendation: strong_yes | yes | maybe | no | strong_no
summary: text
jd_resume_match_summary: text
interview_performance_summary: text
skill_gaps: jsonb
answer_feedback: jsonb
resume_feedback: jsonb
improvement_plan: jsonb
created_at: datetime
updated_at: datetime
```

### embedding_chunks

Stores vector chunks for JD, resume, answers, rubrics, and question bank.

```text
id: string/uuid primary key
session_id: fk interview_sessions.id nullable
owner_type: job_description | resume | answer | rubric | question_bank
owner_id: string nullable
chunk_type: jd | resume | answer | rubric | question_bank
content: text
embedding: vector(1536)
metadata: jsonb
created_at: datetime
```

Use `vector(1536)` for `text-embedding-3-small` unless explicitly changing embedding dimension.

## Indexing Guidance

Suggested indexes:

```text
interview_sessions.status
interview_questions.session_id
interview_questions.session_id + question_number
candidate_answers.question_id
answer_evaluations.answer_id
embedding_chunks.session_id
embedding_chunks.chunk_type
embedding_chunks.owner_type
embedding_chunks.embedding vector index
```

Vector index can be added after basic functionality works. Do not block early development on index tuning.

## Migration Note

The template currently uses `Base.metadata.create_all`. That is acceptable for the early local version.

Later, introduce Alembic migrations before production deployment.
