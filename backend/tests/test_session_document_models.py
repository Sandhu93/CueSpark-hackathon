from app.core.db import Base
from app.models.document import DocumentParseStatus, DocumentType
from app.models.session import InterviewSessionStatus
from app.schemas.document import DocumentCreate
from app.schemas.session import SessionCreate


def test_session_and_document_tables_are_registered():
    assert "interview_sessions" in Base.metadata.tables
    assert "documents" in Base.metadata.tables


def test_session_status_supports_documented_lifecycle():
    assert {status.value for status in InterviewSessionStatus} == {
        "draft",
        "preparing",
        "ready",
        "in_progress",
        "evaluating",
        "report_ready",
        "completed",
        "failed",
    }


def test_document_parse_status_supports_required_values():
    assert {status.value for status in DocumentParseStatus} == {
        "pending",
        "parsed",
        "failed",
        "ocr_required",
    }


def test_create_schemas_accept_foundation_inputs():
    session = SessionCreate(job_description="Build APIs", resume_text=None)
    document = DocumentCreate(
        session_id="session-id",
        document_type=DocumentType.RESUME,
        input_type="paste",
        extracted_text="Resume text",
    )

    assert session.job_description == "Build APIs"
    assert document.parse_status == DocumentParseStatus.PENDING
