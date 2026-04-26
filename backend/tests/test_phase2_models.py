from __future__ import annotations

from pgvector.sqlalchemy import Vector
from sqlalchemy import inspect

from app.core.db import Base
from app.models.agent_result import AgentResult, AgentResultStatus, AgentType
from app.models.answer import CandidateAnswer
from app.models.embedding_chunk import EMBEDDING_DIMENSIONS, ChunkType, EmbeddingChunk
from app.models.evaluation import AnswerEvaluation
from app.models.question import InterviewQuestion, QuestionCategory, QuestionSource, ResponseMode
from app.models.report import HiringRecommendation, InterviewReport


def test_embedding_chunk_vector_column_dimension():
    col = EmbeddingChunk.__table__.c["embedding"]
    assert isinstance(col.type, Vector)
    assert col.type.dim == EMBEDDING_DIMENSIONS


def test_embedding_chunk_session_id_is_nullable():
    col = EmbeddingChunk.__table__.c["session_id"]
    assert col.nullable is True


def test_chunk_type_enum_covers_contract_values():
    expected = {"jd", "resume", "benchmark_profile", "answer", "rubric", "question_bank"}
    assert {e.value for e in ChunkType} == expected


def test_question_category_enum_covers_contract_values():
    expected = {
        "technical",
        "project_experience",
        "behavioral",
        "hr",
        "resume_gap",
        "jd_skill_validation",
        "benchmark_gap_validation",
    }
    assert {e.value for e in QuestionCategory} == expected


def test_question_source_enum_covers_contract_values():
    expected = {"base_plan", "adaptive_followup", "manual", "benchmark_gap"}
    assert {e.value for e in QuestionSource} == expected


def test_response_mode_enum_covers_multimodal_contract_values():
    expected = {"spoken_answer", "written_answer", "code_answer", "mixed_answer"}
    assert {e.value for e in ResponseMode} == expected


def test_question_response_modality_columns_default_to_spoken_flow():
    question = InterviewQuestion(
        session_id="session-1",
        question_number=1,
        category=QuestionCategory.TECHNICAL.value,
        question_text="Explain your approach.",
    )

    assert question.response_mode is None or question.response_mode == ResponseMode.SPOKEN_ANSWER.value
    assert question.requires_audio is None or question.requires_audio is True
    assert question.requires_video is None or question.requires_video is False
    assert question.requires_text is None or question.requires_text is False
    assert question.requires_code is None or question.requires_code is False


def test_answer_model_can_store_multimodal_response_fields():
    answer = CandidateAnswer(
        session_id="session-1",
        question_id="question-1",
        answer_mode=ResponseMode.MIXED_ANSWER.value,
        transcript="Spoken explanation.",
        text_answer="Written explanation.",
        code_answer="print('hello')",
        code_language="python",
        visual_signal_metadata={"face_in_frame_ratio": 0.9},
    )

    assert answer.answer_mode == ResponseMode.MIXED_ANSWER.value
    assert answer.transcript == "Spoken explanation."
    assert answer.text_answer == "Written explanation."
    assert answer.code_answer == "print('hello')"
    assert answer.code_language == "python"
    assert answer.visual_signal_metadata["face_in_frame_ratio"] == 0.9


def test_hiring_recommendation_enum_covers_contract_values():
    expected = {"strong_yes", "yes", "maybe", "no", "strong_no"}
    assert {e.value for e in HiringRecommendation} == expected


def test_agent_result_columns_match_storage_contract():
    columns = AgentResult.__table__.c

    assert columns["answer_id"].foreign_keys
    assert columns["agent_type"].index is True
    assert columns["status"].index is True
    assert columns["score"].nullable is True
    assert columns["payload"].default is not None
    assert columns["error"].nullable is True


def test_interview_report_has_multimodal_summary_columns():
    columns = InterviewReport.__table__.c

    assert "benchmark_gap_coverage_summary" in columns
    assert "audio_communication_summary" in columns
    assert "visual_signal_summary" in columns
    assert "written_answer_quality_summary" in columns
    assert "code_answer_quality_summary" in columns
    assert "multimodal_summary" in columns


def test_models_cover_data_contract_columns():
    expected_columns = {
        "benchmark_profiles": {
            "id",
            "role_key",
            "role_title",
            "seniority_level",
            "domain",
            "profile_name",
            "resume_text",
            "skills",
            "tools",
            "project_signals",
            "impact_signals",
            "ownership_signals",
            "source_type",
            "source_url",
            "is_curated",
            "quality_score",
            "created_at",
            "updated_at",
        },
        "benchmark_comparisons": {
            "id",
            "session_id",
            "role_key",
            "benchmark_profile_ids",
            "benchmark_similarity_score",
            "resume_competitiveness_score",
            "evidence_strength_score",
            "missing_skills",
            "weak_skills",
            "missing_metrics",
            "weak_ownership_signals",
            "missing_project_depth",
            "interview_risk_areas",
            "recommended_resume_fixes",
            "question_targets",
            "created_at",
            "updated_at",
        },
        "interview_questions": {
            "id",
            "session_id",
            "question_number",
            "category",
            "question_text",
            "expected_signal",
            "difficulty",
            "source",
            "benchmark_gap_refs",
            "why_this_was_asked",
            "provenance",
            "response_mode",
            "requires_audio",
            "requires_video",
            "requires_text",
            "requires_code",
            "tts_object_key",
            "tts_status",
            "created_at",
            "updated_at",
        },
        "candidate_answers": {
            "id",
            "session_id",
            "question_id",
            "answer_mode",
            "audio_object_key",
            "transcript",
            "text_answer",
            "code_answer",
            "code_language",
            "transcription_status",
            "processing_status",
            "duration_seconds",
            "word_count",
            "words_per_minute",
            "filler_word_count",
            "communication_metadata",
            "visual_signal_metadata",
            "created_at",
            "updated_at",
        },
        "answer_evaluations": {
            "id",
            "answer_id",
            "relevance_score",
            "role_depth_score",
            "evidence_score",
            "structure_score",
            "jd_alignment_score",
            "benchmark_gap_coverage_score",
            "communication_signal_score",
            "code_quality_score",
            "written_answer_score",
            "visual_signal_score",
            "overall_score",
            "strengths",
            "weaknesses",
            "strict_feedback",
            "improved_answer",
            "red_flags",
            "modality_breakdown",
            "created_at",
            "updated_at",
        },
        "interview_reports": {
            "id",
            "session_id",
            "readiness_score",
            "hiring_recommendation",
            "summary",
            "jd_resume_match_summary",
            "benchmark_similarity_score",
            "resume_competitiveness_score",
            "evidence_strength_score",
            "skill_gaps",
            "benchmark_gaps",
            "interview_risk_areas",
            "answer_feedback",
            "resume_feedback",
            "communication_summary",
            "visual_signal_summary",
            "written_answer_summary",
            "code_answer_summary",
            "improvement_plan",
            "created_at",
            "updated_at",
        },
    }

    for table_name, columns in expected_columns.items():
        model_columns = set(Base.metadata.tables[table_name].c.keys())
        missing = columns - model_columns
        assert not missing, f"{table_name} missing contract columns: {sorted(missing)}"


def test_all_new_tables_registered_on_base():
    from app.core.db import Base
    import app.models  # noqa: F401 — ensure models are imported

    table_names = set(Base.metadata.tables.keys())
    for name in (
        "embedding_chunks",
        "interview_questions",
        "candidate_answers",
        "answer_evaluations",
        "interview_reports",
        "agent_results",
    ):
        assert name in table_names, f"Table '{name}' not registered on Base.metadata"
