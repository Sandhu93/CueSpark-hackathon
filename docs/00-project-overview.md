# 00 — Project Overview

## Product Name

**CueSpark Interview Coach**

## One-Line Description

CueSpark Interview Coach is a benchmark-driven, multimodal AI interview readiness platform that helps candidates practice against the hiring benchmark, not just against generic AI interview questions.

## Target Users

Primary users:

- Job seekers applying to a specific role.
- Experienced professionals switching role, domain, or seniority level.
- Students preparing for placements.
- Bootcamps, colleges, and placement teams that need scalable readiness diagnosis.
- Career coaches who want structured resume/interview gap analysis.

The system must support any job role, not only software/IT. For non-technical roles, `technical` means role-specific competency, tools, processes, domain knowledge, and practical execution ability.

## Core Product Idea

A normal AI mock interview can be created with one prompt. CueSpark adds two stronger product layers:

1. **Benchmark intelligence** — compare the candidate against a role-specific benchmark corpus.
2. **Multimodal evaluation** — evaluate the candidate response across the modalities required by the question.

The product compares:

```txt
Candidate Resume ↔ Job Description ↔ Benchmark Profiles ↔ Candidate Interview Response
```

Then it identifies what stronger candidates show that this candidate does not:

- missing skills
- weak skill evidence
- missing metrics
- weak ownership signals
- missing business impact
- weak project depth
- interview risk areas
- weak answer structure
- weak communication signals
- weak written response quality
- weak code quality where coding is required

The interview is generated from these benchmark gaps, and the final report explains whether the candidate addressed those gaps.

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
  -> question declares expected response mode
  -> candidate answers using audio, text, code, or mixed response as required
  -> modality agents analyze the response
  -> benchmark gap agent checks whether the tested gap was addressed
  -> final evaluation orchestrator combines agent outputs
  -> final multimodal benchmark-aware readiness report is generated
```

## Benchmark Engine

The benchmark engine is the first product differentiator.

Rules:

- Use curated/anonymized benchmark profiles.
- Do not live-scrape personal resumes by default.
- Do not claim profiles are verified hired-candidate resumes unless verification exists.
- Use safe wording: `benchmark profiles`, `curated top-candidate archetypes`, or `role benchmark corpus`.

Recommended initial benchmark roles:

```txt
project_manager
backend_developer
data_analyst
```

Each role should have multiple benchmark profiles covering entry-level, mid-level, experienced, role-switcher, and high-impact portfolio archetypes.

## Multimodal Evaluation

CueSpark questions can request different response modes:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
```

Each response mode activates the relevant analyzers:

- Audio Agent: transcript, pace, filler words, hesitation markers, clarity, structure.
- Text Answer Agent: relevance, structure, specificity, completeness, evidence, clarity.
- Code Evaluation Agent: correctness, edge cases, complexity, readability, testability, explanation quality.
- Video Signal Agent MVP: face in frame, lighting quality, camera presence, eye contact proxy, posture stability, distraction markers.
- Benchmark Gap Agent: whether the candidate addressed the benchmark gap being tested.
- Final Evaluation Orchestrator: combines available agent outputs into a final answer score.

Video-related language must remain careful. CueSpark analyzes **observable visual presence signals**, not emotions, personality, truthfulness, or true confidence.

## Interview Mode

The first production version is **turn-based**:

- One question is shown and played as audio.
- Candidate responds using the expected response mode.
- Candidate submits the answer.
- Backend runs the relevant modality agents.
- Candidate sees transcript/status/feedback.
- Candidate moves to the next question.

Realtime WebRTC conversation is future scope.

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
- Benchmark gap coverage
- Communication signal summary
- Text/code quality summaries where applicable
- Interview risk areas
- Strict hiring-style recommendation without a guarantee

The tone should be **strict interviewer style**, not soft coaching. Feedback should remain professional, evidence-based, and actionable.

## Allowed Claims

The app may claim:

- It compares candidate evidence against curated benchmark profiles.
- It analyzes observable communication signals.
- It estimates fluency from transcript and audio metadata.
- It identifies filler words, answer structure, relevance, and hesitation markers.
- It analyzes written answers for structure, evidence, specificity, and completeness.
- It analyzes code answers for correctness, complexity, edge cases, readability, and explanation quality.
- It identifies resume/interview gaps relative to a role benchmark corpus.

The app must not claim:

- It uses verified hired-candidate resumes unless such verification exists.
- It detects true confidence.
- It detects emotions reliably.
- It scores personality.
- It detects truthfulness.
- It replaces a human recruiter.
- It guarantees interview success.

## Product Scope

In scope for the product roadmap:

- JD paste input.
- Resume upload and resume paste fallback.
- PDF/DOCX/TXT parsing.
- OCR-ready parse status, with OCR implementation later.
- Local Docker Postgres + pgvector.
- MinIO storage.
- Curated benchmark profile fixtures and seeding.
- Benchmark embedding and retrieval.
- Candidate-vs-benchmark comparison.
- Benchmark gap dashboard.
- Benchmark-driven question generation.
- OpenAI TTS for interviewer voice.
- Response-mode-aware interview room.
- Audio recording and transcription.
- Text answer capture and analysis.
- Code answer capture and static code analysis.
- Safe visual signal summary MVP.
- Benchmark-gap coverage analysis.
- Final multimodal evaluation orchestrator.
- Final benchmark-aware readiness report.

Out of scope until explicitly planned:

- Billing.
- Recruiter dashboard.
- Full WebRTC meeting.
- Full video recording storage.
- Emotion detection.
- Personality scoring.
- True confidence detection.
- Truthfulness detection.
- Unsandboxed code execution.
- Live scraping of personal resumes from LinkedIn/Naukri/job boards.
