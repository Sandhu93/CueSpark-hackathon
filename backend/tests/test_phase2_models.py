from __future__ import annotations

from pgvector.sqlalchemy import Vector
from sqlalchemy import inspect

from app.models.answer import CandidateAnswer
from app.models.embedding_chunk import EMBEDDING_DIMENSIONS, ChunkType, EmbeddingChunk
from app.models.evaluation import AnswerEvaluation
from app.models.question import InterviewQuestion, QuestionCategory, QuestionSource
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


def test_hiring_recommendation_enum_covers_contract_values():
    expected = {"strong_yes", "yes", "maybe", "no"}
    assert {e.value for e in HiringRecommendation} == expected


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
    ):
        assert name in table_names, f"Table '{name}' not registered on Base.metadata"
