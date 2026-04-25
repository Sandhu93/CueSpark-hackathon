# 06 — API Contracts

This document defines the intended backend API. Exact implementation may evolve, but route names should remain product-oriented.

## Sessions

### Create Session

```http
POST /sessions
```

Request:

```json
{
  "job_description_text": "string",
  "resume_text": "string optional",
  "resume_object_key": "string optional",
  "resume_filename": "string optional"
}
```

Response:

```json
{
  "id": "session_id",
  "status": "created",
  "prepare_job_id": "job_id optional"
}
```

### Get Session

```http
GET /sessions/{session_id}
```

Response includes:

```json
{
  "id": "session_id",
  "status": "ready",
  "role_title": "string",
  "match_score": 72,
  "current_question_index": 0
}
```

### Prepare Session

```http
POST /sessions/{session_id}/prepare
```

Creates/enqueues a `prepare_session` job.

## Questions

### List Questions

```http
GET /sessions/{session_id}/questions
```

Response:

```json
{
  "items": [
    {
      "id": "question_id",
      "question_number": 1,
      "category": "technical",
      "question_text": "string",
      "difficulty": "medium",
      "tts_status": "not_requested",
      "tts_audio_url": null
    }
  ]
}
```

### Generate Question Audio

```http
POST /questions/{question_id}/tts
```

Response:

```json
{
  "question_id": "question_id",
  "job_id": "job_id",
  "tts_status": "queued"
}
```

### Get Question Audio URL

```http
GET /questions/{question_id}/tts
```

Response:

```json
{
  "question_id": "question_id",
  "tts_status": "generated",
  "audio_url": "presigned_url"
}
```

## Answers

### Submit Candidate Answer

```http
POST /questions/{question_id}/answers
```

Request options:

- Multipart upload with audio file.
- Or JSON with existing `audio_object_key` if uploaded through presigned flow.

Response:

```json
{
  "answer_id": "answer_id",
  "transcription_job_id": "job_id",
  "status": "queued"
}
```

### Get Answer

```http
GET /answers/{answer_id}
```

Response:

```json
{
  "id": "answer_id",
  "question_id": "question_id",
  "transcription_status": "transcribed",
  "transcript": "string",
  "evaluation": {
    "overall_score": 6,
    "strict_feedback": "string"
  }
}
```

## Reports

### Generate Report

```http
POST /sessions/{session_id}/report
```

Response:

```json
{
  "job_id": "job_id",
  "status": "queued"
}
```

### Get Report

```http
GET /sessions/{session_id}/report
```

Response:

```json
{
  "readiness_score": 68,
  "hiring_recommendation": "maybe",
  "summary": "string",
  "skill_gaps": [],
  "answer_feedback": [],
  "improvement_plan": []
}
```

## Jobs

Reuse existing job endpoint:

```http
POST /jobs
GET /jobs/{job_id}
```

Registered job kinds:

```text
prepare_session
generate_question_audio
transcribe_answer
evaluate_answer
generate_report
```

## Uploads

Reuse existing upload endpoints:

```http
POST /uploads/init
POST /uploads/direct
```

Use storage prefixes:

```text
resumes/original/
audio/questions/
audio/answers/
reports/
```
