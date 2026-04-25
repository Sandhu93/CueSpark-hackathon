# Task: Add Frontend Demo Data Layer

## Goal

Create a frontend-only mock data layer that allows CueSpark to demonstrate the full product experience during the hackathon before every backend feature is complete.

This task must not modify backend behavior.

## Scope

Implement only:

- `frontend/src/lib/demo/mock-data.ts`
- `frontend/src/lib/demo/types.ts` if useful
- Mock session object
- Mock benchmark comparison object
- Mock interview question list
- Mock answer transcript
- Mock video/audio communication signals
- Mock final report object

## Out of Scope

Do not implement:

- Backend APIs
- Real TTS
- Real transcription
- Real evaluation
- Authentication
- Payments
- Recruiter dashboard
- Live scraping

## Files Likely Involved

- `frontend/src/lib/demo/mock-data.ts`
- `frontend/src/lib/demo/types.ts`

## Mock Data Requirements

Mock data should represent the full intended product flow:

```txt
Setup → Benchmark Gap Dashboard → Interview Room → Final Report
```

The benchmark mock should include:

- benchmark similarity score
- resume competitiveness score
- evidence strength score
- hiring bar gap
- missing skills
- weak skills
- missing metrics
- weak ownership signals
- interview risk areas
- recommended resume fixes
- question targets

The interview mock should include:

- at least 5 benchmark-driven questions
- category
- difficulty
- why this question was asked
- benchmark gap references
- expected signal

The communication mock should include only safe observable signals:

- face in frame
- lighting quality
- eye contact proxy
- posture stability
- speaking pace
- filler words
- answer structure

The report mock should include:

- readiness score
- hiring recommendation
- benchmark similarity
- resume competitiveness
- evidence strength
- answer feedback
- resume feedback
- preparation plan

## Acceptance Criteria

- [ ] Demo mock data is centralized in `frontend/src/lib/demo/`.
- [ ] No mock data is hardcoded directly inside page components.
- [ ] Mock data uses safe wording.
- [ ] No emotion detection, true confidence detection, or personality scoring appears.
- [ ] Existing real API client remains unchanged unless only type reuse is required.
- [ ] Frontend builds successfully.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- This is a hackathon presentation layer.
- Keep it separate from real backend API paths.
- Do not make fake backend calls.
