"use client";

import type { AnswerEvaluationRead } from "@/lib/types";

export function AnswerFeedbackPanel({ evaluation }: { evaluation: AnswerEvaluationRead | null }) {
  if (!evaluation) {
    return (
      <section className="rounded border border-[var(--border)] p-4">
        <h4 className="text-sm font-semibold">Final answer feedback</h4>
        <p className="mt-2 text-sm text-[var(--muted)]">
          Final feedback will appear after the relevant agents finish processing.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded border border-[var(--border)] p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h4 className="text-sm font-semibold">Final answer feedback</h4>
        <span className="rounded-full border border-[var(--accent)] px-3 py-1 text-sm font-semibold text-[var(--accent)]">
          {evaluation.overall_score ?? "pending"}/100
        </span>
      </div>

      <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
        {evaluation.strict_feedback || "Strict feedback is not available yet."}
      </p>

      {(evaluation.benchmark_gap_summary || evaluation.communication_summary) && (
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {evaluation.benchmark_gap_summary && (
            <SummaryBox title="Benchmark gap summary" value={evaluation.benchmark_gap_summary} />
          )}
          {evaluation.communication_summary && (
            <SummaryBox title="Communication summary" value={evaluation.communication_summary} />
          )}
        </div>
      )}

      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <FeedbackList title="Strengths" value={evaluation.strengths} />
        <FeedbackList title="Weaknesses" value={evaluation.weaknesses} />
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <ScoreTile label="Benchmark gap coverage" value={evaluation.benchmark_gap_coverage_score} />
        <ScoreTile
          label="Communication signal"
          value={evaluation.communication_signal_score ?? evaluation.communication_score}
        />
        <ScoreTile label="Written answer" value={evaluation.written_answer_score} />
        <ScoreTile label="Code quality" value={evaluation.code_quality_score} />
        <ScoreTile label="Visual signal" value={evaluation.visual_signal_score} />
        <ScoreTile label="Evidence" value={evaluation.evidence_score} />
      </div>

      {evaluation.modality_breakdown && Object.keys(evaluation.modality_breakdown).length > 0 && (
        <div className="mt-4 rounded border border-[var(--border)] bg-white/5 p-3">
          <h5 className="text-xs font-semibold uppercase text-[var(--muted)]">
            Evaluation summary
          </h5>
          <div className="mt-2 grid gap-2 text-sm sm:grid-cols-2">
            {Object.entries(evaluation.modality_breakdown)
              .filter(([, value]) => isDisplayable(value))
              .slice(0, 6)
              .map(([key, value]) => (
                <div key={key} className="flex justify-between gap-3">
                  <span className="text-[var(--muted)]">{humanize(key)}</span>
                  <span>{String(value)}</span>
                </div>
              ))}
          </div>
        </div>
      )}
    </section>
  );
}

function SummaryBox({ title, value }: { title: string; value: string }) {
  return (
    <div className="rounded border border-[var(--border)] bg-white/5 p-3">
      <h5 className="text-xs font-semibold uppercase text-[var(--muted)]">{title}</h5>
      <p className="mt-2 text-sm leading-6">{value}</p>
    </div>
  );
}

function FeedbackList({
  title,
  value,
}: {
  title: string;
  value: string | string[] | null | undefined;
}) {
  const items = Array.isArray(value)
    ? value
    : typeof value === "string" && value.trim()
      ? [value]
      : [];

  return (
    <div className="rounded border border-[var(--border)] bg-white/5 p-3">
      <h5 className="text-xs font-semibold uppercase text-[var(--muted)]">{title}</h5>
      {items.length === 0 ? (
        <p className="mt-2 text-sm text-[var(--muted)]">Not available yet.</p>
      ) : (
        <ul className="mt-2 space-y-1 text-sm leading-6">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

function ScoreTile({ label, value }: { label: string; value: number | null | undefined }) {
  if (value === null || value === undefined) return null;
  return (
    <div className="rounded border border-[var(--border)] bg-white/5 p-3">
      <div className="text-xs text-[var(--muted)]">{label}</div>
      <div className="mt-1 text-lg font-semibold">{value}/100</div>
    </div>
  );
}

function humanize(value: string) {
  return value.replaceAll("_", " ");
}

function isDisplayable(value: unknown) {
  return ["string", "number", "boolean"].includes(typeof value);
}
