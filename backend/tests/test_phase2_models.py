from __future__ import annotations

from pgvector.sqlalchemy import Vector
from sqlalchemy import inspect

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
    expected = {"base_plan", "adaptive_followup", "benchmark_gap"}
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
    expected = {"strong_yes", "yes", "maybe", "no"}
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
