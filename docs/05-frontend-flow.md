# 05 — Frontend Flow

## Frontend Goal

The frontend should feel like a structured benchmark-driven interview readiness product, not a chatbot page.

The most important demo moment is the benchmark gap dashboard. It must show that CueSpark compares the candidate against a role benchmark and generates the interview from those gaps.

Initial flow:

```text
Landing
  -> Setup
  -> Match Summary
  -> Benchmark Gap Dashboard
  -> Interview Room
  -> Final Report
```

## Pages

### `/`

Landing/start page.

Should communicate:

- Product name: CueSpark Interview Coach.
- Promise: practice against the hiring bar, not just generic AI questions.
- Core idea: JD + resume + benchmark profiles -> gap-driven mock interview.
- CTA: Start Benchmark Interview.

Avoid positioning it as only a voice-based mock interview app.

### `/setup`

Inputs:

- Job description textarea.
- Resume upload.
- Resume paste fallback textarea.

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

This page is not the main novelty screen. It is a bridge into the benchmark dashboard.

### `/session/[sessionId]/benchmark`

Core novelty page.

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

This page should make the novelty obvious to judges within 10 seconds.

### `/session/[sessionId]/interview`

Core interview page.

Displays:

- Question number.
- Question category.
- Difficulty.
- Question text.
- Why this question was asked.
- Benchmark gap being tested where applicable.
- Audio player for AI interviewer voice.
- Generate/play audio state.
- Record answer button.
- Stop recording button.
- Submit answer button.
- Transcript after transcription.
- Strict benchmark-aware feedback after evaluation.
- Next question button.

Do not show all future questions upfront. Keep the interview focused.

Example `why this question was asked` text:

```text
Benchmark profiles for this role usually show measurable delivery impact and ownership. Your resume mentions project coordination but does not show metrics or final ownership.
```

### `/session/[sessionId]/report`

Displays:

- Readiness score.
- Hiring recommendation.
- JD-resume match summary.
- Benchmark similarity score.
- Resume competitiveness score.
- Evidence strength score.
- Missing benchmark signals.
- Interview risk radar.
- Interview performance summary.
- Score breakdown.
- Answer-by-answer feedback.
- Resume improvement suggestions based on benchmark gaps.
- Preparation plan.

The report should clearly show:

```text
How far the candidate is from the benchmark
What proof is missing
Which answers failed to address the benchmark gaps
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

Prefer:

- Interview room feel.
- Benchmark scorecards.
- Risk radar.
- Evidence gap panels.
- Strict feedback panels.
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
evaluating
evaluated
failed
```

Candidate should be able to retry recording before submitting.

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

Do not build in v1:

- Login.
- Billing.
- User dashboard.
- Multiple saved interviews.
- Video analysis.
- Monaco editor.
- Full meeting UI.
- Admin screens.
- Live scraping UI.
