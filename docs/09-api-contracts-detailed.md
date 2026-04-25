# 09 — API Contracts

This document defines the product API surface. Codex should not invent additional endpoints unless a task file explicitly requires them.

CueSpark APIs are organized around this product flow:

```txt
session setup
→ benchmark preparation
→ benchmark dashboard
→ question delivery + TTS
→ multimodal answer submission
→ modality-agent processing
→ final answer evaluation
→ readiness report
```

## Session

### POST `/api/sessions`

Create an interview session.

Request:

```json
{
  "job_description": "string",
  "resume_text": "string | null",
  "role_title": "string | null",
  "company_name": "string | null"
}
```

Response:

```json
{
  "session_id": "uuid",
  "status": "draft"
}
```

---

### GET `/api/sessions/{session_id}`

Get session state.

Response:

```json
{
  "id": "uuid",
  "status": "draft | preparing | ready | in_progress | evaluating | report_ready | completed | failed",
  "role_title": "string | null",
  "role_key": "string | null",
  "company_name": "string | null",
  "match_score": 0,
  "benchmark_similarity_score": 0,
  "resume_competitiveness_score": 0,
  "evidence_strength_score": 0,
  "current_question_index": 0,
  "created_at": "datetime"
}
```

---

### POST `/api/sessions/{session_id}/prepare`

Starts background preparation.

Preparation includes parsing, chunking, embeddings, JD-resume match analysis, benchmark retrieval, benchmark comparison, and benchmark-driven question generation.

Response:

```json
{
  "job_id": "string",
  "status": "queued"
}
```

---

## Documents

### POST `/api/sessions/{session_id}/resume`

Upload resume file.

Form-data:

```txt
file: PDF/DOCX/TXT
```

Response:

```json
{
  "document_id": "uuid",
  "parse_status": "pending"
}
```

---

## Benchmark

### GET `/api/sessions/{session_id}/benchmark`

Get benchmark comparison for a prepared session.

Response:

```json
{
  "session_id": "uuid",
  "role_key": "backend_developer",
  "benchmark_similarity_score": 54,
  "resume_competitiveness_score": 48,
  "evidence_strength_score": 39,
  "benchmark_profiles": [
    {
      "id": "uuid",
      "profile_name": "Backend Benchmark 01",
      "role_title": "Backend Developer",
      "seniority_level": "mid",
      "quality_score": 88
    }
  ],
  "missing_skills": [],
  "weak_skills": [],
  "missing_metrics": [],
  "weak_ownership_signals": [],
  "interview_risk_areas": [],
  "recommended_resume_fixes": [],
  "question_targets": []
}
```

This endpoint is read-only. It should not trigger benchmark generation.

---

## Questions

### GET `/api/sessions/{session_id}/questions`

List generated benchmark-driven questions.

Response:

```json
{
  "questions": [
    {
      "id": "uuid",
      "question_number": 1,
      "category": "benchmark_gap_validation",
      "difficulty": "medium",
      "question_text": "string",
      "expected_signal": "string",
      "source": "benchmark_gap",
      "benchmark_gap_refs": [],
      "why_this_was_asked": "string",
      "response_mode": "spoken_answer",
      "requires_audio": true,
      "requires_video": false,
      "requires_text": false,
      "requires_code": false,
      "tts_audio_url": "string | null"
    }
  ]
}
```

---

### POST `/api/questions/{question_id}/tts`

Generate interviewer audio on demand.

Response:

```json
{
  "question_id": "uuid",
  "audio_url": "string"
}
```

---

## Answers

### POST `/api/questions/{question_id}/answers`

Submit candidate answer for a question.

This endpoint must support multimodal answers based on the question's `response_mode` and modality flags.

#### Spoken answer multipart form-data

```txt
answer_mode: spoken_answer
audio: webm/wav/mp3
```

#### Written answer JSON

```json
{
  "answer_mode": "written_answer",
  "text_answer": "string"
}
```

#### Code answer JSON

```json
{
  "answer_mode": "code_answer",
  "code_answer": "string",
  "code_language": "python"
}
```

#### Mixed answer multipart form-data

```txt
answer_mode: mixed_answer
audio: optional webm/wav/mp3
text_answer: optional string
code_answer: optional string
code_language: optional string
visual_signal_metadata: optional JSON string
```

Response:

```json
{
  "answer_id": "uuid",
  "job_id": "string | null",
  "status": "queued | pending | stored"
}
```

Validation rules:

- If `requires_audio=true`, audio is required.
- If `requires_text=true`, `text_answer` is required.
- If `requires_code=true`, `code_answer` and `code_language` are required.
- Unsupported file types should return validation errors.
- Audio binary must be stored in MinIO, not Postgres.

---

### GET `/api/answers/{answer_id}`

Get answer details, transcript, modality-agent results, and evaluation.

Response:

```json
{
  "id": "uuid",
  "session_id": "uuid",
  "question_id": "uuid",
  "answer_mode": "spoken_answer | written_answer | code_answer | mixed_answer",
  "transcript": "string | null",
  "text_answer": "string | null",
  "code_answer": "string | null",
  "code_language": "string | null",
  "duration_seconds": 0,
  "word_count": 0,
  "words_per_minute": 0,
  "filler_word_count": 0,
  "communication_metadata": {},
  "visual_signal_metadata": {},
  "agent_results": [
    {
      "agent_type": "audio | video_signal | text_answer | code_evaluation | benchmark_gap | final_orchestrator",
      "status": "pending | running | succeeded | failed",
      "score": 0,
      "payload": {}
    }
  ],
  "evaluation": {
    "overall_score": 0,
    "relevance_score": 0,
    "role_depth_score": 0,
    "evidence_score": 0,
    "clarity_score": 0,
    "benchmark_gap_coverage_score": 0,
    "communication_signal_score": 0,
    "code_quality_score": 0,
    "written_answer_score": 0,
    "visual_signal_score": 0,
    "strict_feedback": "string",
    "modality_breakdown": {}
  }
}
```

---

## Agent Results

Agent results are usually created by worker tasks. A read endpoint is optional, but if implemented it should be read-only.

### GET `/api/answers/{answer_id}/agent-results`

Response:

```json
{
  "answer_id": "uuid",
  "agent_results": [
    {
      "id": "uuid",
      "agent_type": "audio",
      "status": "succeeded",
      "score": 7,
      "payload": {},
      "created_at": "datetime"
    }
  ]
}
```

---

## Report

### POST `/api/sessions/{session_id}/report`

Generate final report.

Response:

```json
{
  "job_id": "string",
  "status": "queued"
}
```

---

### GET `/api/sessions/{session_id}/report`

Get final multimodal benchmark-aware report.

Response:

```json
{
  "readiness_score": 0,
  "hiring_recommendation": "strong_yes | yes | maybe | no | strong_no",
  "summary": "string",
  "benchmark_similarity_score": 0,
  "resume_competitiveness_score": 0,
  "evidence_strength_score": 0,
  "skill_gaps": [],
  "benchmark_gaps": [],
  "interview_risk_areas": [],
  "answer_feedback": [],
  "resume_feedback": [],
  "communication_summary": {},
  "visual_signal_summary": {},
  "written_answer_summary": {},
  "code_answer_summary": {},
  "improvement_plan": []
}
```

The report must not make hiring guarantees or claim emotion/personality/true-confidence detection.
