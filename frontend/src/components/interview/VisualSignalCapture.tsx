"use client";

import { useEffect } from "react";

import { useVideoPreview } from "@/hooks/useVideoPreview";
import type { VisualSignalMetadata } from "@/lib/types";

const safeSignalLabels = [
  "camera presence",
  "lighting quality",
  "eye contact proxy",
  "posture stability",
];

export function defaultVisualSignalMetadata(): VisualSignalMetadata {
  return {
    camera_presence: "absent",
    lighting_quality: "moderate",
    face_in_frame_ratio: null,
    eye_contact_proxy: "not_measured",
    posture_stability: "not_measured",
    distraction_markers: [],
    safe_signal_labels: safeSignalLabels,
  };
}

export function VisualSignalCapture({
  value,
  disabled,
  onChange,
}: {
  value: VisualSignalMetadata;
  disabled?: boolean;
  onChange: (metadata: VisualSignalMetadata) => void;
}) {
  const preview = useVideoPreview();
  const isActive = preview.state === "active";

  useEffect(() => {
    if (preview.state === "active") {
      onChange({ ...value, camera_presence: "stable" });
    }
    if (preview.state === "stopped") {
      onChange({ ...value, camera_presence: "absent" });
    }
    // The parent owns value updates; this effect should respond only to camera state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [preview.state]);

  function sampleLighting() {
    const video = preview.videoRef.current;
    if (!video || video.videoWidth === 0 || video.videoHeight === 0) return;
    const canvas = document.createElement("canvas");
    canvas.width = 32;
    canvas.height = 18;
    const context = canvas.getContext("2d");
    if (!context) return;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
    let brightness = 0;
    for (let index = 0; index < pixels.length; index += 4) {
      brightness += (pixels[index] + pixels[index + 1] + pixels[index + 2]) / 3;
    }
    brightness /= pixels.length / 4;
    const lighting_quality =
      brightness < 65 ? "poor" : brightness < 135 ? "moderate" : "good";
    onChange({ ...value, lighting_quality });
  }

  return (
    <section className="rounded border border-[var(--border)] p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h4 className="text-sm font-semibold">Visual presence signals</h4>
          <p className="mt-1 max-w-2xl text-xs leading-5 text-[var(--muted)]">
            Camera preview is local and used only for observable interview-presence
            metadata. CueSpark does not detect emotion, personality, truthfulness, or
            true confidence.
          </p>
        </div>
        <span className="rounded-full bg-white/10 px-3 py-1 text-xs capitalize text-[var(--muted)]">
          {preview.state.replaceAll("_", " ")}
        </span>
      </div>

      <div className="mt-4 overflow-hidden rounded border border-[var(--border)] bg-black/30">
        <video
          ref={preview.videoRef}
          muted
          playsInline
          className={`aspect-video w-full object-cover ${isActive ? "block" : "hidden"}`}
        />
        {!isActive && (
          <div className="flex aspect-video items-center justify-center p-6 text-center text-sm text-[var(--muted)]">
            Camera preview is off. Start camera only if you want to include visual
            presence metadata.
          </div>
        )}
      </div>

      {preview.error && <p className="mt-3 text-sm text-red-200">{preview.error}</p>}

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          type="button"
          onClick={preview.start}
          disabled={disabled || preview.state === "requesting_permission" || isActive}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
        >
          {preview.state === "requesting_permission" ? "Requesting..." : "Start camera"}
        </button>
        <button
          type="button"
          onClick={preview.stop}
          disabled={disabled || !isActive}
          className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          Stop camera
        </button>
        <button
          type="button"
          onClick={sampleLighting}
          disabled={disabled || !isActive}
          className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          Sample lighting
        </button>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <SelectField
          label="Lighting quality"
          value={String(value.lighting_quality ?? "moderate")}
          disabled={disabled}
          options={["good", "moderate", "poor"]}
          onChange={(lighting_quality) => onChange({ ...value, lighting_quality })}
        />
        <SelectField
          label="Eye contact proxy"
          value={String(value.eye_contact_proxy ?? "not_measured")}
          disabled={disabled}
          options={["not_measured", "low", "moderate", "high"]}
          onChange={(eye_contact_proxy) => onChange({ ...value, eye_contact_proxy })}
        />
        <SelectField
          label="Posture stability"
          value={String(value.posture_stability ?? "not_measured")}
          disabled={disabled}
          options={["not_measured", "unstable", "moderate", "steady"]}
          onChange={(posture_stability) => onChange({ ...value, posture_stability })}
        />
        <SelectField
          label="Camera presence"
          value={String(value.camera_presence ?? "absent")}
          disabled={disabled}
          options={["stable", "intermittent", "absent"]}
          onChange={(camera_presence) => onChange({ ...value, camera_presence })}
        />
      </div>
    </section>
  );
}

function SelectField({
  label,
  value,
  options,
  disabled,
  onChange,
}: {
  label: string;
  value: string;
  options: string[];
  disabled?: boolean;
  onChange: (value: string) => void;
}) {
  return (
    <label className="block text-sm">
      <span className="font-medium">{label}</span>
      <select
        value={value}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded border border-[var(--border)] bg-black/30 p-3 text-sm capitalize outline-none focus:border-[var(--accent)] disabled:opacity-70"
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option.replaceAll("_", " ")}
          </option>
        ))}
      </select>
    </label>
  );
}
