"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import type React from "react";
import { useCallback, useEffect, useState } from "react";

import { NoticePanel } from "@/components/product/NoticePanel";
import { SessionNav } from "@/components/product/SessionNav";
import { api } from "@/lib/api";
import type { BenchmarkResponse } from "@/lib/types";
import { isBenchmarkComparison } from "@/lib/types";

export default function BenchmarkPage() {
  const params = useParams<{ sessionId: string }>();
  const sessionId = params.sessionId;
  const [benchmark, setBenchmark] = useState<BenchmarkResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [preparing, setPreparing] = useState(false);

  const loadBenchmark = useCallback(
    async (active = true) => {
      try {
        const result = await api.getBenchmark(sessionId);
        if (!active) return;
        setBenchmark(result);
        setError(null);
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "Unable to load benchmark");
      } finally {
        if (active) setLoading(false);
      }
    },
    [sessionId],
  );

  useEffect(() => {
    let active = true;
    loadBenchmark(active);
    const interval = window.setInterval(() => loadBenchmark(active), 3000);
    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, [loadBenchmark]);

  return (
    <main className="mx-auto min-h-screen w-full max-w-6xl px-6 py-10">
      <header className="mb-8 border-b border-[var(--border)] pb-5">
        <SessionNav sessionId={sessionId} active="benchmark" />
        <h1 className="mt-3 text-3xl font-semibold tracking-tight">Benchmark gap dashboard</h1>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-[var(--muted)]">
          CueSpark compares candidate evidence against curated role benchmark profiles,
          then turns the gaps into interview risk areas and question targets.
        </p>
      </header>

      {loading && <StatePanel>Loading benchmark comparison...</StatePanel>}
      {error && (
        <NoticePanel
          title="Benchmark unavailable"
          tone="error"
          action={
            <button
              onClick={() => {
                setLoading(true);
                void loadBenchmark();
              }}
              className="rounded border border-red-300/40 px-3 py-2 text-xs"
            >
              Refresh benchmark
            </button>
          }
        >
          {error}
        </NoticePanel>
      )}

      {benchmark && !isBenchmarkComparison(benchmark) && (
        <NoticePanel
          title="Benchmark pending"
          action={
            <>
              <button
                onClick={() => {
                  setLoading(true);
                  void loadBenchmark();
                }}
                className="rounded border border-[var(--border)] px-3 py-2 text-xs"
              >
                Refresh status
              </button>
              <button
                onClick={async () => {
                  setPreparing(true);
                  try {
                    await api.prepareSession(sessionId);
                    await loadBenchmark();
                  } finally {
                    setPreparing(false);
                  }
                }}
                disabled={preparing}
                className="rounded bg-[var(--accent)] px-3 py-2 text-xs font-semibold text-black disabled:opacity-50"
              >
                {preparing ? "Starting..." : "Retry preparation"}
              </button>
            </>
          }
        >
          Benchmark comparison is pending for this session. Start preparation from the match
          page, then keep this dashboard open while the backend writes the comparison.
        </NoticePanel>
      )}

      {benchmark && isBenchmarkComparison(benchmark) && (
        <div className="space-y-6">
          <section className="grid gap-4 md:grid-cols-3">
            <ScoreCard
              label="Benchmark similarity"
              value={benchmark.benchmark_similarity_score}
              detail="How closely the resume evidence maps to the role benchmark corpus."
            />
            <ScoreCard
              label="Resume competitiveness"
              value={benchmark.resume_competitiveness_score}
              detail="How strong the resume looks relative to curated top-candidate archetypes."
            />
            <ScoreCard
              label="Evidence strength"
              value={benchmark.evidence_strength_score}
              detail="How much concrete proof, metrics, and ownership evidence is present."
            />
          </section>

          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-sm font-semibold">Why this is benchmark-driven</h2>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
              The dashboard is not a generic mock interview prompt. It shows which role
              benchmark signals are missing or weak, then exposes the exact gap targets
              that question generation should probe.
            </p>
            <div className="mt-4 text-sm">
              <span className="text-[var(--muted)]">Role key:</span>{" "}
              <span className="font-medium">{benchmark.role_key}</span>
            </div>
          </section>

          <section className="grid gap-4 lg:grid-cols-2">
            <ListPanel title="Missing skills" items={benchmark.missing_skills} />
            <ListPanel title="Weak skills" items={benchmark.weak_skills} />
            <ListPanel title="Missing metrics" items={benchmark.missing_metrics} />
            <ListPanel title="Weak ownership signals" items={benchmark.weak_ownership_signals} />
            <ListPanel title="Interview risk areas" items={benchmark.interview_risk_areas} />
            <ListPanel title="Recommended resume fixes" items={benchmark.recommended_resume_fixes} />
          </section>

          <ListPanel
            title="Question targets"
            items={benchmark.question_targets}
            description="These are the benchmark gaps that should drive strict interviewer questions."
          />

          <div className="flex flex-wrap gap-3">
            <Link
              href={`/session/${sessionId}/interview`}
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black"
            >
              Continue interview
            </Link>
            <button
              onClick={() => {
                setLoading(true);
                void loadBenchmark();
              }}
              className="rounded border border-[var(--border)] px-4 py-2 text-sm"
            >
              Refresh benchmark
            </button>
          </div>

          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-sm font-semibold">Benchmark profiles</h2>
            {benchmark.benchmark_profiles.length === 0 ? (
              <p className="mt-3 text-sm text-[var(--muted)]">No profile summaries returned.</p>
            ) : (
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                {benchmark.benchmark_profiles.map((profile) => (
                  <div key={profile.id} className="rounded border border-[var(--border)] p-4">
                    <div className="font-medium">{profile.profile_name}</div>
                    <div className="mt-1 text-sm text-[var(--muted)]">
                      {profile.role_title} - {profile.seniority_level}
                    </div>
                    <div className="mt-2 text-sm">
                      Quality score: {profile.quality_score === null ? "n/a" : profile.quality_score}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
      )}
    </main>
  );
}

function ScoreCard({
  label,
  value,
  detail,
}: {
  label: string;
  value: number | null;
  detail: string;
}) {
  return (
    <div className="rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="text-xs uppercase text-[var(--muted)]">{label}</div>
      <div className="mt-2 text-3xl font-semibold">{value === null ? "pending" : `${value}/100`}</div>
      <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{detail}</p>
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
  description?: string;
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

function StatePanel({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded border border-[var(--border)] bg-black/20 p-5 text-sm leading-6 text-[var(--muted)]">
      {children}
    </div>
  );
}
