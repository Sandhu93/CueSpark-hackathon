# Task: Add Curated Benchmark Fixtures

## Goal

Add curated/anonymized benchmark profile fixtures for the hackathon demo.

## Scope

Implement only:

- Fixture files for benchmark profiles.
- At least 3 demo role keys.
- 5 benchmark profiles per demo role.
- Clear fixture format that can be seeded into Postgres later.

## Out of Scope

Do not implement:

- Live internet scraping.
- LinkedIn/Naukri scraping.
- Claims that profiles are real selected resumes.
- Embedding generation.
- Candidate comparison logic.
- Frontend UI.

## Files Likely Involved

- `fixtures/benchmarks/`
- `docs/13-benchmark-engine-design.md` if minor clarification is needed

## Recommended Demo Roles

```txt
project_manager
backend_developer
data_analyst
```

Each role should have:

```txt
1. Strong fresher / entry-level profile
2. Strong 2-3 year profile
3. Strong experienced profile
4. Domain-switcher profile
5. High-impact portfolio profile
```

## Fixture Format

Use JSON or YAML. JSON is preferred for easy loading.

Each profile should include:

```json
{
  "role_key": "project_manager",
  "role_title": "Project Manager",
  "seniority_level": "mid",
  "domain": "software_delivery",
  "profile_name": "PM Benchmark 01",
  "resume_text": "...",
  "skills": [],
  "tools": [],
  "project_signals": [],
  "impact_signals": [],
  "ownership_signals": [],
  "source_type": "curated",
  "source_url": null,
  "is_curated": true,
  "quality_score": 85
}
```

## Acceptance Criteria

- [ ] Benchmark fixtures exist for at least 3 role keys.
- [ ] Each role has 5 profiles.
- [ ] Profiles are anonymized/curated.
- [ ] Fixtures include skills, tools, impact signals, and ownership signals.
- [ ] No live scraping code is added.
- [ ] No real personal data is included.

## Verification

Run a JSON validation command if JSON is used:

```bash
python -m json.tool fixtures/benchmarks/project_manager.json > /dev/null
```

Repeat for each fixture file.

## Notes for Codex

- Make profiles realistic but synthetic/curated.
- Do not copy real resumes verbatim.
