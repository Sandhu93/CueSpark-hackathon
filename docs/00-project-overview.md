# 00 — Project Overview

## Product Name

**CueSpark Interview Coach**

## One-Line Description

CueSpark Interview Coach helps job seekers practice realistic role-specific mock interviews when they do not have access to an expert interviewer.

## Target Users

Initial users:

- Job seekers applying to job roles.
- Experienced professionals switching roles.

The system must support any job role, not only software/IT. For non-technical roles, “technical” means role-specific competency.

## Core User Flow

```text
Candidate opens app
  -> pastes job description
  -> uploads or pastes resume
  -> system creates interview session
  -> system analyzes JD-resume fit
  -> system generates interview plan
  -> interviewer bot asks one question at a time using voice
  -> candidate records an answer
  -> system transcribes and evaluates the answer
  -> final strict interviewer report is generated
```

## Interview Mode

Initial version is **turn-based**:

- One question is shown and played as audio.
- Candidate records one answer.
- Candidate submits the answer.
- Backend transcribes and evaluates.
- Candidate moves to the next question.

Realtime conversation is future scope.

## Interview Categories

Every interview plan should contain a balanced mix from these categories:

1. `technical`
2. `project_experience`
3. `behavioral`
4. `hr`
5. `resume_gap`
6. `jd_skill_validation`

For non-software roles, `technical` means job-specific competency, tools, process knowledge, domain knowledge, and practical execution ability.

## Scoring Style

The final report must include:

- Overall readiness score: `0-100`
- JD match score
- Technical / role-specific depth
- Communication clarity
- Evidence and examples
- Role relevance
- Confidence/fluency signal
- Improvement priority
- Strict hiring-style recommendation

The tone should be **strict interviewer style**, not soft coaching. However, feedback should remain professional and actionable.

## Allowed Claims

The app may claim:

- It analyzes communication signals.
- It estimates fluency from transcript and audio metadata.
- It identifies filler words, answer structure, relevance, and hesitation markers.

The app must not claim:

- It detects true confidence.
- It detects emotions reliably.
- It replaces a human recruiter.
- It guarantees interview success.

## Initial Version Scope

In scope:

- Single-session demo without login.
- JD paste input.
- Resume upload and resume paste fallback.
- PDF/DOCX text parsing.
- OCR provision but not OCR implementation.
- Local Docker Postgres + pgvector.
- MinIO storage.
- OpenAI TTS for interviewer voice.
- OpenAI transcription for candidate audio.
- Strict answer evaluation.
- Final report UI.

Out of scope:

- User accounts.
- Billing.
- Recruiter dashboard.
- Full WebRTC meeting.
- Live video analysis.
- Coding compiler.
- Monaco editor.
- OCR implementation.
- Job URL scraping.
