from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import text

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database_url, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

_POSTGRES_SCHEMA_COMPAT_STATEMENTS = (
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS response_mode VARCHAR DEFAULT 'spoken_answer'
    """,
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS requires_audio BOOLEAN DEFAULT true
    """,
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS requires_video BOOLEAN DEFAULT false
    """,
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS requires_text BOOLEAN DEFAULT false
    """,
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS requires_code BOOLEAN DEFAULT false
    """,
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS tts_object_key VARCHAR
    """,
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS provenance JSONB DEFAULT '{}'::jsonb
    """,
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS tts_status VARCHAR
    """,
    """
    ALTER TABLE IF EXISTS interview_questions
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS answer_mode VARCHAR DEFAULT 'spoken_answer'
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS text_answer TEXT
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS code_answer TEXT
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS code_language VARCHAR
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS transcription_status VARCHAR DEFAULT 'pending'
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS processing_status VARCHAR DEFAULT 'pending'
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS communication_metadata JSONB DEFAULT '{}'::jsonb
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS visual_signal_metadata JSONB DEFAULT '{}'::jsonb
    """,
    """
    ALTER TABLE IF EXISTS candidate_answers
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE IF EXISTS benchmark_profiles
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE IF EXISTS benchmark_comparisons
    ADD COLUMN IF NOT EXISTS missing_project_depth JSONB DEFAULT '[]'::jsonb
    """,
    """
    ALTER TABLE IF EXISTS benchmark_comparisons
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS structure_score INTEGER
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS jd_alignment_score INTEGER
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS benchmark_gap_coverage_score INTEGER
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS communication_score INTEGER
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS communication_signal_score INTEGER
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS code_quality_score INTEGER
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS written_answer_score INTEGER
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS visual_signal_score INTEGER
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS red_flags JSONB DEFAULT '[]'::jsonb
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS modality_breakdown JSONB DEFAULT '{}'::jsonb
    """,
    """
    ALTER TABLE IF EXISTS answer_evaluations
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS jd_resume_match_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS benchmark_gap_coverage_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS audio_communication_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS communication_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS visual_signal_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS written_answer_quality_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS written_answer_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS code_answer_quality_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS code_answer_summary TEXT
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS multimodal_summary JSONB DEFAULT '{}'::jsonb
    """,
    """
    ALTER TABLE IF EXISTS interview_reports
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    """,
)


async def init_db() -> None:
    # Import models so they register on Base.metadata
    import app.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
        await apply_postgres_schema_compat(conn)


async def apply_postgres_schema_compat(conn: AsyncConnection) -> None:
    if conn.dialect.name != "postgresql":
        return

    for statement in _POSTGRES_SCHEMA_COMPAT_STATEMENTS:
        await conn.execute(text(statement))


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
