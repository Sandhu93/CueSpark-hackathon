# 05 — Frontend Flow

## Frontend Goal

The frontend should feel like a structured interview product, not a chatbot page.

Initial flow:

```text
Landing
  -> Setup
  -> Match Summary
  -> Interview Room
  -> Final Report
```

## Pages

### `/`

Landing/start page.

Should communicate:

- Product name: CueSpark Interview Coach.
- Promise: role-specific mock interviews from JD + resume.
- CTA: Start Mock Interview.

### `/setup`

Inputs:

- Job description textarea.
- Resume upload.
- Resume paste fallback textarea.

Actions:

- Create session.
- Show preparation status.
- Navigate to match summary when ready.

### `/session/[sessionId]/match`

Displays:

- JD-resume match score.
- Role title/domain inferred.
- Candidate strengths.
- Candidate gaps.
- Interview categories planned.
- Button: Start Interview.

### `/session/[sessionId]/interview`

Core page.

Displays:

- Question number.
- Question category.
- Difficulty.
- Question text.
- Audio player for AI interviewer voice.
- Generate/play audio state.
- Record answer button.
- Stop recording button.
- Submit answer button.
- Transcript after transcription.
- Strict feedback after evaluation.
- Next question button.

Do not show all future questions upfront. Keep the interview focused.

### `/session/[sessionId]/report`

Displays:

- Readiness score.
- Hiring recommendation.
- JD-resume match summary.
- Interview performance summary.
- Score breakdown.
- Answer-by-answer feedback.
- Skill gaps.
- Resume improvement suggestions.
- Preparation plan.

## UX Tone

Visual style should be professional and serious.

Avoid:

- Cartoonish interview bot.
- Game-like colors.
- Chat bubble-only layout.
- Overly friendly feedback.

Prefer:

- Interview room feel.
- Scorecards.
- Clear progress indicator.
- Strict feedback panels.
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
