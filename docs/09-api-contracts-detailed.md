# API Contracts

This document defines the first-version API surface. Codex should not invent additional endpoints unless a task file explicitly requires them.

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
  "company_name": "string | null",
  "match_score": 0,
  "created_at": "datetime"
}
```

---

### POST `/api/sessions/{session_id}/prepare`

Starts background preparation.

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

## Questions

### GET `/api/sessions/{session_id}/questions`

List generated questions.

Response:

```json
{
  "questions": [
    {
      "id": "uuid",
      "question_number": 1,
      "category": "technical",
      "difficulty": "medium",
      "question_text": "string",
      "expected_signal": "string",
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

Upload candidate answer audio.

Form-data:

```txt
audio: webm/wav/mp3
```

Response:

```json
{
  "answer_id": "uuid",
  "job_id": "string",
  "status": "queued"
}
```

---

### GET `/api/answers/{answer_id}`

Get answer transcript, communication metrics, and evaluation.

Response:

```json
{
  "id": "uuid",
  "transcript": "string | null",
  "duration_seconds": 0,
  "word_count": 0,
  "words_per_minute": 0,
  "filler_word_count": 0,
  "evaluation": {
    "overall_score": 0,
    "relevance_score": 0,
    "role_depth_score": 0,
    "evidence_score": 0,
    "clarity_score": 0,
    "strict_feedback": "string"
  }
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

Get final report.

Response:

```json
{
  "readiness_score": 0,
  "hiring_recommendation": "strong_yes | yes | maybe | no",
  "summary": "string",
  "skill_gaps": [],
  "answer_feedback": [],
  "resume_feedback": [],
  "improvement_plan": []
}
```
