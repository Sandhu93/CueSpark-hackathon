from __future__ import annotations

from app.core.db import Base
from app.models.benchmark_comparison import BenchmarkComparison
from app.models.benchmark_profile import BenchmarkProfile, BenchmarkSourceType


def test_benchmark_profile_table_registered():
    assert "benchmark_profiles" in Base.metadata.tables


def test_benchmark_comparison_table_registered():
    assert "benchmark_comparisons" in Base.metadata.tables


def test_benchmark_profile_has_uuid_pk():
    col = BenchmarkProfile.__table__.c["id"]
    assert col.primary_key


def test_benchmark_comparison_has_uuid_pk():
    col = BenchmarkComparison.__table__.c["id"]
    assert col.primary_key


def test_benchmark_comparison_session_id_has_fk():
    col = BenchmarkComparison.__table__.c["session_id"]
    fk_targets = {fk.target_fullname for fk in col.foreign_keys}
    assert "interview_sessions.id" in fk_targets


def test_benchmark_source_type_enum_values():
    assert BenchmarkSourceType.CURATED == "curated"
    assert BenchmarkSourceType.PUBLIC == "public"
    assert BenchmarkSourceType.SYNTHETIC == "synthetic"


def test_benchmark_profile_jsonb_columns_exist():
    table = BenchmarkProfile.__table__
    for col_name in ("skills", "tools", "project_signals", "impact_signals", "ownership_signals"):
        assert col_name in table.c, f"column {col_name!r} missing from benchmark_profiles"


def test_benchmark_comparison_jsonb_columns_exist():
    table = BenchmarkComparison.__table__
    for col_name in (
        "benchmark_profile_ids",
        "missing_skills",
        "weak_skills",
        "missing_metrics",
        "weak_ownership_signals",
        "interview_risk_areas",
        "recommended_resume_fixes",
        "question_targets",
    ):
        assert col_name in table.c, f"column {col_name!r} missing from benchmark_comparisons"


def test_both_new_tables_in_models_init():
    import app.models as m
    assert hasattr(m, "BenchmarkProfile")
    assert hasattr(m, "BenchmarkComparison")
