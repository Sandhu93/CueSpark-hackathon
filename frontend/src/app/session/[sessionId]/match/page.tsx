"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import type React from "react";
import { useEffect, useMemo, useState } from "react";

import { api } from "@/lib/api";
import type { SessionRead } from "@/lib/types";

export default function MatchPage() {
  const params = useParams<{ sessionId: string }>();
  const sessionId = params.sessionId;
  const [session, setSession] = useState<SessionRead | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function load() {
      try {
        const nextSession = await api.getSession(sessionId);
        if (!active) return;
        setSession(nextSession);
        setError(null);
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "Unable to load session");
      } finally {
        if (active) setLoading(false);
      }
    }

    load();
    const interval = window.setInterval(load, 2500);
    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, [sessionId]);

  const statusTone = useMemo(() => {
    if (!session) return "text-[var(--muted)]";
    if (session.status === "ready" || session.status === "completed") return "text-emerald-300";
    if (session.status === "failed") return "text-red-300";
    if (session.status === "preparing") return "text-yellow-200";
    return "text-[var(--muted)]";
  }, [session]);

  return (
    <main className="mx-auto min-h-screen w-full max-w-4xl px-6 py-10">
      <header className="mb-8 border-b border-[var(--border)] pb-5">
        <Link href="/setup" className="text-sm text-[var(--muted)]">
          Setup
        </Link>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight">Match status</h1>
        <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
          Preparation state and JD-resume match signals for this benchmark session.
        </p>
      </header>

      {loading && <Panel>Loading session...</Panel>}
      {error && <ErrorPanel message={error} />}

      {session && (
        <div className="space-y-5">
          <section className="grid gap-4 sm:grid-cols-3">
            <Metric label="Status" value={session.status} valueClassName={statusTone} />
            <Metric label="Match score" value={formatScore(session.match_score)} />
            <Metric label="Role key" value={session.role_key ?? "pending"} />
          </section>

          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-sm font-semibold">Session details</h2>
            <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
              <Info label="Session ID" value={session.id} />
              <Info label="Role title" value={session.role_title ?? "pending"} />
              <Info label="Company" value={session.company_name ?? "not provided"} />
              <Info label="Updated" value={new Date(session.updated_at).toLocaleString()} />
            </dl>
          </section>

          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-sm font-semibold">Benchmark readiness</h2>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
              The benchmark dashboard shows why the interview plan is not generic: it is
              driven by role-corpus gaps, evidence strength, and risks in the candidate
              resume against curated benchmark profiles.
            </p>
            <div className="mt-5 flex flex-wrap gap-3">
              <Link
                href={`/session/${session.id}/benchmark`}
                className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black"
              >
                Open benchmark dashboard
              </Link>
              <button
                onClick={async () => {
                  setLoading(true);
                  try {
                    await api.prepareSession(session.id);
                    setError(null);
                  } catch (err) {
                    setError(err instanceof Error ? err.message : "Unable to start preparation");
                  } finally {
                    setLoading(false);
                  }
                }}
                className="rounded border border-[var(--border)] px-4 py-2 text-sm"
              >
                Retry preparation
              </button>
            </div>
          </section>
        </div>
      )}
    </main>
  );
}

function Metric({
  label,
  value,
  valueClassName,
}: {
  label: string;
  value: string;
  valueClassName?: string;
}) {
  return (
    <div className="rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="text-xs uppercase text-[var(--muted)]">{label}</div>
      <div className={`mt-2 break-words text-2xl font-semibold ${valueClassName ?? ""}`}>
        {value}
      </div>
    </div>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-[var(--muted)]">{label}</dt>
      <dd className="mt-1 break-words">{value}</dd>
    </div>
  );
}

function Panel({ children }: { children: React.ReactNode }) {
  return <div className="rounded border border-[var(--border)] p-5 text-sm">{children}</div>;
}

function ErrorPanel({ message }: { message: string }) {
  return (
    <div className="rounded border border-red-500/40 bg-red-500/10 p-5 text-sm text-red-200">
      {message}
    </div>
  );
}

function formatScore(score: number | null) {
  return score === null ? "pending" : `${score}/100`;
}
