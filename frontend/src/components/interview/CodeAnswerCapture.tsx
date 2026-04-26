"use client";

import { useState } from "react";

import { AnswerResultSummary } from "@/components/interview/AnswerResultSummary";
import { useSubmittedAnswerPolling } from "@/hooks/useSubmittedAnswerPolling";
import { api } from "@/lib/api";

const languages = [
  "python",
  "typescript",
  "javascript",
  "java",
  "go",
  "sql",
  "pseudocode",
];

export function CodeAnswerCapture({
  questionId,
  questionText,
}: {
  questionId: string;
  questionText: string;
}) {
  const [codeAnswer, setCodeAnswer] = useState("");
  const [codeLanguage, setCodeLanguage] = useState("python");
  const [explanation, setExplanation] = useState("");
  const [answerId, setAnswerId] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const { answer, state, setAnswer, setState, refresh } = useSubmittedAnswerPolling(answerId);

  const canSubmit = codeAnswer.trim().length > 0 && codeLanguage.trim().length > 0 && !answerId;

  async function submitAnswer() {
    if (!canSubmit) return;
    setState("uploading");
    setSubmitError(null);
    try {
      const response = await api.submitCodeAnswer(questionId, {
        code_answer: codeAnswer.trim(),
        code_language: codeLanguage,
        text_answer: explanation.trim() || undefined,
      });
      setAnswerId(response.answer_id);
      setState("processing");
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : "Unable to submit code answer");
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
          <h3 className="font-medium">Code answer</h3>
          <p className="mt-1 text-sm text-[var(--muted)]">
            Submit code or pseudocode for static review. CueSpark does not execute code here.
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

      <label className="mt-4 block text-sm font-medium" htmlFor={`language-${questionId}`}>
        Language
      </label>
      <select
        id={`language-${questionId}`}
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

      <label className="mt-4 block text-sm font-medium" htmlFor={`code-${questionId}`}>
        Code
      </label>
      <textarea
        id={`code-${questionId}`}
        value={codeAnswer}
        onChange={(event) => {
          setCodeAnswer(event.target.value);
          if (!answerId) setState("editing");
        }}
        disabled={Boolean(answerId)}
        rows={12}
        spellCheck={false}
        className="mt-2 w-full resize-y rounded border border-[var(--border)] bg-black/40 p-3 font-mono text-sm leading-6 outline-none focus:border-[var(--accent)] disabled:opacity-70"
        placeholder="Write your solution here. Static review only; no local execution."
      />

      <label className="mt-4 block text-sm font-medium" htmlFor={`explanation-${questionId}`}>
        Explanation
      </label>
      <textarea
        id={`explanation-${questionId}`}
        value={explanation}
        onChange={(event) => setExplanation(event.target.value)}
        disabled={Boolean(answerId)}
        rows={4}
        className="mt-2 w-full resize-y rounded border border-[var(--border)] bg-black/30 p-3 text-sm leading-6 outline-none focus:border-[var(--accent)] disabled:opacity-70"
        placeholder="Explain complexity, edge cases, trade-offs, and test approach..."
      />

      <div className="mt-3 flex flex-wrap items-center justify-between gap-3 text-xs text-[var(--muted)]">
        <span>{codeAnswer.split(/\n/).filter((line) => line.trim()).length} non-empty lines</span>
        <span>No code execution is performed in the browser.</span>
      </div>

      {submitError && <p className="mt-3 text-sm text-red-200">{submitError}</p>}

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          onClick={submitAnswer}
          disabled={!canSubmit || state === "uploading"}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
        >
          {state === "uploading" ? "Submitting..." : "Submit code answer"}
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
        emptyMessage="After submission, CueSpark will show static code-review agent status and feedback when available."
        onRefresh={answerId ? () => void refresh() : undefined}
      />
    </div>
  );
}
