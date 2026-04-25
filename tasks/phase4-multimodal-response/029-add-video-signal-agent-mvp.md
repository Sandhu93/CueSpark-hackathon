# Task: Add Video Signal Agent MVP

## Goal

Add a safe MVP video-signal analysis layer for interview presence signals.

The first version should avoid storing full video and should avoid unsupported claims such as emotion detection, personality detection, or true confidence detection.

## Scope

Implement only:

- Data model/schema support for video signal summaries.
- `video_signal_agent.py` service with mock mode.
- Accept frontend-provided video signal metadata OR sampled frame metadata if already available.
- Store structured video signal summary linked to candidate answer.
- Safe scoring for visual presence signals.

## Out of Scope

Do not implement:

- Full video recording upload.
- Continuous video streaming.
- WebRTC.
- Emotion detection.
- True confidence detection.
- Personality detection.
- Face recognition or identity verification.
- Liveness detection.
- Final score orchestration.
- Final report.

## Files Likely Involved

- `backend/app/services/video_signal_agent.py`
- `backend/app/schemas/agent_results.py`
- `backend/app/models/answer.py`
- `backend/app/tasks/analyze_video_signals.py`
- `backend/tests/`

## Input

Preferred MVP input:

```json
{
  "face_in_frame_ratio": 0.92,
  "lighting_quality": "good",
  "eye_contact_proxy": "moderate",
  "posture_stability": "steady",
  "camera_presence": "stable",
  "distraction_markers": []
}
```

This can initially be mock/frontend-provided metadata. Real computer vision can be added later.

## Output Schema

Recommended output:

```json
{
  "face_in_frame_score": 9,
  "lighting_score": 8,
  "eye_contact_proxy_score": 6,
  "posture_stability_score": 7,
  "camera_presence_score": 9,
  "visual_signal_score": 8,
  "observations": [],
  "risks": []
}
```

## Safe Language Rules

Use:

```txt
visual signal
face in frame
lighting quality
eye contact proxy
posture stability
camera presence
```

Do not use:

```txt
emotion detection
true confidence detection
personality detection
truthfulness detection
```

## Acceptance Criteria

- [ ] Video signal agent/service exists.
- [ ] Output is structured and typed.
- [ ] Mock mode works without external CV dependencies.
- [ ] Agent stores visual signal summaries linked to the answer.
- [ ] No full video upload or streaming is implemented.
- [ ] No unsupported confidence/emotion/personality claims are made.
- [ ] No final scoring/reporting is implemented here.

## Verification

Run:

```bash
pytest backend/tests
```

Manual check with sample metadata is acceptable.

## Notes for Codex

- This is an MVP signal layer, not a surveillance or identity feature.
- Prefer storing summaries over raw video.
- Keep privacy and safety explicit.
