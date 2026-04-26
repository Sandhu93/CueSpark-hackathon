"use client";

import { useParams } from "next/navigation";
import type React from "react";
import { useCallback, useEffect, useMemo, useState } from "react";

import { NoticePanel, SafetyCopy } from "@/components/product/NoticePanel";
import { SessionNav } from "@/components/product/SessionNav";
import { api } from "@/lib/api";
import type { Job, MultimodalReportRead, SessionRead } from "@/lib/types";

type ReportState = "loading" | "missing" | "generating" | "ready" | "failed";

export default function SessionReportPage() {
  const params = useParams<{ sessionId: string }>();
  const sessionId = params.sessionId;
  const [session, setSession] = useState<SessionRead | null>(null);
  const [report, setReport] = useState<MultimodalReportRead | null>(null);
  const [job, setJob] = useState<Job | null>(null);
  const [state, setState] = useState<ReportState>("loading");
  const [error, setError] = useState<string | null>(null);

  const loadReport = useCallback(
    async (active = true) => {
      try {
        const nextReport = await api.getReport(sessionId);
        if (!active) return;
        setReport(nextReport);
        setError(null);
        setState("ready");
      } catch (err) {
        if (!active) return;
        setReport(null);
        setState(isMissingReportError(err) ? "missing" : "failed");
        setError(isMissingReportError(err) ? null : errorMessage(err));
      }
    },
    [sessionId],
  );

  useEffect(() => {
    let active = true;

    async function load() {
      setState("loading");
      try {
        const nextSession = await api.getSession(sessionId);
        if (!active) return;
        setSession(nextSession);
        await loadReport(active);
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "Unable to load session report");
        setState("failed");
      }
    }

    load();
    return () => {
      active = false;
    };
  }, [loadReport, sessionId]);

  useEffect(() => {
    if (!job || job.status === "succeeded" || job.status === "failed") return;
    const activeJob = job;
    let active = true;

    async function pollJob() {
      try {
        const nextJob = await api.getJob(activeJob.id);
        if (!active) return;
        setJob(nextJob);
        if (nextJob.status === "succeeded") {
          await loadReport(active);
        }
        if (nextJob.status === "failed") {
          setError(nextJob.error || "Report generation failed");
          setState("failed");
        }
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "Unable to refresh report job");
        setState("failed");
      }
    }

    const timer = window.setInterval(pollJob, 2500);
    pollJob();
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [job, loadReport]);

  const recommendation = report?.hiring_recommendation
    ? humanize(report.hiring_recommendation)
    : "pending";
  const answerFeedbackItems = useMemo(
    () => normalizeList(report?.answer_feedback),
    [report?.answer_feedback],
  );

  async function generateReport() {
    setState("generating");
    setError(null);
    try {
      const nextJob = await api.generateReport(sessionId);
      setJob(nextJob);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to generate report");
      setState("failed");
    }
  }

  return (
    <main className="mx-auto min-h-screen w-full max-w-6xl px-6 py-8">
      <header className="mb-6 border-b border-[var(--border)] pb-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <SessionNav sessionId={sessionId} active="report" />
          <span className="rounded border border-[var(--border)] px-3 py-1 text-xs capitalize text-[var(--muted)]">
            Report {state}
          </span>
        </div>

        <div className="mt-5 grid gap-5 lg:grid-cols-[1fr_auto]">
          <div>
            <p className="text-sm font-medium text-[var(--accent)]">
              {session?.role_title ?? session?.role_key ?? "Target role pending"}
              {session?.company_name ? ` at ${session.company_name}` : ""}
            </p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight">
              Multimodal readiness report
            </h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-[var(--muted)]">
              Benchmark-aware readiness recommendation based on resume evidence,
              interview answers, and available communication signal summaries.
            </p>
          </div>
          <ReadinessScore score={report?.readiness_score ?? null} recommendation={recommendation} />
        </div>
      </header>

      {state === "loading" && <StatePanel>Loading readiness report...</StatePanel>}
      {state === "missing" && (
        <GeneratePanel onGenerate={generateReport} disabled={false} />
      )}
      {state === "generating" && (
        <NoticePanel
          title="Report generation in progress"
          action={
            <button
              onClick={() => job && void api.getJob(job.id).then(setJob)}
              className="rounded border border-[var(--border)] px-3 py-2 text-xs"
            >
              Refresh status
            </button>
          }
        >
          Report generation is queued or running. Keep this page open while CueSpark
          aggregates benchmark gaps, answer feedback, and modality summaries.
        </NoticePanel>
      )}
      {state === "failed" && (
        <NoticePanel
          title="Report unavailable"
          tone="error"
          action={
            <>
              <button
                onClick={() => void loadReport()}
                className="rounded border border-red-300/40 px-3 py-2 text-xs"
              >
                Refresh report
              </button>
              <button
                onClick={generateReport}
                className="rounded border border-red-300/40 px-3 py-2 text-xs"
              >
                Generate report
              </button>
            </>
          }
        >
          {error || "Unable to load or generate the report."}
        </NoticePanel>
      )}

      {state === "ready" && report && (
        <div className="space-y-6">
          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-sm font-semibold">Strict summary</h2>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
              {report.summary || "Summary is not available yet."}
            </p>
            <p className="mt-4 text-sm leading-6 text-[var(--muted)]">
              {report.jd_resume_match_summary || "JD-resume match summary is not available yet."}
            </p>
          </section>

          <SafetyCopy recommendation />

          <section className="grid gap-4 md:grid-cols-4">
            <ScoreCard label="JD-resume match" value={session?.match_score ?? null} />
            <ScoreCard label="Benchmark similarity" value={report.benchmark_similarity_score} />
            <ScoreCard label="Resume competitiveness" value={report.resume_competitiveness_score} />
            <ScoreCard label="Evidence strength" value={report.evidence_strength_score} />
          </section>

          <section className="grid gap-4 lg:grid-cols-2">
            <ListPanel
              title="Benchmark gap coverage"
              items={normalizeList(report.benchmark_gaps)}
              description={report.benchmark_gap_coverage_summary}
            />
            <ListPanel
              title="Interview risk areas"
              items={normalizeList(report.interview_risk_areas)}
            />
          </section>

          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-sm font-semibold">Answer-by-answer feedback</h2>
            {answerFeedbackItems.length === 0 ? (
              <p className="mt-3 text-sm text-[var(--muted)]">No answer feedback returned.</p>
            ) : (
              <div className="mt-4 space-y-3">
                {answerFeedbackItems.map((item, index) => (
                  <FeedbackCard key={`${item}-${index}`} index={index + 1} item={item} />
                ))}
              </div>
            )}
          </section>

          <section className="grid gap-4 lg:grid-cols-2">
            <SummaryPanel
              title="Communication signal summary"
              value={report.audio_communication_summary ?? report.communication_summary}
            />
            <SummaryPanel title="Visual signal summary" value={report.visual_signal_summary} />
            <SummaryPanel
              title="Written answer summary"
              value={report.written_answer_quality_summary ?? report.written_answer_summary}
            />
            <SummaryPanel
              title="Code answer summary"
              value={report.code_answer_quality_summary ?? report.code_answer_summary}
            />
          </section>

          <section className="grid gap-4 lg:grid-cols-2">
            <ListPanel
              title="Resume improvement suggestions"
              items={normalizeList(report.resume_feedback)}
            />
            <ListPanel
              title="Preparation plan"
              items={normalizeList(report.improvement_plan)}
            />
          </section>
        </div>
      )}
    </main>
  );
}

function ReadinessScore({
  score,
  recommendation,
}: {
  score: number | null;
  recommendation: string;
}) {
  return (
    <section className="min-w-64 rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="text-xs uppercase text-[var(--muted)]">Readiness score</div>
      <div className="mt-2 text-4xl font-semibold">
        {score === null ? "pending" : `${score}/100`}
      </div>
      <div className="mt-4 text-xs uppercase text-[var(--muted)]">
        Readiness recommendation
      </div>
      <div className="mt-1 text-lg font-semibold capitalize">{recommendation}</div>
    </section>
  );
}

function GeneratePanel({
  onGenerate,
  disabled,
}: {
  onGenerate: () => void;
  disabled: boolean;
}) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">No report is available yet</h2>
      <p className="mt-2 max-w-3xl text-sm leading-6 text-[var(--muted)]">
        Generate the final report after the interview answers and agent processing have
        completed. The report will aggregate benchmark gap coverage, answer feedback,
        communication signal summary, and preparation priorities.
      </p>
      <button
        onClick={onGenerate}
        disabled={disabled}
        className="mt-4 rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
      >
        Generate readiness report
      </button>
    </section>
  );
}

function ScoreCard({ label, value }: { label: string; value: number | null }) {
  return (
    <div className="rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="text-xs uppercase text-[var(--muted)]">{label}</div>
      <div className="mt-2 text-3xl font-semibold">
        {value === null ? "pending" : `${value}/100`}
      </div>
    </div>
  );
}

function ListPanel({
  title,
  items,
  description,
}: {
  title: string;
  items: string[];
  description?: string | null;
}) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">{title}</h2>
      {description && <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{description}</p>}
      {items.length === 0 ? (
        <p className="mt-4 text-sm text-[var(--muted)]">No items returned.</p>
      ) : (
        <ul className="mt-4 space-y-2 text-sm leading-6">
          {items.map((item) => (
            <li key={item} className="rounded border border-[var(--border)] px-3 py-2">
              {item}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function FeedbackCard({ index, item }: { index: number; item: string }) {
  return (
    <article className="rounded border border-[var(--border)] p-4">
      <div className="text-xs uppercase text-[var(--muted)]">Answer {index}</div>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{item}</p>
    </article>
  );
}

function SummaryPanel({
  title,
  value,
}: {
  title: string;
  value: string | Record<string, unknown> | null | undefined;
}) {
  const items = normalizeSummary(value);
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">{title}</h2>
      {items.length === 0 ? (
        <p className="mt-3 text-sm text-[var(--muted)]">Not available.</p>
      ) : (
        <div className="mt-4 space-y-2 text-sm leading-6 text-[var(--muted)]">
          {items.map((item) => (
            <p key={item}>{item}</p>
          ))}
        </div>
      )}
    </section>
  );
}

function StatePanel({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded border border-[var(--border)] bg-black/20 p-5 text-sm leading-6 text-[var(--muted)]">
      {children}
    </div>
  );
}

function normalizeList(value: unknown): string[] {
  if (!value) return [];
  if (Array.isArray(value)) {
    return value.map(formatUnknownValue).filter(Boolean);
  }
  if (typeof value === "string") {
    return value
      .split(/\n+/)
      .map((item) => item.trim())
      .filter(Boolean);
  }
  return [formatUnknownValue(value)].filter(Boolean);
}

function normalizeSummary(value: unknown): string[] {
  if (!value) return [];
  if (typeof value === "string") return value.trim() ? [value] : [];
  if (Array.isArray(value)) return value.map(formatUnknownValue).filter(Boolean);
  if (typeof value === "object") {
    return Object.entries(value as Record<string, unknown>)
      .filter(([, entryValue]) => entryValue !== null && entryValue !== undefined)
      .map(([key, entryValue]) => `${humanize(key)}: ${formatUnknownValue(entryValue)}`);
  }
  return [String(value)];
}

function formatUnknownValue(value: unknown): string {
  if (value === null || value === undefined) return "";
  if (typeof value === "string") return value.trim();
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (Array.isArray(value)) return value.map(formatUnknownValue).filter(Boolean).join(", ");
  if (typeof value === "object") {
    const record = value as Record<string, unknown>;
    const preferred =
      record.strict_feedback ??
      record.feedback ??
      record.summary ??
      record.question ??
      record.title;
    if (preferred) return String(preferred);
    return Object.entries(record)
      .map(([key, entryValue]) => `${humanize(key)}: ${formatUnknownValue(entryValue)}`)
      .join("; ");
  }
  return String(value);
}

function isMissingReportError(err: unknown) {
  const message = errorMessage(err);
  return message.startsWith("404") || message.toLowerCase().includes("not found");
}

function errorMessage(err: unknown) {
  return err instanceof Error ? err.message : "Unknown error";
}

function humanize(value: string) {
  return value.replaceAll("_", " ");
}
