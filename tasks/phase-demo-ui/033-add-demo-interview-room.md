# Task: Add Demo Interview Room

## Goal

Build a polished mock-data interview room that shows how CueSpark converts benchmark gaps into a realistic interview experience.

This is a frontend-only hackathon demo screen.

## Scope

Implement only:

- `/demo/interview` route
- AI interviewer panel
- Candidate video mock tile
- Current benchmark-driven question
- Why this question was asked
- Benchmark gap references
- Mock recording state
- Mock answer transcript
- Safe video/audio signal panel
- Navigation to demo report

## Out of Scope

Do not implement:

- Real camera access
- Real microphone recording
- Real TTS playback
- Real transcription
- Real evaluation
- Backend changes
- WebRTC
- Emotion detection
- True confidence detection

## Files Likely Involved

- `frontend/src/app/demo/interview/page.tsx`
- `frontend/src/components/demo/`
- `frontend/src/lib/demo/mock-data.ts`

## UI Requirements

The interview room should include:

1. AI Interviewer Panel
   - question text
   - question category
   - difficulty
   - expected signal

2. Candidate Video Mock
   - visual video tile
   - mock recording badge
   - mock answer waveform

3. Why This Was Asked
   - explain benchmark gap behind the question

4. Communication Signals Panel
   - face in frame
   - lighting quality
   - eye contact proxy
   - posture stability
   - speaking pace
   - filler words
   - answer structure

Safe disclaimer:

```txt
Observable communication signals only — no emotion or true-confidence detection.
```

## Acceptance Criteria

- [ ] `/demo/interview` page exists.
- [ ] Uses centralized mock data.
- [ ] Clearly labels itself as Demo Preview / Mock Data Mode.
- [ ] Shows AI interviewer, candidate video mock, and signal panel.
- [ ] Shows why the question was asked.
- [ ] Shows benchmark gap references.
- [ ] Uses safe communication-signal language.
- [ ] Has CTA to `/demo/report`.
- [ ] No real camera/microphone access is requested.
- [ ] No real API calls happen.

## Verification

Run:

```bash
cd frontend
npm run lint
npm run build
```

## Notes for Codex

- This screen is for presentation, not production functionality.
- Make it feel like a complete product without pretending the backend interview loop is complete.
