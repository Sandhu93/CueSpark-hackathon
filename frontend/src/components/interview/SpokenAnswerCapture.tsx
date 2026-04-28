"use client";

import { useEffect, useRef, useState } from "react";

import { AnswerResultSummary } from "@/components/interview/AnswerResultSummary";
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import { api } from "@/lib/api";
import type { CandidateAnswerRead } from "@/lib/types";

type SpokenFlowState =
  | "idle"
  | "recording"
  | "recorded_not_submitted"
  | "uploading"
  | "processing"
  | "transcribing"
  | "running_agents"
  | "evaluated"
  | "failed";

export function SpokenAnswerCapture({ questionId }: { questionId: string }) {
  const recorder = useAudioRecorder();
  const resetRecorder = recorder.reset;
  const previousQuestionIdRef = useRef(questionId);
  const [flowState, setFlowState] = useState<SpokenFlowState>("idle");
  const [answerId, setAnswerId] = useState<string | null>(null);
  const [answer, setAnswer] = useState<CandidateAnswerRead | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    if (previousQuestionIdRef.current === questionId) return;
    previousQuestionIdRef.current = questionId;
    setFlowState("idle");
    setAnswerId(null);
    setAnswer(null);
    setSubmitError(null);
    resetRecorder();
  }, [questionId, resetRecorder]);

  useEffect(() => {
    if (recorder.state === "recording") setFlowState("recording");
    if (recorder.state === "recorded") setFlowState("recorded_not_submitted");
    if (recorder.state === "error") setFlowState("failed");
  }, [recorder.state]);

  useEffect(() => {
    if (!answerId || flowState === "evaluated" || flowState === "failed") return;
    const submittedAnswerId = answerId;
    let active = true;

    async function loadAnswer() {
      try {
        const nextAnswer = await api.getAnswer(submittedAnswerId);
        if (!active) return;
        setAnswer(nextAnswer);
        setFlowState(classifyAnswerState(nextAnswer));
      } catch {
        if (active) setFlowState("processing");
      }
    }

    loadAnswer();
    const timer = window.setInterval(loadAnswer, 2500);
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [answerId, flowState]);

  const statusLabel = flowState.replaceAll("_", " ");
  const canSubmit = recorder.recording !== null && flowState === "recorded_not_submitted";

  async function submitAnswer() {
    if (!recorder.recording) return;
    setFlowState("uploading");
    setSubmitError(null);
    try {
      const response = await api.submitSpokenAnswer(questionId, {
        audio: recorder.recording.file,
        duration_seconds: recorder.recording.durationSeconds,
      });
      setAnswerId(response.answer_id);
      setFlowState("processing");
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : "Unable to submit spoken answer");
      setFlowState("failed");
    }
  }

  function retry() {
    setAnswerId(null);
    setAnswer(null);
    setSubmitError(null);
    recorder.reset();
    setFlowState("idle");
  }

  return (
    <div className="rounded border border-[var(--border)] p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="font-medium">Spoken answer</h3>
          <p className="mt-1 text-sm text-[var(--muted)]">
            Record, retry, then submit your spoken response for transcription and agent analysis.
          </p>
        </div>
        <span className="rounded-full bg-white/10 px-3 py-1 text-xs capitalize text-[var(--muted)]">
          {statusLabel}
        </span>
      </div>

      <div className="mt-4 rounded border border-[var(--border)] bg-black/20 p-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="text-3xl font-semibold tabular-nums">
              {formatSeconds(recorder.elapsedSeconds)}
            </div>
            <p className="mt-1 text-xs text-[var(--muted)]">Recording timer</p>
          </div>
          <Waveform active={flowState === "recording"} />
        </div>
      </div>

      {recorder.error && <ErrorText>{recorder.error}</ErrorText>}
      {submitError && <ErrorText>{submitError}</ErrorText>}

      {recorder.recording && (
        <audio className="mt-4 w-full" controls src={recorder.recording.url}>
          <track kind="captions" />
        </audio>
      )}

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          onClick={recorder.start}
          disabled={flowState === "recording" || flowState === "uploading" || flowState === "processing"}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
        >
          Start recording
        </button>
        <button
          onClick={recorder.stop}
          disabled={flowState !== "recording"}
          className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          Stop
        </button>
        <button
          onClick={retry}
          disabled={flowState === "recording" || flowState === "uploading"}
          className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          Retry
        </button>
        <button
          onClick={submitAnswer}
          disabled={!canSubmit}
          className="rounded border border-[var(--accent)] px-4 py-2 text-sm font-semibold text-[var(--accent)] disabled:cursor-not-allowed disabled:opacity-50"
        >
          Submit answer
        </button>
      </div>

      {answerId && (
        <div className="mt-4 rounded border border-[var(--border)] p-3 text-sm text-[var(--muted)]">
          Answer ID: <span className="text-[var(--fg)]">{answerId}</span>
        </div>
      )}

      <AnswerProcessingDetails
        answer={answer}
        agentResults={answer?.agent_results ?? []}
        onRefresh={answerId ? () => void refreshAnswer(answerId) : undefined}
      />
    </div>
  );

  async function refreshAnswer(submittedAnswerId: string) {
    const nextAnswer = await api.getAnswer(submittedAnswerId);
    setAnswer(nextAnswer);
    setFlowState(classifyAnswerState(nextAnswer));
  }
}

function AnswerProcessingDetails({
  answer,
  agentResults,
  onRefresh,
}: {
  answer: CandidateAnswerRead | null;
  agentResults: NonNullable<CandidateAnswerRead["agent_results"]>;
  onRefresh?: () => void;
}) {
  return (
    <AnswerResultSummary
      answer={answer}
      agentResults={agentResults}
      emptyMessage="After submission, CueSpark will show transcript, communication signals, agent status, and final feedback when available."
      onRefresh={onRefresh}
    />
  );
}

function Waveform({ active }: { active: boolean }) {
  return (
    <div className="flex h-10 items-end gap-1" aria-hidden="true">
      {Array.from({ length: 18 }).map((_, index) => (
        <span
          key={index}
          className={`w-1 rounded-full ${active ? "bg-[var(--accent)]" : "bg-white/20"}`}
          style={{ height: `${10 + ((index * 7) % 28)}px` }}
        />
      ))}
    </div>
  );
}

function ErrorText({ children }: { children: React.ReactNode }) {
  return <p className="mt-3 text-sm text-red-200">{children}</p>;
}

function classifyAnswerState(answer: CandidateAnswerRead): SpokenFlowState {
  if (answer.evaluation?.overall_score !== null && answer.evaluation?.overall_score !== undefined) {
    return "evaluated";
  }
  if (answer.agent_results?.some((result) => result.status === "running")) {
    return "running_agents";
  }
  if (answer.transcript) return "running_agents";
  return "transcribing";
}

function formatSeconds(totalSeconds: number) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}
