from __future__ import annotations

from io import BytesIO

from docx import Document as DocxDocument

from app.models.document import DocumentParseStatus
from app.services.document_parser import extract_document_text


def test_extract_txt_document():
    result = extract_document_text(
        b"Backend developer with API ownership and measurable production impact.",
        "resume.txt",
        "text/plain",
    )

    assert result.parse_status == DocumentParseStatus.PARSED
    assert "API ownership" in (result.extracted_text or "")
    assert result.metadata["character_count"] > 30


def test_weak_extraction_marks_ocr_required():
    result = extract_document_text(b"   \n  ", "resume.txt", "text/plain")

    assert result.parse_status == DocumentParseStatus.OCR_REQUIRED
    assert result.extracted_text is None


def test_extract_docx_document():
    document = DocxDocument()
    document.add_paragraph(
        "Project manager with delivery ownership, risk reporting, and stakeholder alignment."
    )
    buffer = BytesIO()
    document.save(buffer)

    result = extract_document_text(
        buffer.getvalue(),
        "resume.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    assert result.parse_status == DocumentParseStatus.PARSED
    assert "stakeholder alignment" in (result.extracted_text or "")


def test_extract_text_pdf_document():
    pdf = _minimal_text_pdf(
        "Data analyst with SQL dashboards and measurable business impact"
    )

    result = extract_document_text(pdf, "resume.pdf", "application/pdf")

    assert result.parse_status == DocumentParseStatus.PARSED
    assert "Data analyst" in (result.extracted_text or "")
    assert result.metadata["page_count"] == 1


def test_failed_extraction_uses_safe_metadata():
    result = extract_document_text(b"not a valid docx", "resume.docx")

    assert result.parse_status == DocumentParseStatus.FAILED
    assert result.extracted_text is None
    assert "error" in result.metadata
    assert "not a valid docx" not in str(result.metadata)


def _minimal_text_pdf(text: str) -> bytes:
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    )
    return bytes(pdf)
