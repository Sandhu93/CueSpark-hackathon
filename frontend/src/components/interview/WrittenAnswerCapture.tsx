"use client";

import { useMemo, useState } from "react";

import { AnswerResultSummary } from "@/components/interview/AnswerResultSummary";
import { useSubmittedAnswerPolling } from "@/hooks/useSubmittedAnswerPolling";
import { api } from "@/lib/api";

export function WrittenAnswerCapture({
  questionId,
  questionText,
}: {
  questionId: string;
  questionText: string;
}) {
  const [textAnswer, setTextAnswer] = useState("");
  const [answerId, setAnswerId] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const { answer, state, setAnswer, setState, refresh } = useSubmittedAnswerPolling(answerId);

  const wordCount = useMemo(
    () => textAnswer.trim().split(/\s+/).filter(Boolean).length,
    [textAnswer],
  );
  const canSubmit = textAnswer.trim().length > 0 && state !== "uploading" && !answerId;

  async function submitAnswer() {
    if (!canSubmit) return;
    setState("uploading");
    setSubmitError(null);
    try {
      const response = await api.submitWrittenAnswer(questionId, {
        text_answer: textAnswer.trim(),
      });
      setAnswerId(response.answer_id);
      setState("processing");
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : "Unable to submit written answer");
      setState("failed");
    }
  }

  function reset() {
    setAnswerId(null);
    setAnswer(null);
    setSubmitError(null);
    setState("editing");
  }

  return (
    <div className="rounded border border-[var(--border)] p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="font-medium">Written answer</h3>
          <p className="mt-1 text-sm text-[var(--muted)]">
            Draft a structured response. CueSpark will evaluate relevance, evidence,
            specificity, completeness, and clarity.
          </p>
        </div>
        <span className="rounded-full bg-white/10 px-3 py-1 text-xs capitalize text-[var(--muted)]">
          {state.replaceAll("_", " ")}
        </span>
      </div>

      <div className="mt-4 rounded border border-[var(--border)] bg-black/20 p-3 text-sm text-[var(--muted)]">
        <span className="font-medium text-[var(--fg)]">Question reminder:</span>{" "}
        {questionText}
      </div>

      <textarea
        value={textAnswer}
        onChange={(event) => {
          setTextAnswer(event.target.value);
          if (!answerId) setState("editing");
        }}
        disabled={Boolean(answerId)}
        rows={8}
        className="mt-4 w-full resize-y rounded border border-[var(--border)] bg-black/30 p-3 text-sm leading-6 outline-none focus:border-[var(--accent)] disabled:opacity-70"
        placeholder="Write your answer with context, action, evidence, and measurable result..."
      />

      <div className="mt-3 flex flex-wrap items-center justify-between gap-3 text-xs text-[var(--muted)]">
        <span>{textAnswer.length} characters</span>
        <span>{wordCount} words</span>
      </div>

      {submitError && <p className="mt-3 text-sm text-red-200">{submitError}</p>}

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          onClick={submitAnswer}
          disabled={!canSubmit}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
        >
          {state === "uploading" ? "Submitting..." : "Submit written answer"}
        </button>
        <button
          onClick={reset}
          disabled={state === "uploading"}
          className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          Edit another response
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
        emptyMessage="After submission, CueSpark will show text-agent status and feedback when available."
        onRefresh={answerId ? () => void refresh() : undefined}
      />
    </div>
  );
}
