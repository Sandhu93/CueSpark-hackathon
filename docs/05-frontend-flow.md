# 05 — Frontend Flow

## Frontend Goal

The frontend should feel like a serious benchmark-driven interview readiness product, not a chatbot page.

The product experience must make three things obvious:

1. CueSpark compares the candidate against a role benchmark.
2. CueSpark generates questions from the candidate's actual evidence gaps.
3. CueSpark captures and evaluates the candidate response using the modalities required by each question.

Core flow:

```text
Landing
  -> Setup
  -> Match Summary
  -> Benchmark Gap Dashboard
  -> Interview Room
  -> Multimodal Evaluation Status
  -> Final Readiness Report
```

## Pages

### `/`

Landing/start page.

Should communicate:

- Product name: CueSpark Interview Coach.
- Promise: practice against the hiring benchmark, not just generic AI questions.
- Core idea: JD + resume + benchmark profiles -> benchmark gaps -> response-mode-aware interview -> readiness report.
- CTA: Start Benchmark Interview.

Avoid positioning it as only a voice-based mock interview app.

### `/setup`

Inputs:

- Job description textarea.
- Resume upload.
- Resume paste fallback textarea.
- Optional interviewer context later, if implemented.

Actions:

- Create session.
- Upload or store resume.
- Trigger preparation.
- Show preparation status.
- Navigate to match/benchmark flow when ready.

### `/session/[sessionId]/match`

Displays:

- JD-resume match score.
- Role title/domain inferred.
- Normalized role key.
- Candidate strengths.
- Candidate gaps.
- Preparation status for benchmark analysis.
- Button: View Benchmark Gaps.

This page is not the main product screen. It is a bridge into the benchmark dashboard.

### `/session/[sessionId]/benchmark`

Core benchmark-intelligence page.

Displays:

- Benchmark similarity score.
- Resume competitiveness score.
- Evidence strength score.
- Hiring bar gap if available.
- Retrieved benchmark profile summaries.
- Missing skills.
- Weak skills.
- Missing metrics.
- Weak ownership signals.
- Interview risk areas.
- Recommended resume fixes.
- Question targets generated from benchmark gaps.
- Button: Start Benchmark-Driven Interview.

Recommended visual layout:

```text
Candidate vs Hiring Benchmark

Benchmark Similarity: 54%
Resume Competitiveness: 48%
Evidence Strength: 39%
Hiring Bar Gap: High

Top Benchmark Gaps
1. No measurable impact
2. Weak ownership proof
3. Missing role-specific tool depth
4. No business outcome evidence
5. Weak project scale indicators

Interview Strategy
This interview will focus on ownership, metrics, role-specific depth, and project evidence.
```

This page should make the product differentiation obvious within 10 seconds.

### `/session/[sessionId]/interview`

Core interview execution page.

Displays:

- Question number.
- Question category.
- Difficulty.
- Question text.
- Why this question was asked.
- Benchmark gap being tested where applicable.
- Required response mode.
- Required modalities.
- Audio player for AI interviewer voice.
- Generate/play audio state.
- Response capture area based on question mode.
- Submit answer button.
- Processing status.
- Transcript and agent-result summaries after processing.
- Strict benchmark-aware feedback after evaluation.
- Next question button.

Question response modes:

```text
spoken_answer
written_answer
code_answer
mixed_answer
```

#### Spoken Answer UI

Show:

- microphone recording controls
- recording timer
- retry recording
- upload/submission state
- transcript after processing
- communication signals when available

#### Written Answer UI

Show:

- text area/editor
- answer structure guidance if useful
- submit text answer
- text analysis status

#### Code Answer UI

Show:

- code editor, later Monaco
- language selector
- optional explanation text
- submit code answer
- code analysis status

For the first product version, code evaluation can be static analysis only. Do not execute arbitrary code without a sandbox.

#### Mixed Answer UI

Show the relevant capture panels together, for example:

```text
Audio explanation + code editor
Audio explanation + written case answer
```

### `/session/[sessionId]/report`

Displays:

- Readiness score.
- Hiring recommendation without guarantee.
- JD-resume match summary.
- Benchmark similarity score.
- Resume competitiveness score.
- Evidence strength score.
- Missing benchmark signals.
- Interview risk radar.
- Answer-by-answer feedback.
- Benchmark gap coverage summary.
- Communication summary.
- Written answer summary if available.
- Code quality summary if available.
- Visual signal summary if available.
- Resume improvement suggestions based on benchmark gaps.
- Preparation plan.

The report should clearly show:

```text
How far the candidate is from the benchmark
What proof is missing
Which answers failed to address the benchmark gaps
Which modalities were strong or weak
What to improve before applying
```

## UX Tone

Visual style should be professional and serious.

Avoid:

- Cartoonish interview bot.
- Game-like colors.
- Chat bubble-only layout.
- Overly friendly feedback.
- Claiming benchmark profiles are real hired-candidate resumes.
- Claiming emotion, personality, truthfulness, or true-confidence detection.

Prefer:

- Interview room feel.
- Benchmark scorecards.
- Risk radar.
- Evidence gap panels.
- Strict feedback panels.
- Response-mode indicators.
- Modality signal panels.
- Clear progress indicator.
- Minimal distractions.

## Recording UX

The browser should record candidate audio using MediaRecorder.

Expected UI states:

```text
idle
recording
recorded_not_submitted
uploading
transcribing
running_agents
evaluating
evaluated
failed
```

Candidate should be able to retry recording before submitting.

## Video/Visual Signal UX

For MVP, visual signals should be optional and carefully labeled.

Allowed labels:

```text
face in frame
lighting quality
eye contact proxy
posture stability
camera presence
visual signal summary
```

Do not display:

```text
emotion score
true confidence score
personality score
truthfulness score
```

Recommended disclaimer:

```text
Observable visual presence signals only — no emotion, personality, truthfulness, or true-confidence detection.
```

## Benchmark UX Requirements

The frontend should explain benchmark data honestly:

Use:

```text
Curated benchmark profiles
Role benchmark corpus
Top-candidate archetypes
```

Do not use:

```text
Hired resumes
Selected resumes
LinkedIn selected profiles
```

The benchmark page should make clear that the benchmark is used to identify evidence gaps and interview risks.

## API Client Rule

All backend calls should go through `frontend/src/lib/api.ts`.

Avoid scattering `fetch()` calls across page components.

## Frontend Scope Control

Do not build until explicitly planned:

- Login.
- Billing.
- User dashboard.
- Multiple saved interviews.
- Full video recording storage.
- Realtime WebRTC meeting.
- Recruiter/admin screens.
- Live scraping UI.
- Unsandboxed code execution.
