"""Benchmark-driven interview question generation service."""
from __future__ import annotations

import json
import re
import uuid

from loguru import logger
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.question import InterviewQuestion, QuestionCategory, QuestionSource
from app.schemas.benchmark import BenchmarkAnalysisResult
from app.schemas.match import MatchAnalysisResult
from app.schemas.question import GeneratedQuestion
from app.services import llm
from app.services.prompts import QUESTION_GENERATION_V1

_FALLBACK_GAP = "core role competency"


def _select_gap(candidate_groups: list[list[str]], used: set[str]) -> str:
    for group in candidate_groups:
        for value in group:
            gap = value.strip()
            if not gap:
                continue
            key = gap.casefold()
            if key not in used:
                used.add(key)
                return gap
    return _FALLBACK_GAP


def _benchmark_gap_questions(benchmark_result: BenchmarkAnalysisResult) -> list[GeneratedQuestion]:
    """Build 4 priority-ordered benchmark gap questions."""
    used: set[str] = set()
    high_risk_gap = _select_gap([benchmark_result.interview_risk_areas], used)
    metrics_gap = _select_gap(
        [benchmark_result.missing_metrics, benchmark_result.question_targets],
        used,
    )
    ownership_gap = _select_gap([benchmark_result.weak_ownership_signals], used)
    skill_gap = _select_gap(
        [
            benchmark_result.question_targets,
            benchmark_result.missing_skills,
            benchmark_result.weak_skills,
        ],
        used,
    )

    configs = [
        (
            high_risk_gap,
            "You have limited evidence of {gap}. Describe a specific situation where you directly "
            "addressed this and what the measurable outcome was.",
            "Concrete evidence resolving identified interview risk area: {gap}",
        ),
        (
            metrics_gap,
            "Your background lacks evidence of {gap}. Quantify your most comparable achievement "
            "with real numbers.",
            "Quantified impact evidence for missing metric: {gap}",
        ),
        (
            ownership_gap,
            "Top performers in this role show {gap}. Provide a specific example from your "
            "experience that demonstrates this directly.",
            "Strong ownership signal: {gap}",
        ),
        (
            skill_gap,
            "Walk me through hands-on experience with {gap}. Give a specific, measurable example "
            "of impact.",
            "Demonstrated proficiency and evidence of impact for benchmark skill target: {gap}",
        ),
    ]

    return [
        GeneratedQuestion(
            question_number=0,
            category=QuestionCategory.BENCHMARK_GAP_VALIDATION.value,
            question_text=text_template.format(gap=gap),
            expected_signal=signal_template.format(gap=gap),
            difficulty="hard",
            source=QuestionSource.BENCHMARK_GAP.value,
            benchmark_gap_refs=[gap],
            why_this_was_asked=f"Benchmark gap: {gap}",
        )
        for gap, text_template, signal_template in configs
    ]


_BASE_PLAN_SPECS: list[dict] = [
    dict(
        category=QuestionCategory.PROJECT_EXPERIENCE.value,
        question_text="Walk me through a project where you had end-to-end ownership from "
        "scoping to delivery. What trade-offs did you make?",
        expected_signal="Clear ownership, decision-making, handling trade-offs under constraint",
        difficulty="hard",
        why_this_was_asked="JD requirement: demonstrated ownership and delivery track record",
    ),
    dict(
        category=QuestionCategory.JD_SKILL_VALIDATION.value,
        question_text="What is the most technically complex problem you have solved in this "
        "role domain? Walk me through your approach.",
        expected_signal="Depth of technical expertise relevant to the role",
        difficulty="hard",
        why_this_was_asked="JD requirement: technical depth validation",
    ),
    dict(
        category=QuestionCategory.JD_SKILL_VALIDATION.value,
        question_text="Describe how you have collaborated with cross-functional stakeholders "
        "to deliver a complex initiative.",
        expected_signal="Evidence of stakeholder management and influence without direct authority",
        difficulty="medium",
        why_this_was_asked="JD requirement: cross-functional collaboration",
    ),
    dict(
        category=QuestionCategory.RESUME_GAP.value,
        question_text="Your resume lists achievements without specific numbers. Pick one role "
        "and give me the quantified outcomes.",
        expected_signal="Measurable outcomes: revenue, cost, time, quality metrics",
        difficulty="medium",
        why_this_was_asked="Resume gap: absence of quantified outcomes",
    ),
    dict(
        category=QuestionCategory.TECHNICAL.value,
        question_text="Describe a time you had to make a significant technical decision under "
        "uncertainty. How did you decide, and what happened?",
        expected_signal="Structured decision-making, risk assessment, ownership of outcome",
        difficulty="hard",
        why_this_was_asked="JD requirement: technical leadership and judgment",
    ),
    dict(
        category=QuestionCategory.BEHAVIORAL.value,
        question_text="Tell me about a time you had to push back on a stakeholder's request. "
        "How did you handle it?",
        expected_signal="Principled disagreement, constructive communication, positive resolution",
        difficulty="medium",
        why_this_was_asked="Behavioral: conflict resolution under pressure",
    ),
    dict(
        category=QuestionCategory.BEHAVIORAL.value,
        question_text="Describe a situation where you had to deliver under tight deadlines with "
        "limited resources.",
        expected_signal="Prioritization, scope management, delivery under constraint",
        difficulty="medium",
        why_this_was_asked="Behavioral: delivery pressure and resilience",
    ),
    dict(
        category=QuestionCategory.TECHNICAL.value,
        question_text="How have you ensured quality and reliability in your deliverables in your "
        "most recent role?",
        expected_signal="Process discipline, measurement, continuous improvement",
        difficulty="medium",
        why_this_was_asked="JD requirement: quality and reliability standards",
    ),
    dict(
        category=QuestionCategory.HR.value,
        question_text="What is the biggest professional growth area you are targeting in the "
        "next 12 months?",
        expected_signal="Self-awareness, alignment to role requirements, growth mindset",
        difficulty="easy",
        why_this_was_asked="HR: growth mindset and role fit assessment",
    ),
    dict(
        category=QuestionCategory.HR.value,
        question_text="Why are you interested in this specific role at this stage of your career?",
        expected_signal="Clear motivation, understanding of role requirements, genuine interest",
        difficulty="easy",
        why_this_was_asked="HR: motivation and role alignment",
    ),
]


def _mock_questions(
    match_result: MatchAnalysisResult,
    benchmark_result: BenchmarkAnalysisResult | None,
) -> list[GeneratedQuestion]:
    if benchmark_result is not None:
        benchmark_qs = _benchmark_gap_questions(benchmark_result)
        base_qs = [
            GeneratedQuestion(
                question_number=0,
                source=QuestionSource.BASE_PLAN.value,
                **spec,
            )
            for spec in _BASE_PLAN_SPECS[:6]
        ]
        all_qs = benchmark_qs + base_qs
    else:
        all_qs = [
            GeneratedQuestion(
                question_number=0,
                source=QuestionSource.BASE_PLAN.value,
                **spec,
            )
            for spec in _BASE_PLAN_SPECS[:10]
        ]

    for index, question in enumerate(all_qs, 1):
        question.question_number = index

    return all_qs[:10]


def _parse_questions(raw: str) -> list[dict]:
    """Extract the questions array from an LLM response containing {"questions": [...]}."""
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM response: {raw[:200]!r}")
    data = json.loads(match.group())
    if "questions" not in data:
        raise ValueError(
            f"LLM response missing 'questions' key; found: {list(data.keys())}"
        )
    questions = data["questions"]
    if not isinstance(questions, list):
        raise ValueError(f"'questions' must be a list, got {type(questions).__name__}")
    return questions


def _format_benchmark_section(benchmark_result: BenchmarkAnalysisResult | None) -> str:
    if benchmark_result is None:
        return "No benchmark comparison data available."
    lines: list[str] = []
    if benchmark_result.interview_risk_areas:
        lines.append(f"High-risk areas: {'; '.join(benchmark_result.interview_risk_areas)}")
    if benchmark_result.missing_skills:
        lines.append(f"Missing skills: {', '.join(benchmark_result.missing_skills)}")
    if benchmark_result.weak_skills:
        lines.append(f"Weak skills: {', '.join(benchmark_result.weak_skills)}")
    if benchmark_result.missing_metrics:
        lines.append(f"Missing metrics evidence: {'; '.join(benchmark_result.missing_metrics)}")
    if benchmark_result.weak_ownership_signals:
        lines.append(
            f"Weak ownership signals: {'; '.join(benchmark_result.weak_ownership_signals)}"
        )
    if benchmark_result.question_targets:
        lines.append(f"Question targets: {'; '.join(benchmark_result.question_targets)}")
    if benchmark_result.recommended_resume_fixes:
        lines.append(
            f"Resume fixes to probe: {'; '.join(benchmark_result.recommended_resume_fixes)}"
        )
    lines.append(
        f"Benchmark similarity: {benchmark_result.benchmark_similarity_score}/100  "
        f"Evidence strength: {benchmark_result.evidence_strength_score}/100"
    )
    return "\n".join(lines)


def _persist_questions(
    db: Session,
    session_id: str,
    questions: list[GeneratedQuestion],
) -> None:
    for question in questions:
        row = InterviewQuestion(
            id=str(uuid.uuid4()),
            session_id=session_id,
            question_number=question.question_number,
            category=question.category,
            question_text=question.question_text,
            expected_signal=question.expected_signal,
            difficulty=question.difficulty,
            source=question.source,
            benchmark_gap_refs=question.benchmark_gap_refs,
            why_this_was_asked=question.why_this_was_asked,
            response_mode=question.response_mode.value,
            requires_audio=question.requires_audio,
            requires_video=question.requires_video,
            requires_text=question.requires_text,
            requires_code=question.requires_code,
        )
        db.add(row)
    logger.info(
        "question_generator: persisted {} questions for session_id={}",
        len(questions),
        session_id,
    )


def generate_interview_questions(
    jd_text: str,
    resume_text: str,
    match_result: MatchAnalysisResult,
    benchmark_result: BenchmarkAnalysisResult | None,
    *,
    session_id: str,
    db: Session,
) -> list[GeneratedQuestion]:
    """Generate and persist a 10-question interview plan."""
    if settings.ai_mock_mode or not settings.openai_api_key:
        logger.info("question_generator: mock mode - returning placeholder questions")
        questions = _mock_questions(match_result, benchmark_result)
    else:
        benchmark_section = _format_benchmark_section(benchmark_result)
        prompt = QUESTION_GENERATION_V1.format(
            jd_text=jd_text,
            resume_text=resume_text,
            role_title=match_result.role_title,
            seniority_level=match_result.seniority_level,
            match_score=match_result.match_score,
            missing_skills=", ".join(match_result.missing_skills) or "none identified",
            risk_areas="; ".join(match_result.risk_areas) or "none identified",
            interview_focus_areas="; ".join(match_result.interview_focus_areas) or "general",
            benchmark_section=benchmark_section,
        )
        try:
            raw = llm.chat(
                messages=[{"role": "user", "content": prompt}],
                model=settings.openai_chat_model,
            )
            question_dicts = _parse_questions(raw)
            questions = [GeneratedQuestion(**data) for data in question_dicts]
            if len(questions) != 10:
                raise ValueError(f"Expected 10 questions, got {len(questions)}")
            logger.info(
                "question_generator: LLM generated {} questions for session_id={}",
                len(questions),
                session_id,
            )
        except Exception as exc:
            logger.warning(
                "question_generator: falling back after LLM parse failure: {}",
                exc,
            )
            questions = _mock_questions(match_result, benchmark_result)

    _persist_questions(db, session_id, questions)
    return questions
