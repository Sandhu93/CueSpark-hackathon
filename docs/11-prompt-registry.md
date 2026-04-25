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
- normalized role key
- seniority level
- match score
- matched skills
- missing skills
- risk areas
- interview focus areas

## `BENCHMARK_ANALYSIS_V1`

Input:

- job description
- resume text
- match analysis
- retrieved benchmark profiles

Output:

- benchmark similarity score
- resume competitiveness score
- evidence strength score
- missing skills
- weak skills
- missing metrics
- weak ownership signals
- interview risk areas
- recommended resume fixes
- question targets

## `QUESTION_GENERATION_V1`

Input:

- JD summary
- resume summary
- match analysis
- benchmark comparison
- benchmark gap question targets

Output:

- 10 questions
- category
- difficulty
- expected signal
- reason for asking
- source: `jd | resume | benchmark_gap | mixed`
- benchmark gap references where applicable
- why this question was asked

At least 4 questions should be directly tied to benchmark gaps when benchmark data exists.

## `ANSWER_EVALUATION_V1`

Input:

- question
- expected signal
- JD context
- resume context
- benchmark gap being tested
- answer transcript
- communication metrics

Output:

- scores
- strengths
- weaknesses
- benchmark gap coverage
- strict feedback
- improved answer

## `FINAL_REPORT_V1`

Input:

- match analysis
- benchmark comparison
- questions
- answer evaluations

Output:

- readiness score
- hiring recommendation
- overall summary
- benchmark similarity score
- resume competitiveness score
- evidence strength score
- benchmark gaps
- interview risk areas
- answer feedback
- resume feedback
- preparation plan

## Rules

- Do not scatter prompts across service files.
- Do not place large prompts inside FastAPI route handlers.
- Do not place prompts inside React components.
- All LLM outputs must map to typed Pydantic schemas.
- Version prompts when their output contract changes.
- Do not generate generic interview questions when benchmark gaps are available.
- Do not claim benchmark profiles are verified hired-candidate resumes unless the source data proves it.
