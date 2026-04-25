# Prompt Registry

All prompts must live in:

```txt
backend/app/services/prompts.py
```

No route handler or task should contain large inline prompts.

Each prompt should have:

- prompt name
- version
- purpose
- expected JSON schema
- model used

## Required Prompts

## `MATCH_ANALYSIS_V1`

Input:

- job description
- resume text

Output:

- role title
- seniority level
- match score
- matched skills
- missing skills
- risk areas
- interview focus areas

## `QUESTION_GENERATION_V1`

Input:

- JD summary
- resume summary
- match analysis

Output:

- 10 questions
- category
- difficulty
- expected signal
- reason for asking

## `ANSWER_EVALUATION_V1`

Input:

- question
- expected signal
- JD context
- resume context
- answer transcript
- communication metrics

Output:

- scores
- strengths
- weaknesses
- strict feedback
- improved answer

## `FINAL_REPORT_V1`

Input:

- match analysis
- questions
- answer evaluations

Output:

- readiness score
- hiring recommendation
- overall summary
- skill gaps
- answer feedback
- preparation plan

## Rules

- Do not scatter prompts across service files.
- Do not place large prompts inside FastAPI route handlers.
- Do not place prompts inside React components.
- All LLM outputs must map to typed Pydantic schemas.
- Version prompts when their output contract changes.
