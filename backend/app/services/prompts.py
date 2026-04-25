"""Versioned prompt registry. All LLM prompts live here so they can be reviewed
and updated in one place."""
from __future__ import annotations

BENCHMARK_ANALYSIS_V1 = """\
You are a strict technical recruiter comparing a candidate's resume against
curated benchmark profiles for the same role.

Return a JSON object with exactly these fields:
  benchmark_similarity_score     – integer 0-100: how closely the candidate
                                   matches the benchmark standard
  resume_competitiveness_score   – integer 0-100: how competitive this resume
                                   is in the current market for this role
  evidence_strength_score        – integer 0-100: strength of measurable
                                   evidence and quantified impact claims
  missing_skills                 – skills common in benchmarks but absent from
                                   the candidate resume (list of strings)
  weak_skills                    – skills the candidate claims but lacks
                                   concrete evidence for (list of strings)
  missing_metrics                – types of measurable impact not present in
                                   the candidate resume (list of strings)
  weak_ownership_signals         – ownership or leadership signals present in
                                   benchmarks but weak in the candidate
                                   (list of strings)
  interview_risk_areas           – areas an interviewer must probe due to gaps
                                   or inconsistencies (list of strings)
  recommended_resume_fixes       – specific, actionable improvements the
                                   candidate should make to their resume
                                   (list of strings)
  question_targets               – specific interview topics to address based
                                   on the identified gaps (list of strings)

Respond ONLY with valid JSON. No commentary outside the JSON block.
Do not claim benchmark profiles represent real hired candidates.

--- CANDIDATE RESUME ---
{resume_text}

--- BENCHMARK PROFILES (role standard) ---
{benchmark_summaries}
"""

QUESTION_GENERATION_V1 = """\
You are a strict technical interviewer designing an interview plan for a specific candidate.

Generate exactly 10 interview questions using the materials below.

Priority order:
1. High-risk benchmark gaps (interview_risk_areas, missing_metrics, weak_ownership_signals)
2. Missing skills identified in the benchmark comparison
3. JD skill validation
4. Behavioral / HR

When benchmark gap data is provided, AT LEAST 4 questions must directly test those gaps.
Use strict, probing language — do not accept vague or generic answers.
Do not generate questions about things the candidate already demonstrates strongly.

Return a JSON object with a single key "questions" containing an array of exactly 10 objects.
Each object must have:
  question_number      – integer 1-10
  category             – one of: technical, project_experience, behavioral, hr, resume_gap,
                         jd_skill_validation, benchmark_gap_validation
  question_text        – the interview question text (string)
  expected_signal      – what a strong answer would demonstrate (string)
  difficulty           – "easy", "medium", or "hard"
  source               – "benchmark_gap" if tied to a benchmark gap, otherwise "base_plan"
  benchmark_gap_refs   – list of specific gap strings this question tests (empty list if base_plan)
  why_this_was_asked   – one sentence: what prompted this question (JD, benchmark gap, resume gap)

Respond ONLY with valid JSON. No commentary outside the JSON block.

--- JOB DESCRIPTION ---
{jd_text}

--- CANDIDATE RESUME ---
{resume_text}

--- MATCH ANALYSIS ---
Role: {role_title} ({seniority_level})
Match Score: {match_score}/100
Missing Skills: {missing_skills}
Risk Areas: {risk_areas}
Interview Focus: {interview_focus_areas}

--- BENCHMARK COMPARISON GAPS ---
{benchmark_section}
"""

MATCH_ANALYSIS_V1 = """\
You are a strict technical recruiter evaluating candidate fit.

Given the job description and resume below, return a JSON object with exactly
these fields:
  role_title       – the job title as stated in the JD (string)
  role_key         – a normalized snake_case identifier, e.g. "backend_developer",
                     "project_manager", "data_analyst" (string)
  seniority_level  – one of: "junior", "mid", "senior", "lead", "principal",
                     "director" (string)
  match_score      – integer 0-100 representing overall fit
  matched_skills   – list of skills present in both JD and resume (list of strings)
  missing_skills   – list of skills required by JD but absent from resume
                     (list of strings)
  risk_areas       – list of concerns that would worry an interviewer
                     (list of strings)
  interview_focus_areas – list of topics that should be probed during the
                          interview to validate or address gaps (list of strings)

Respond ONLY with valid JSON. No commentary outside the JSON block.

--- JOB DESCRIPTION ---
{jd_text}

--- RESUME ---
{resume_text}
"""
