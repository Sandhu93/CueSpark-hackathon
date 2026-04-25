from __future__ import annotations

import json
import re

from loguru import logger

from app.core.config import settings
from app.models.answer import CandidateAnswer
from app.models.question import InterviewQuestion
from app.schemas.agent_results import CodeEvaluationResult
from app.services import llm
from app.services.prompts import CODE_EVALUATION_V1


def analyze_code_answer(
    *,
    question: InterviewQuestion,
    answer: CandidateAnswer,
    sample_test_cases: str | None = None,
) -> CodeEvaluationResult:
    if not answer.code_answer or not answer.code_answer.strip():
        raise ValueError("Candidate answer has no code to analyze")

    gap_refs = [str(gap) for gap in (question.benchmark_gap_refs or []) if str(gap).strip()]

    if settings.ai_mock_mode or not settings.openai_api_key:
        logger.info("code_evaluation_agent: mock mode for answer_id={}", answer.id)
        return _mock_result(
            code_answer=answer.code_answer,
            code_language=answer.code_language,
            explanation=answer.text_answer or answer.transcript,
            gap_refs=gap_refs,
        )

    prompt = CODE_EVALUATION_V1.format(
        question_text=question.question_text,
        expected_signal=question.expected_signal or "No expected signal provided.",
        benchmark_gap_refs="\n".join(f"- {gap}" for gap in gap_refs) or "No benchmark gap refs.",
        code_language=answer.code_language or "unspecified",
        code_answer=answer.code_answer,
        candidate_explanation=answer.text_answer or answer.transcript or "No explanation provided.",
        sample_test_cases=sample_test_cases or "No sample test cases provided.",
    )
    raw = llm.chat(
        messages=[{"role": "user", "content": prompt}],
        model=settings.openai_chat_model,
    )
    data = _parse_json_object(raw)
    return CodeEvaluationResult(**data)


def _mock_result(
    *,
    code_answer: str,
    code_language: str | None,
    explanation: str | None,
    gap_refs: list[str],
) -> CodeEvaluationResult:
    has_function = bool(re.search(r"\b(def|function|class|public|const|let|fn)\b", code_answer))
    has_branch = bool(re.search(r"\b(if|else|switch|case|try|except|catch)\b", code_answer))
    has_loop = bool(re.search(r"\b(for|while|map|reduce)\b", code_answer))
    has_return = "return" in code_answer
    has_tests = bool(re.search(r"\b(assert|test|expect|pytest|unittest)\b", code_answer.lower()))
    line_count = len([line for line in code_answer.splitlines() if line.strip()])
    explanation_words = len(re.findall(r"[A-Za-z0-9']+", explanation or ""))

    correctness = 7 if has_function or has_return else 5
    edge_cases = 7 if has_branch else 5
    complexity = 8 if has_loop or has_branch else 6
    readability = 8 if line_count <= 80 else 6
    testability = 8 if has_tests else 5
    explanation_score = 8 if explanation_words >= 20 else 6 if explanation_words > 0 else 4

    strengths = []
    weaknesses = []
    improvements = []
    if has_function or has_return:
        strengths.append("Provides a concrete implementation structure.")
    else:
        weaknesses.append("Code lacks a clear callable implementation shape.")
        improvements.append("Wrap the solution in a clear function or class with defined inputs and outputs.")
    if has_branch:
        strengths.append("Includes conditional handling for at least one scenario.")
    else:
        weaknesses.append("Edge-case handling is not visible from the static code.")
        improvements.append("Add explicit handling for empty, invalid, or boundary inputs.")
    if has_tests:
        strengths.append("Includes test-oriented evidence.")
    else:
        weaknesses.append("No sample tests or assertions are included.")
        improvements.append("Add representative test cases as text or assertions.")
    if gap_refs:
        strengths.append("Reviewed against benchmark gap references.")

    return CodeEvaluationResult(
        correctness_score=correctness,
        edge_case_score=edge_cases,
        complexity_score=complexity,
        readability_score=readability,
        testability_score=testability,
        explanation_score=explanation_score,
        strengths=strengths,
        weaknesses=weaknesses,
        suggested_improvements=improvements,
        complexity_analysis=_complexity_analysis(code_language, has_loop, line_count),
    )


def _complexity_analysis(code_language: str | None, has_loop: bool, line_count: int) -> str:
    language = code_language or "unspecified language"
    if has_loop:
        return (
            f"Static review only: {language} solution appears to use iteration; explain expected "
            "time and space complexity in the interview answer."
        )
    return (
        f"Static review only: {language} solution is short ({line_count} non-empty lines); "
        "complexity cannot be runtime-verified here."
    )


def _parse_json_object(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in code evaluation response: {raw[:200]!r}")
    return json.loads(match.group())
