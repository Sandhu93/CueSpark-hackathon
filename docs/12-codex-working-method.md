# Codex Working Method

Use Codex in small, controlled passes.

## Planning Prompt

Use this before code edits:

```txt
Read AGENTS.md, docs/00-project-overview.md, docs/01-architecture.md, docs/08-implementation-sequence.md, and tasks/<phase>/<task>.md.

Do not edit files yet.

Return:
1. Files you need to inspect
2. Files you expect to modify
3. Implementation plan
4. Risks or ambiguities
5. Verification command
```

## Implementation Prompt

Use this when ready to edit:

```txt
Implement only tasks/<phase>/<task>.md.

Rules:
- Do not implement future phases.
- Do not refactor unrelated code.
- Keep route handlers thin.
- Keep AI calls inside service modules.
- Use typed schemas.
- Update tests only where relevant.
- After implementation, report changed files and validation steps.
```

## Review Prompt

Use this after changes:

```txt
Review the changes against the task file only.

Check:
1. Scope creep
2. Broken imports
3. Missing schemas
4. Missing tests
5. Hardcoded secrets
6. Unnecessary libraries
7. Whether acceptance criteria are met

Do not rewrite code unless there is a clear defect.
```

## Token-Saving Rules

Do:

- Read only `AGENTS.md`, selected docs, the selected task file, and files directly related to the task.
- Use repository search instead of opening many files.
- Implement one endpoint or one service at a time.
- Prefer small commits.
- Ask Codex to report changed files every time.

Avoid:

- “Read the entire repo and build the backend.”
- “Improve the architecture.”
- “Make the UI better.”
- “Add missing features.”
- “Refactor as needed.”

These phrases cause scope creep.
