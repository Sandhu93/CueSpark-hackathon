"use client";

import { useMemo } from "react";

import { AgentStatusPanel } from "@/components/interview/AgentStatusPanel";
import { AnswerFeedbackPanel } from "@/components/interview/AnswerFeedbackPanel";
import type { AgentResultRead, CandidateAnswerRead } from "@/lib/types";

export function AnswerResultSummary({
  answer,
  agentResults,
  emptyMessage,
  onRefresh,
}: {
  answer: CandidateAnswerRead | null;
  agentResults: AgentResultRead[];
  emptyMessage: string;
  onRefresh?: () => void;
}) {
  const metricRows = useMemo(
    (): [string, unknown][] => {
      const metrics = answer?.communication_metrics ?? answer?.communication_metadata ?? {};
      const rows: [string, unknown][] = [
        ["Words", answer?.word_count],
        ["Words/min", answer?.words_per_minute],
        ["Filler words", answer?.filler_word_count],
        ["Communication score", metrics.communication_signal_score],
      ];
      return rows.filter(([, value]) => value !== null && value !== undefined);
    },
    [
      answer?.communication_metadata,
      answer?.communication_metrics,
      answer?.filler_word_count,
      answer?.word_count,
      answer?.words_per_minute,
    ],
  );

  if (!answer) {
    return <p className="mt-4 text-sm leading-6 text-[var(--muted)]">{emptyMessage}</p>;
  }

  return (
    <div className="mt-5 space-y-4">
      {answer.transcript && (
        <section className="rounded border border-[var(--border)] p-4">
          <h4 className="text-sm font-semibold">Transcript</h4>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{answer.transcript}</p>
        </section>
      )}

      {metricRows.length > 0 && (
        <section className="rounded border border-[var(--border)] p-4">
          <h4 className="text-sm font-semibold">Communication signals</h4>
          <p className="mt-1 text-xs text-[var(--muted)]">
            Observable communication signal labels only.
          </p>
          <dl className="mt-3 grid gap-3 sm:grid-cols-2">
            {metricRows.map(([label, value]) => (
              <div key={String(label)} className="rounded bg-white/5 p-3">
                <dt className="text-xs text-[var(--muted)]">{label}</dt>
                <dd className="mt-1 font-semibold">{String(value)}</dd>
              </div>
            ))}
          </dl>
          <SafeSignalLabels
            labels={extractStringList(
              answer.communication_metrics?.safe_signal_labels ??
                answer.communication_metadata?.safe_signal_labels,
            )}
          />
        </section>
      )}

      <VisualSignalSummary answer={answer} />

      <AgentStatusPanel answer={answer} agentResults={agentResults} onRefresh={onRefresh} />
      <AnswerFeedbackPanel evaluation={answer.evaluation ?? null} />
    </div>
  );
}

function VisualSignalSummary({ answer }: { answer: CandidateAnswerRead }) {
  const labels = extractStringList(answer.visual_signal_metadata.safe_signal_labels);
  const visibleSignals = [
    "face in frame",
    "lighting quality",
    "eye contact proxy",
    "posture stability",
  ];
  const hasMetadata = Object.keys(answer.visual_signal_metadata ?? {}).length > 0;

  if (!hasMetadata) return null;

  return (
    <section className="rounded border border-[var(--border)] p-4">
      <h4 className="text-sm font-semibold">Visual signals</h4>
      <p className="mt-1 text-xs text-[var(--muted)]">
        Observable visual signal labels only.
      </p>
      <SafeSignalLabels labels={labels.length > 0 ? labels : visibleSignals} />
    </section>
  );
}

function SafeSignalLabels({ labels }: { labels: string[] }) {
  if (labels.length === 0) return null;
  return (
    <div className="mt-3 flex flex-wrap gap-2">
      {labels.map((label) => (
        <span
          key={label}
          className="rounded-full border border-[var(--border)] px-3 py-1 text-xs text-[var(--muted)]"
        >
          {label}
        </span>
      ))}
    </div>
  );
}

function extractStringList(value: unknown): string[] {
  return Array.isArray(value)
    ? value.map((item) => String(item)).filter(Boolean)
    : [];
}
