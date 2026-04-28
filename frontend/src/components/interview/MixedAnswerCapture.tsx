"use client";

import { useMemo, useState } from "react";
import type React from "react";

import { AnswerResultSummary } from "@/components/interview/AnswerResultSummary";
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import { useSubmittedAnswerPolling } from "@/hooks/useSubmittedAnswerPolling";
import { api } from "@/lib/api";
import type { QuestionRead, VisualSignalMetadata } from "@/lib/types";

const languages = [
  "python",
  "typescript",
  "javascript",
  "java",
  "go",
  "sql",
  "pseudocode",
];

export function MixedAnswerCapture({ question }: { question: QuestionRead }) {
  const recorder = useAudioRecorder();
  const [textAnswer, setTextAnswer] = useState("");
  const [codeAnswer, setCodeAnswer] = useState("");
  const [codeLanguage, setCodeLanguage] = useState("python");
  const [visualMetadata, setVisualMetadata] = useState<VisualSignalMetadata>({
    face_in_frame_ratio: 0.9,
    lighting_quality: "good",
    eye_contact_proxy: "moderate",
    posture_stability: "steady",
    camera_presence: "stable",
    safe_signal_labels: [
      "face in frame",
      "lighting quality",
      "eye contact proxy",
      "posture stability",
    ],
  });
  const [answerId, setAnswerId] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const { answer, state, setAnswer, setState, refresh } = useSubmittedAnswerPolling(answerId);

  const wordCount = useMemo(
    () => textAnswer.trim().split(/\s+/).filter(Boolean).length,
    [textAnswer],
  );
  const requiresAudio = question.requires_audio;
  const requiresText = question.requires_text;
  const requiresCode = question.requires_code;
  const requiresVideo = question.requires_video;
  const hasRequiredAudio = !requiresAudio || recorder.recording !== null;
  const hasRequiredText = !requiresText || textAnswer.trim().length > 0;
  const hasRequiredCode =
    !requiresCode || (codeAnswer.trim().length > 0 && codeLanguage.trim().length > 0);
  const canSubmit =
    !answerId &&
    state !== "uploading" &&
    recorder.state !== "recording" &&
    hasRequiredAudio &&
    hasRequiredText &&
    hasRequiredCode;

  async function submitAnswer() {
    if (!canSubmit) return;
    setState("uploading");
    setSubmitError(null);
    try {
      const response = await api.submitMixedAnswer(question.id, {
        audio: recorder.recording?.file,
        duration_seconds: recorder.recording?.durationSeconds,
        text_answer: textAnswer.trim() || undefined,
        code_answer: codeAnswer.trim() || undefined,
        code_language: codeAnswer.trim() ? codeLanguage : undefined,
        visual_signal_metadata: requiresVideo ? visualMetadata : undefined,
      });
      setAnswerId(response.answer_id);
      setState("processing");
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : "Unable to submit mixed answer");
      setState("failed");
    }
  }

  function reset() {
    setAnswerId(null);
    setAnswer(null);
    setSubmitError(null);
    recorder.reset();
    setState("editing");
  }

  return (
    <div className="rounded border border-[var(--border)] p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="font-medium">Mixed answer</h3>
          <p className="mt-1 text-sm text-[var(--muted)]">
            Submit one combined response with the required audio, written, code, and safe
            visual-signal fields.
          </p>
        </div>
        <span className="rounded-full bg-white/10 px-3 py-1 text-xs capitalize text-[var(--muted)]">
          {state.replaceAll("_", " ")}
        </span>
      </div>

      <div className="mt-4 rounded border border-[var(--border)] bg-black/20 p-3 text-sm text-[var(--muted)]">
        <span className="font-medium text-[var(--fg)]">Question reminder:</span>{" "}
        {question.question_text}
      </div>

      {requiresAudio && (
        <section className="mt-4 rounded border border-[var(--border)] p-4">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h4 className="text-sm font-semibold">Spoken explanation</h4>
              <p className="mt-1 text-xs text-[var(--muted)]">
                Record the verbal part of this mixed response.
              </p>
            </div>
            <div className="text-2xl font-semibold tabular-nums">
              {formatSeconds(recorder.elapsedSeconds)}
            </div>
          </div>

          {recorder.error && <ErrorText>{recorder.error}</ErrorText>}

          {recorder.recording && (
            <audio className="mt-4 w-full" controls src={recorder.recording.url}>
              <track kind="captions" />
            </audio>
          )}

          <div className="mt-4 flex flex-wrap gap-3">
            <button
              onClick={recorder.start}
              disabled={
                Boolean(answerId) || recorder.state === "recording" || state === "uploading"
              }
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
            >
              Start recording
            </button>
            <button
              onClick={recorder.stop}
              disabled={recorder.state !== "recording"}
              className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
            >
              Stop
            </button>
            <button
              onClick={recorder.reset}
              disabled={Boolean(answerId) || recorder.state === "recording" || state === "uploading"}
              className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
            >
              Retry audio
            </button>
          </div>
        </section>
      )}

      {requiresText && (
        <section className="mt-4 rounded border border-[var(--border)] p-4">
          <label className="text-sm font-semibold" htmlFor={`mixed-text-${question.id}`}>
            Written response
          </label>
          <textarea
            id={`mixed-text-${question.id}`}
            value={textAnswer}
            onChange={(event) => {
              setTextAnswer(event.target.value);
              if (!answerId) setState("editing");
            }}
            disabled={Boolean(answerId)}
            rows={6}
            className="mt-3 w-full resize-y rounded border border-[var(--border)] bg-black/30 p-3 text-sm leading-6 outline-none focus:border-[var(--accent)] disabled:opacity-70"
            placeholder="Add written structure, assumptions, evidence, and measurable impact..."
          />
          <div className="mt-2 flex justify-between text-xs text-[var(--muted)]">
            <span>{textAnswer.length} characters</span>
            <span>{wordCount} words</span>
          </div>
        </section>
      )}

      {requiresCode && (
        <section className="mt-4 rounded border border-[var(--border)] p-4">
          <h4 className="text-sm font-semibold">Code or pseudocode</h4>
          <p className="mt-1 text-xs text-[var(--muted)]">
            Static review only. CueSpark does not execute code here.
          </p>
          <label className="mt-4 block text-sm font-medium" htmlFor={`mixed-language-${question.id}`}>
            Language
          </label>
          <select
            id={`mixed-language-${question.id}`}
            value={codeLanguage}
            onChange={(event) => setCodeLanguage(event.target.value)}
            disabled={Boolean(answerId)}
            className="mt-2 w-full rounded border border-[var(--border)] bg-black/30 p-3 text-sm outline-none focus:border-[var(--accent)] disabled:opacity-70"
          >
            {languages.map((language) => (
              <option key={language} value={language}>
                {language}
              </option>
            ))}
          </select>

          <label className="mt-4 block text-sm font-medium" htmlFor={`mixed-code-${question.id}`}>
            Code
          </label>
          <textarea
            id={`mixed-code-${question.id}`}
            value={codeAnswer}
            onChange={(event) => {
              setCodeAnswer(event.target.value);
              if (!answerId) setState("editing");
            }}
            disabled={Boolean(answerId)}
            rows={10}
            spellCheck={false}
            className="mt-2 w-full resize-y rounded border border-[var(--border)] bg-black/40 p-3 font-mono text-sm leading-6 outline-none focus:border-[var(--accent)] disabled:opacity-70"
            placeholder="Write code or pseudocode. No browser execution is performed."
          />
        </section>
      )}

      {requiresVideo && (
        <VisualSignalMetadataPanel
          metadata={visualMetadata}
          disabled={Boolean(answerId)}
          onChange={setVisualMetadata}
        />
      )}

      {submitError && <ErrorText>{submitError}</ErrorText>}

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          onClick={submitAnswer}
          disabled={!canSubmit}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
        >
          {state === "uploading" ? "Submitting..." : "Submit mixed answer"}
        </button>
        <button
          onClick={reset}
          disabled={state === "uploading" || recorder.state === "recording"}
          className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          Reset response
        </button>
      </div>

      {answerId && (
        <div className="mt-4 rounded border border-[var(--border)] p-3 text-sm text-[var(--muted)]">
          Answer ID: <span className="text-[var(--fg)]">{answerId}</span>
        </div>
      )}

      <AnswerResultSummary
        answer={answer}
        agentResults={answer?.agent_results ?? []}
        emptyMessage="After submission, CueSpark will show one mixed-answer processing status and feedback result."
        onRefresh={answerId ? () => void refresh() : undefined}
      />
    </div>
  );
}

function VisualSignalMetadataPanel({
  metadata,
  disabled,
  onChange,
}: {
  metadata: VisualSignalMetadata;
  disabled: boolean;
  onChange: (metadata: VisualSignalMetadata) => void;
}) {
  return (
    <section className="mt-4 rounded border border-[var(--border)] p-4">
      <h4 className="text-sm font-semibold">Visual signal metadata</h4>
      <p className="mt-1 text-xs leading-5 text-[var(--muted)]">
        Optional mock/manual observable visual presence signals only. This does not request
        camera access and does not detect emotion, personality, truthfulness, or true confidence.
      </p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <SelectField
          label="Lighting quality"
          value={String(metadata.lighting_quality ?? "good")}
          disabled={disabled}
          options={["good", "moderate", "poor"]}
          onChange={(value) => onChange({ ...metadata, lighting_quality: value })}
        />
        <SelectField
          label="Eye contact proxy"
          value={String(metadata.eye_contact_proxy ?? "moderate")}
          disabled={disabled}
          options={["steady", "moderate", "low"]}
          onChange={(value) => onChange({ ...metadata, eye_contact_proxy: value })}
        />
        <SelectField
          label="Posture stability"
          value={String(metadata.posture_stability ?? "steady")}
          disabled={disabled}
          options={["steady", "moderate", "unstable"]}
          onChange={(value) => onChange({ ...metadata, posture_stability: value })}
        />
        <SelectField
          label="Camera presence"
          value={String(metadata.camera_presence ?? "stable")}
          disabled={disabled}
          options={["stable", "intermittent", "absent"]}
          onChange={(value) => onChange({ ...metadata, camera_presence: value })}
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
  disabled: boolean;
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
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

function ErrorText({ children }: { children: React.ReactNode }) {
  return <p className="mt-3 text-sm text-red-200">{children}</p>;
}

function formatSeconds(totalSeconds: number) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}
