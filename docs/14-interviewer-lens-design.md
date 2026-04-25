# Interviewer Lens Design

## Purpose

Interviewer Lens is an optional personalization layer for CueSpark.

The benchmark engine answers:

```txt
How does the candidate compare against the role benchmark?
```

Interviewer Lens answers:

```txt
Given the interviewer context provided by the candidate, what is this interviewer likely to probe?
```

Together:

```txt
JD + Resume + Benchmark Gaps + Interviewer Lens -> More realistic interview questions
```

## Important Safety Rule

Do not scrape LinkedIn.

The first version supports only:

- user-uploaded LinkedIn-exported PDF
- pasted interviewer profile text
- recruiter notes pasted by the candidate
- public bio text pasted by the candidate

Use safe wording:

```txt
user-provided interviewer context
interviewer lens
likely focus areas
question strategy
```

Avoid unsafe/overclaiming wording:

```txt
we scrape LinkedIn
we know exactly what they will ask
we profile the interviewer
we predict exact questions
```

## Output

The analysis should produce:

```json
{
  "interviewer_name": "string | null",
  "interviewer_title": "string | null",
  "company": "string | null",
  "seniority_signal": "string | null",
  "domain_signals": [],
  "technical_focus_areas": [],
  "leadership_focus_areas": [],
  "likely_interview_style": "string",
  "likely_question_bias": [],
  "candidate_risk_from_interviewer_lens": [],
  "question_strategy": []
}
```

## How It Is Used

Question generation should use Interviewer Lens as secondary personalization.

Priority order:

1. JD requirements
2. Candidate resume gaps
3. Benchmark comparison gaps
4. Interviewer Lens focus areas

Interviewer Lens must not override the benchmark engine. It should sharpen the questions, not replace the core gap-driven logic.

## Out of Scope

- LinkedIn scraping
- automatic login to LinkedIn
- bypassing access restrictions
- storing third-party personal data permanently without user consent
- claiming exact question prediction
- judging the interviewer personally
