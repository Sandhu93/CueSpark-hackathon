# Task 052 — Realtime, Video, and Editor Future Scope

## Status

Future scope. Do not implement in the initial build.

## Realtime Voice

Future version may use realtime voice conversation. This should be a separate mode from turn-based interview.

Do not modify the turn-based state machine to fake realtime behavior.

## Video Analysis

Future version may analyze visual communication signals, but must not claim reliable emotion or truth detection.

Allowed wording:

```text
visual communication signals
```

Avoid wording:

```text
true confidence detection
emotion detection
lie detection
```

## Monaco Editor / Code Execution

Future version may add role-specific workspaces:

- coding editor
- pseudo-code answer box
- storyboard/design prompt
- case-study workspace

This should be implemented as an answer workspace type, not as a separate product.
