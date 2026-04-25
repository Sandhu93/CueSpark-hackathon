from __future__ import annotations

import pytest

from app.services.chunking import ChunkResult, chunk_text


# ── basic behaviour ──────────────────────────────────────────────────────────

def test_empty_string_returns_empty_list():
    assert chunk_text("", "jd") == []


def test_whitespace_only_returns_empty_list():
    assert chunk_text("   \n\t  ", "resume") == []


def test_short_text_returns_single_chunk():
    result = chunk_text("Hello world", "jd")
    assert len(result) == 1
    assert result[0].content == "Hello world"
    assert result[0].chunk_index == 0
    assert result[0].chunk_type == "jd"


def test_chunk_index_is_sequential():
    text = " ".join(["word"] * 300)  # enough to produce multiple chunks
    result = chunk_text(text, "resume", chunk_size=100, overlap=10)
    for i, chunk in enumerate(result):
        assert chunk.chunk_index == i


def test_chunk_type_is_preserved_on_every_chunk():
    text = " ".join(["word"] * 300)
    result = chunk_text(text, "benchmark_profile", chunk_size=100, overlap=10)
    assert all(c.chunk_type == "benchmark_profile" for c in result)


def test_no_text_is_lost():
    """Every word in the original text appears in at least one chunk."""
    words = [f"word{i}" for i in range(100)]
    text = " ".join(words)
    result = chunk_text(text, "jd", chunk_size=80, overlap=20)
    combined = " ".join(c.content for c in result)
    for word in words:
        assert word in combined


def test_no_word_is_split_across_chunk_boundary():
    """Chunk boundaries must not fall inside a word."""
    text = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi"
    result = chunk_text(text, "jd", chunk_size=20, overlap=5)
    words_in_original = set(text.split())
    for chunk in result:
        for word in chunk.content.split():
            assert word in words_in_original


def test_overlap_produces_shared_content():
    """With overlap > 0 the tail of chunk N should appear in chunk N+1."""
    text = " ".join([f"token{i}" for i in range(60)])
    result = chunk_text(text, "resume", chunk_size=100, overlap=40)
    if len(result) >= 2:
        tail_words = result[0].content.split()[-3:]
        head_of_next = result[1].content
        assert any(w in head_of_next for w in tail_words)


def test_text_exactly_one_chunk_size():
    text = "a" * 500
    result = chunk_text(text, "jd", chunk_size=500, overlap=50)
    assert len(result) == 1
    assert result[0].content == "a" * 500


def test_leading_and_trailing_whitespace_stripped():
    result = chunk_text("  hello world  ", "jd")
    assert result[0].content == "hello world"


# ── chunk types ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("chunk_type", [
    "jd", "resume", "benchmark_profile", "answer", "rubric", "question_bank",
])
def test_all_contract_chunk_types_accepted(chunk_type):
    result = chunk_text("Some sample text for this chunk type.", chunk_type)
    assert len(result) == 1
    assert result[0].chunk_type == chunk_type


# ── guard rails ──────────────────────────────────────────────────────────────

def test_invalid_chunk_size_raises():
    with pytest.raises(ValueError):
        chunk_text("text", "jd", chunk_size=0)


def test_overlap_equal_to_chunk_size_raises():
    with pytest.raises(ValueError):
        chunk_text("text", "jd", chunk_size=100, overlap=100)


def test_negative_overlap_raises():
    with pytest.raises(ValueError):
        chunk_text("text", "jd", chunk_size=100, overlap=-1)
