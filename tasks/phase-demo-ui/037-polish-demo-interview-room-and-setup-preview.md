# Task: Polish Demo Interview Room And Setup Preview

## Goal

Make the demo interview experience feel like a coherent product flow: setup context leads into a benchmark-driven interview room, then into the final report.

This is a frontend-only `/demo/*` polish task.

## Scope

Implement only:

- Visual polish for `/demo/interview`
- Optional demo-only setup preview section on `/demo`
- Stronger workflow progression from setup to benchmark to interview to report
- Static mock interview controls and transcript/workspace panels
- Safe communication signal presentation

## Out of Scope

Do not implement:

- Backend changes
- Real setup API changes
- Real camera access
- Real microphone recording
- Real TTS playback
- Real transcription
- Real evaluation
- WebRTC
- Monaco editor or code execution
- PDF export
- Email export
- Authentication
- Payments
- Emotion detection
- True confidence detection
- Personality scoring

## Files Likely Involved

- `frontend/src/app/demo/page.tsx`
- `frontend/src/app/demo/interview/page.tsx`
- `frontend/src/components/demo/`
- `frontend/src/lib/demo/mock-data.ts`
- `frontend/src/lib/demo/types.ts`

## UI Requirements

### `/demo`

Optionally add a setup-preview section inspired by the provided mock:

- JD input preview
- Resume input preview
- Optional interviewer-lens preview
- "What CueSpark will prepare" checklist
- Workflow steps:
  - Setup
  - Match
  - Benchmark
  - Interview
  - Report

This section must be static and must not replace or break the real `/setup` route.

### `/demo/interview`

Make the page feel closer to a premium interview room:

- Interview progress header:
  - mock status
  - mock timer
  - question count/progress
- AI interviewer panel:
  - current question
  - strict mode label
  - follow-up likely / expected signal
- Candidate video mock tile:
  - static fake video area
  - mock recording badge
  - no real permissions
- Transcript panel:
  - sample live transcript lines
  - clearly mocked
- Response workspace:
  - text/code-style static area if useful
  - no Monaco, no execution
- Communication signals rail:
  - face in frame
  - lighting quality
  - eye contact proxy
  - posture stability
  - speaking pace
  - filler words
  - answer structure
- Bottom control bar:
  - static mute/video/notes/pause/settings controls
  - no real behavior

## Safety Requirements

- Include safe disclaimer:

```txt
Observable communication signals only - no emotion or true-confidence detection.
```

- Do not request browser camera or microphone permissions.
- Do not add real recording, TTS, transcription, or evaluation.

## Data Requirements

- Use centralized mock data from `frontend/src/lib/demo/mock-data.ts`.
- If more interview-room demo content is needed, add it to centralized mock data/types.
- Do not hardcode core interview data directly inside the page component.

## Acceptance Criteria

- [ ] `/demo/interview` feels like a complete product preview while remaining static/mock.
- [ ] `/demo` better explains the setup-to-report workflow if the optional setup preview is implemented.
- [ ] No real API calls happen.
- [ ] No camera or microphone access is requested.
- [ ] Existing real `/setup` flow continues to work.
- [ ] No backend files are modified.
- [ ] No unsupported claims appear.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- Keep this task demo-only.
- The interview room can look realistic, but every recording, signal, transcript, and control must be clearly static/mock.
- Use safe wording: observable communication signals, eye contact proxy, speaking pace, filler words, answer structure.
