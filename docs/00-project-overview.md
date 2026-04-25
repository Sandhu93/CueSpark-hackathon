# 00 — Project Overview

## Product Name

**CueSpark Interview Coach**

## One-Line Description

CueSpark Interview Coach is a benchmark-driven AI interview readiness platform that helps candidates practice against the hiring bar, not just against generic AI-generated questions.

## Target Users

Initial users:

- Job seekers applying to job roles.
- Experienced professionals switching roles.

The system must support any job role, not only software/IT. For non-technical roles, `technical` means role-specific competency.

## Core Product Idea

A normal AI mock interview can be created with one prompt. CueSpark adds a benchmark layer.

The system compares:

```txt
Candidate Resume ↔ Job Description ↔ Benchmark Profiles
```

Then it identifies what stronger candidates show that this candidate does not:

- missing skills
- weak skill evidence
- missing metrics
- weak ownership signals
- missing business impact
- weak project depth
- interview risk areas

The mock interview is generated from these benchmark gaps.

## Core User Flow

```text
Candidate opens app
  -> pastes job description
  -> uploads or pastes resume
  -> system creates interview session
  -> system analyzes JD-resume fit
  -> system retrieves curated benchmark profiles for the inferred role
  -> system compares candidate resume against benchmark profiles
  -> system generates benchmark gap analysis
  -> system generates benchmark-driven interview plan
  -> interviewer bot asks one question at a time using voice
  -> candidate records an answer
  -> system transcribes and evaluates the answer
  -> final benchmark-aware strict interviewer report is generated
```

## Benchmark Engine

The benchmark engine is the novelty layer.

For the hackathon version:

- Use curated/anonymized benchmark profiles.
- Do not live-scrape personal resumes.
- Do not claim profiles are verified hired-candidate resumes.
- Use safe wording: `benchmark profiles`, `curated top-candidate archetypes`, or `role benchmark corpus`.

Recommended initial benchmark roles:

```txt
project_manager
backend_developer
data_analyst
```

Each role should have 5 benchmark profiles.

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
7. `benchmark_gap_validation`

For non-software roles, `technical` means job-specific competency, tools, process knowledge, domain knowledge, and practical execution ability.

## Scoring Style

The final report must include:

- Overall readiness score: `0-100`
- JD match score
- Benchmark similarity score
- Resume competitiveness score
- Evidence strength score
- Role-specific depth
- Communication clarity
- Benchmark gap coverage
- Interview risk areas
- Strict hiring-style recommendation

The tone should be **strict interviewer style**, not soft coaching. However, feedback should remain professional and actionable.

## Allowed Claims

The app may claim:

- It compares candidate evidence against curated benchmark profiles.
- It analyzes communication signals.
- It estimates fluency from transcript and audio metadata.
- It identifies filler words, answer structure, relevance, and hesitation markers.
- It identifies resume/interview gaps relative to a role benchmark corpus.

The app must not claim:

- It uses verified hired-candidate resumes unless such verification exists.
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
- Curated benchmark profile fixtures.
- Benchmark profile seeding.
- Benchmark embedding and retrieval.
- Candidate-vs-benchmark comparison.
- Benchmark gap dashboard.
- Benchmark-driven question generation.
- OpenAI TTS for interviewer voice.
- OpenAI transcription for candidate audio.
- Benchmark-aware strict answer evaluation.
- Final benchmark-aware report UI.

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
- Live scraping of personal resumes from LinkedIn/Naukri/job boards.
