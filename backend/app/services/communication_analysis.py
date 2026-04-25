from __future__ import annotations

import re

from app.schemas.answer import AudioAgentResult

FILLER_WORDS = {"um", "uh", "like", "actually", "basically", "you know"}
HESITATION_MARKERS = {"...", "—", "--"}


def analyze_communication_signals(
    transcript: str,
    *,
    duration_seconds: float | None,
) -> AudioAgentResult:
    words = re.findall(r"[A-Za-z0-9']+", transcript)
    normalized_words = [word.lower() for word in words]
    filler_matches = [word for word in normalized_words if word in FILLER_WORDS]
    unique_fillers = sorted(set(filler_matches))
    hesitation_markers = [marker for marker in HESITATION_MARKERS if marker in transcript]
    word_count = len(words)
    words_per_minute = _words_per_minute(word_count, duration_seconds)
    structure_observations = _structure_observations(transcript)

    return AudioAgentResult(
        transcript=transcript,
        word_count=word_count,
        duration_seconds=duration_seconds,
        words_per_minute=words_per_minute,
        filler_word_count=len(filler_matches),
        filler_words=unique_fillers,
        hesitation_markers=hesitation_markers,
        structure_observations=structure_observations,
        communication_signal_score=_communication_signal_score(
            word_count=word_count,
            words_per_minute=words_per_minute,
            filler_word_count=len(filler_matches),
            structure_observations=structure_observations,
        ),
    )


def _words_per_minute(word_count: int, duration_seconds: float | None) -> float | None:
    if duration_seconds is None or duration_seconds <= 0:
        return None
    return round(word_count / (duration_seconds / 60), 1)


def _structure_observations(transcript: str) -> list[str]:
    lower = transcript.lower()
    observations: list[str] = []
    if any(term in lower for term in ("first", "then", "after", "finally")):
        observations.append("Uses sequence markers")
    if any(term in lower for term in ("impact", "reduced", "improved", "increased")):
        observations.append("Mentions impact")
    if any(term in lower for term in ("owned", "led", "responsible")):
        observations.append("Mentions ownership")
    if not observations:
        observations.append("Answer structure needs clearer context, action, and impact")
    return observations


def _communication_signal_score(
    *,
    word_count: int,
    words_per_minute: float | None,
    filler_word_count: int,
    structure_observations: list[str],
) -> int:
    score = 7
    if word_count < 20:
        score -= 2
    if words_per_minute is not None and (words_per_minute < 90 or words_per_minute > 180):
        score -= 1
    if filler_word_count > 8:
        score -= 1
    if "Answer structure needs clearer context, action, and impact" not in structure_observations:
        score += 1
    return max(1, min(10, score))
