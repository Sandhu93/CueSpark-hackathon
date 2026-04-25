# Benchmark Engine Design

## Purpose

The benchmark engine is the novelty layer of CueSpark Interview Coach.

Instead of only comparing a candidate resume to a job description, CueSpark compares the candidate against a role-specific benchmark set of stronger candidate profiles. The system identifies what stronger profiles show that the candidate does not: measurable impact, role-specific evidence, ownership signals, tools, project depth, and interview risk areas.

## New Product Positioning

CueSpark is a benchmark-driven AI interview preparation platform.

Instead of simply asking generic mock interview questions, CueSpark compares a candidate's resume against the job description and a role-specific benchmark set of strong public profiles or curated top-candidate archetypes.

It identifies what stronger candidates show that this candidate does not: measurable impact, role-specific evidence, ownership signals, skills, tools, and project depth.

Then it generates a strict interviewer-style mock interview focused on those gaps and produces a readiness report showing how far the candidate is from the benchmark.

## Why This Matters

A normal LLM prompt can generate interview questions from a JD and resume. The benchmark engine adds market-relative comparison:

```txt
Candidate Resume ↔ Job Description ↔ Benchmark Profiles ↔ Interview Performance
```

This makes the output more specific and defensible:

- The system can say what the candidate is missing compared to stronger profiles.
- Questions can target evidence gaps, not generic topics.
- Reports can explain readiness relative to a benchmark, not just an AI opinion.

## Hackathon Version

For the hackathon, do not live-scrape personal resumes from the internet.

Use curated/anonymized benchmark fixtures stored in the repository. This avoids privacy, copyright, and data-quality risks while still demonstrating the core idea.

Recommended initial benchmark roles:

```txt
project_manager
backend_developer
data_analyst
```

Each role should have 5 benchmark profiles:

```txt
1. Strong fresher / entry-level profile
2. Strong 2-3 year profile
3. Strong experienced profile
4. Domain-switcher profile
5. High-impact portfolio profile
```

## Later Version

A later version may support public-source retrieval, but it must be source-attributed and legally safe.

Do not claim that scraped resumes are “selected resumes” unless their selection outcome is actually verified.

Prefer this wording:

```txt
benchmark profiles
curated top-candidate archetypes
high-signal public profiles
role benchmark corpus
```

Avoid this wording:

```txt
resumes that got selected
hired candidate resumes
LinkedIn selected resumes
```

## Benchmark Inputs

Each benchmark profile should include:

- role title
- normalized role key
- seniority level
- domain
- resume text
- skills
- tools
- project signals
- measurable impact signals
- ownership signals
- source type
- source URL if public
- whether it is curated
- quality score

## Benchmark Comparison Outputs

The benchmark engine should produce:

```txt
benchmark_similarity_score
resume_competitiveness_score
evidence_strength_score
missing_skills
weak_skills
missing_metrics
weak_ownership_signals
missing_project_depth
interview_risk_areas
benchmark_profile_matches
recommended_resume_fixes
benchmark_driven_question_targets
```

## Evidence Gap Types

Use these gap categories:

```txt
missing_skill
weak_skill_evidence
missing_metric
weak_project_ownership
missing_business_impact
unclear_seniority_signal
missing_tool_depth
weak_domain_alignment
resume_gap_unexplained
communication_risk
```

## Example

Candidate claim:

```txt
Managed backend development for a web application.
```

Benchmark expectation:

```txt
Designed and deployed FastAPI services, improved response time by 35%, owned API design, handled database migrations, and coordinated production release.
```

Detected gaps:

```txt
- missing_metric
- weak_project_ownership
- missing_business_impact
- missing_tool_depth
```

Generated question:

```txt
Your resume mentions backend development, but it does not show scale, ownership, or measurable impact. Describe one backend system you personally designed and explain the most important technical tradeoff you made.
```

## Architecture

```txt
JD + Resume
   ↓
Role Inference
   ↓
Benchmark Retrieval
   ↓
Candidate vs Benchmark Analysis
   ↓
Benchmark Gap Analysis
   ↓
Benchmark-Driven Question Generation
   ↓
Interview + Evaluation
   ↓
Benchmark-Aware Final Report
```

## Storage

Recommended tables:

```txt
benchmark_profiles
benchmark_comparisons
```

Use existing `embedding_chunks` for benchmark chunks with:

```txt
chunk_type = benchmark_profile
owner_type = benchmark_profile
owner_id = benchmark_profiles.id
```

## Report Sections

The final report should include:

```txt
1. Overall readiness score
2. JD-resume match score
3. Benchmark similarity score
4. Resume competitiveness score
5. Evidence strength score
6. Missing benchmark signals
7. Interview risk radar
8. Answer-by-answer performance
9. Resume fixes based on benchmark gaps
10. Preparation plan
```

## Demo Explanation for Judges

Use this explanation:

```txt
A normal AI mock interview can be done with one prompt. CueSpark adds a benchmark layer. It compares the candidate against role-specific strong candidate archetypes, finds what evidence is missing, and then generates the mock interview from those benchmark gaps. The result is not just generic questions, but a market-relative readiness report.
```
