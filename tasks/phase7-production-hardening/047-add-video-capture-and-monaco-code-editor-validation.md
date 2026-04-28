# Task: Add Video Capture MVP and Monaco Code Editor Validation

## Goal

Add two production-interview-room capabilities that are needed to properly validate CueSpark's multimodal interview flow:

```txt
1. Video/visual-signal capture MVP
2. Monaco-based code answer editor
```

This task should make the real `/session/[sessionId]/interview` route capable of testing visual-presence signals and realistic code-answer input in local/mock mode.

## Why This Task Exists

CueSpark claims multimodal interview evaluation. The mock-mode interview now supports multiple response modes, but two areas still need proper production UI validation:

- `requires_video=true` currently only shows a placeholder. We need a safe camera/video capture MVP to test visual-signal metadata flow.
- Code answers currently use a plain textarea. We need Monaco editor so coding questions feel realistic and can be validated properly.

This is still an MVP. Do not build a full proctoring system, full video recording platform, or online judge.

## Product Boundaries

Allowed:

- Request camera permission only when the candidate explicitly clicks a button.
- Show local camera preview inside the interview room.
- Capture safe visual-presence metadata.
- Optionally capture a small still-frame/sample locally for analysis/preview if needed.
- Submit visual signal metadata with the answer payload.
- Use Monaco editor for code/pseudocode entry.
- Keep static code evaluation only.

Not allowed:

- Emotion detection.
- True confidence detection.
- Personality scoring.
- Truthfulness detection.
- Face recognition or identity verification.
- Liveness detection.
- Continuous surveillance.
- Full WebRTC meeting.
- Uploading/storing full video files in this task.
- Executing arbitrary code.
- Major interview-room redesign.

## Scope

### 1. Video / Visual Signal Capture MVP

Implement a small production component, for example:

```txt
frontend/src/components/interview/VisualSignalCapture.tsx
frontend/src/hooks/useVideoPreview.ts
```

The component should:

- Render only when `requires_video=true`.
- Show a clear safe-label/disclaimer.
- Have a `Start camera` button.
- Request camera permission only after the user clicks `Start camera`.
- Show local video preview.
- Have a `Stop camera` button.
- Compute or collect safe visual-presence metadata.
- Pass visual metadata into answer submission for supported answer modes.

Recommended MVP metadata:

```json
{
  "camera_presence": "stable",
  "lighting_quality": "good | moderate | poor",
  "face_in_frame_ratio": null,
  "eye_contact_proxy": "not_measured | low | moderate | high",
  "posture_stability": "not_measured | unstable | moderate | steady",
  "distraction_markers": []
}
```

Implementation note:

- It is acceptable for `face_in_frame_ratio`, `eye_contact_proxy`, and `posture_stability` to be `not_measured` or manually/mock selected in this task.
- If computing lighting quality is simple, use a small canvas sample from the local video frame to estimate brightness.
- Do not introduce heavy computer-vision dependencies unless explicitly justified and approved.

### 2. Visual Metadata Submission

Ensure `visual_signal_metadata` is submitted with answers when available:

- spoken answer with video metadata
- written answer with video metadata if required
- code answer with video metadata if required
- mixed answer with video metadata if required

If unified mixed-answer capture has not been implemented yet, keep changes minimal and do not build a large mixed-flow redesign here.

### 3. Monaco Code Editor

Replace the plain code textarea in `CodeAnswerCapture` with Monaco editor.

Recommended dependency:

```txt
@monaco-editor/react
monaco-editor
```

Implementation requirements:

- Load Monaco client-side only.
- Use dynamic import or the library's SSR-safe pattern for Next.js.
- Keep a simple fallback/loading state.
- Keep existing language selector.
- Map supported languages to Monaco language IDs where possible.
- Preserve the existing `api.submitCodeAnswer` flow.
- Preserve explanation textarea.
- Do not execute code.

## Out of Scope

Do not implement:

- Full video file upload/storage.
- Audio/video synchronization.
- WebRTC.
- AI-based facial emotion analysis.
- Face recognition.
- Liveness detection.
- Monaco test runner.
- Sandboxed code execution.
- Major layout redesign.
- Report UI redesign.

## Files Likely Involved

Frontend:

```txt
frontend/package.json
frontend/src/components/interview/VisualSignalCapture.tsx
frontend/src/hooks/useVideoPreview.ts
frontend/src/components/interview/CodeAnswerCapture.tsx
frontend/src/components/interview/SpokenAnswerCapture.tsx
frontend/src/components/interview/WrittenAnswerCapture.tsx
frontend/src/app/session/[sessionId]/interview/page.tsx
frontend/src/lib/types.ts
```

Backend only if a clear contract bug is found:

```txt
backend/app/api/answers.py
backend/app/schemas/answer.py
backend/tests/test_answer_submission_api.py
```

Prefer no backend changes unless the existing `visual_signal_metadata` handling is insufficient.

## UX Requirements

### Video/Visual Panel Copy

Use safe wording:

```txt
Visual presence signals
Camera preview is processed only for observable interview-presence metadata. CueSpark does not detect emotion, personality, truthfulness, or true confidence.
```

### Camera States

Support:

```txt
idle
requesting_permission
active
stopped
permission_denied
not_supported
error
```

### Monaco States

Support:

```txt
loading editor
editor ready
editor failed / fallback textarea
```

## Acceptance Criteria

- [ ] `requires_video=true` questions show a real camera-preview capture panel, not only a placeholder.
- [ ] Camera permission is requested only after user action.
- [ ] User can start and stop camera preview.
- [ ] Visual metadata can be produced and passed into answer submission where available.
- [ ] No full video file is uploaded or stored.
- [ ] No unsafe claims are added.
- [ ] Code answer UI uses Monaco editor or a safe Monaco loading/fallback path.
- [ ] Existing code answer submission still works.
- [ ] Written/spoken answer submission still works.
- [ ] Frontend build succeeds.
- [ ] Backend tests still pass if backend is touched.

## Verification

Run:

```bash
npm.cmd --prefix frontend install
npm.cmd --prefix frontend run build
```

If backend touched:

```bash
docker compose exec api pytest backend/tests/test_answer_submission_api.py -q
docker compose exec api pytest -q
```

Manual browser validation:

1. Start a fresh session with `AI_MOCK_MODE=true`.
2. Prepare the session.
3. Open the interview room.
4. Navigate to a question with `requires_video=true`.
5. Click `Start camera`.
6. Confirm browser asks for camera permission.
7. Confirm local preview appears after permission.
8. Confirm safe visual metadata appears or can be selected.
9. Stop camera.
10. Submit the answer and confirm visual metadata does not break answer processing.
11. Navigate to a code question.
12. Confirm Monaco editor loads.
13. Write code and submit.
14. Confirm answer processing/report generation still works.

## Notes for Codex

- This task is about validating multimodal capture, not redesigning the full interview room.
- Keep video privacy conservative.
- Do not store full video.
- Do not execute code.
- Do not add unsafe claims.
- If Monaco causes build issues, implement a documented fallback textarea rather than breaking the product.
