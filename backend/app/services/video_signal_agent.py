from __future__ import annotations

from typing import Any

from loguru import logger

from app.core.config import settings
from app.models.answer import CandidateAnswer
from app.schemas.agent_results import VideoSignalResult


DEFAULT_VIDEO_SIGNAL_METADATA: dict[str, Any] = {
    "face_in_frame_ratio": 0.9,
    "lighting_quality": "good",
    "eye_contact_proxy": "moderate",
    "posture_stability": "steady",
    "camera_presence": "stable",
    "distraction_markers": [],
}

SAFE_VISUAL_SIGNAL_LABELS = [
    "face in frame",
    "lighting quality",
    "eye contact proxy",
    "posture stability",
    "camera presence",
]


def analyze_video_signals(
    *,
    answer: CandidateAnswer,
    metadata: dict[str, Any] | None = None,
) -> VideoSignalResult:
    source = metadata or answer.visual_signal_metadata or {}
    if not source:
        if settings.ai_mock_mode or not settings.openai_api_key:
            logger.info("video_signal_agent: mock metadata for answer_id={}", answer.id)
            source = DEFAULT_VIDEO_SIGNAL_METADATA
        else:
            raise ValueError("Candidate answer has no video signal metadata to analyze")

    face_score = _score_face_in_frame(source.get("face_in_frame_ratio"))
    lighting_score = _score_quality(source.get("lighting_quality"), good_values={"good", "strong"})
    eye_contact_score = _score_quality(
        source.get("eye_contact_proxy"),
        good_values={"steady", "good", "high"},
        moderate_values={"moderate", "mixed"},
    )
    posture_score = _score_quality(
        source.get("posture_stability"),
        good_values={"steady", "stable", "good"},
        moderate_values={"moderate", "mixed"},
    )
    camera_score = _score_quality(
        source.get("camera_presence"),
        good_values={"stable", "present", "good"},
        moderate_values={"intermittent", "moderate"},
    )

    distraction_markers = _list_strings(source.get("distraction_markers"))
    if distraction_markers:
        posture_score = max(1, posture_score - min(len(distraction_markers), 3))
        camera_score = max(1, camera_score - 1)

    visual_score = round(
        (face_score + lighting_score + eye_contact_score + posture_score + camera_score) / 5
    )

    return VideoSignalResult(
        face_in_frame_score=face_score,
        lighting_score=lighting_score,
        eye_contact_proxy_score=eye_contact_score,
        posture_stability_score=posture_score,
        camera_presence_score=camera_score,
        visual_signal_score=visual_score,
        observations=_observations(
            face_score=face_score,
            lighting_score=lighting_score,
            eye_contact_score=eye_contact_score,
            posture_score=posture_score,
            camera_score=camera_score,
        ),
        risks=_risks(
            face_score=face_score,
            lighting_score=lighting_score,
            eye_contact_score=eye_contact_score,
            posture_score=posture_score,
            camera_score=camera_score,
            distraction_markers=distraction_markers,
        ),
    )


def _score_face_in_frame(value: Any) -> int:
    try:
        ratio = float(value)
    except (TypeError, ValueError):
        return 5
    if ratio >= 0.9:
        return 9
    if ratio >= 0.75:
        return 7
    if ratio >= 0.5:
        return 5
    return 3


def _score_quality(
    value: Any,
    *,
    good_values: set[str],
    moderate_values: set[str] | None = None,
) -> int:
    normalized = str(value or "").strip().lower().replace("_", " ")
    moderate = moderate_values or {"moderate", "mixed", "acceptable"}
    if normalized in good_values:
        return 8
    if normalized in moderate:
        return 6
    if normalized in {"poor", "low", "unstable", "absent", "off frame"}:
        return 3
    return 5


def _list_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _observations(
    *,
    face_score: int,
    lighting_score: int,
    eye_contact_score: int,
    posture_score: int,
    camera_score: int,
) -> list[str]:
    observations = ["Observable visual presence signals only; no identity or inner-state analysis."]
    if face_score >= 7:
        observations.append("Face-in-frame signal is usable for interview presence review.")
    if lighting_score >= 7:
        observations.append("Lighting quality is sufficient for a professional interview setup.")
    if camera_score >= 7:
        observations.append("Camera presence appears stable from the provided metadata.")
    if eye_contact_score >= 6:
        observations.append("Eye contact proxy is acceptable, based on frontend-provided metadata.")
    if posture_score >= 6:
        observations.append("Posture stability appears acceptable during the sampled period.")
    return observations


def _risks(
    *,
    face_score: int,
    lighting_score: int,
    eye_contact_score: int,
    posture_score: int,
    camera_score: int,
    distraction_markers: list[str],
) -> list[str]:
    risks = []
    if face_score < 7:
        risks.append("Face-in-frame signal may be inconsistent.")
    if lighting_score < 7:
        risks.append("Lighting quality may reduce perceived interview presence.")
    if eye_contact_score < 6:
        risks.append("Eye contact proxy is weak or inconsistent.")
    if posture_score < 6:
        risks.append("Posture stability may appear inconsistent.")
    if camera_score < 7:
        risks.append("Camera presence may be unstable.")
    for marker in distraction_markers:
        risks.append(f"Observed distraction marker: {marker}.")
    return risks
