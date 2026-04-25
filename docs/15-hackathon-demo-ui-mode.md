# 15 — Hackathon Demo UI Mode

## Purpose

The hackathon demo UI mode exists so CueSpark can present the full product vision to judges before every backend feature is fully implemented.

The real backend implementation is still the source of truth, but the demo mode allows the frontend to show:

```txt
Setup
→ Match Summary
→ Benchmark Gap Dashboard
→ Interview Room
→ Video/Audio Signal Panel
→ Final Readiness Report
```

This is especially useful because the current backend has the benchmark-preparation pipeline working, but the full interview execution loop and report pipeline are still being completed.

## Why This Exists

The benchmark engine is the core novelty, but judges also need to see the complete product experience.

A mock-data frontend mode helps demonstrate:

- how the benchmark dashboard looks
- how benchmark gaps become interview questions
- how the AI interview room will work
- how observable communication signals will be shown
- how the final readiness report will summarize gaps, answers, and preparation steps

## Rule: Demo Mode Must Not Fake Backend Completion

The demo UI may use mock data, but the app must clearly separate:

```txt
Implemented backend flow
```

from:

```txt
Demo preview / mock data flow
```

Use safe labels such as:

- Demo Preview
- Mock Data Mode
- Product Vision Preview
- Simulated Interview Room

Avoid labels such as:

- Production Ready
- Fully Implemented
- Live Evaluation Complete

## Recommended Frontend Approach

Add a simple frontend-only demo mode:

```txt
/demo
/demo/benchmark
/demo/interview
/demo/report
```

or add a toggle:

```txt
Use Demo Data
```

The safest hackathon approach is a separate `/demo` route group so the real implementation path remains clean.

## Mock Data Location

Store mock data in:

```txt
frontend/src/lib/demo/mock-data.ts
```

Suggested mock objects:

- `mockSession`
- `mockBenchmarkComparison`
- `mockInterviewQuestions`
- `mockAnswerTranscript`
- `mockCommunicationSignals`
- `mockFinalReport`

## Demo UI Screens

### 1. Demo Landing / Setup Preview

Shows the product flow and sample JD/resume/interviewer context.

### 2. Benchmark Dashboard

Must show:

- benchmark similarity score
- resume competitiveness score
- evidence strength score
- hiring bar gap
- missing skills
- weak evidence
- missing metrics
- weak ownership signals
- interview risk areas
- question targets

### 3. Interview Room

Must show:

- AI interviewer panel
- candidate video tile mock
- current benchmark-driven question
- why this question was asked
- benchmark gap references
- recording state
- answer transcript preview
- safe video/audio signal panel

Safe video/audio signals:

- face in frame
- lighting quality
- eye contact proxy
- posture stability
- speaking pace
- filler words
- answer structure

Do not claim emotion detection, true confidence detection, or personality detection.

### 4. Final Report

Must show:

- readiness score
- hiring recommendation
- JD-resume match
- benchmark similarity
- evidence strength
- interview risk areas
- answer-by-answer feedback
- resume improvement suggestions
- preparation plan

## Demo Copy

Recommended positioning:

```txt
CueSpark helps candidates practice against the hiring benchmark, not just against an AI chatbot.
```

Recommended explanation:

```txt
This demo preview shows the complete intended product experience using mock data. The implemented backend currently supports the benchmark-preparation pipeline; the interview execution and report generation layers are the next implementation phases.
```

## Out of Scope

Do not build these in demo mode:

- fake authentication
- fake payment screens
- fake recruiter dashboard
- fake scraping flow
- real video analysis claims
- emotion detection UI
- personality scoring UI

## Success Criteria

A judge should understand in 90 seconds:

1. What CueSpark is.
2. Why it is different from a generic AI mock interview.
3. How benchmark gaps drive the interview.
4. What the final report will provide.
5. What is implemented now and what is the next phase.
