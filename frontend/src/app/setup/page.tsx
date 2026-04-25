"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import type React from "react";
import { useState } from "react";

import { api } from "@/lib/api";

type SubmitState = "idle" | "creating" | "uploading" | "preparing" | "done";

export default function SetupPage() {
  const router = useRouter();
  const [jobDescription, setJobDescription] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [roleTitle, setRoleTitle] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [state, setState] = useState<SubmitState>("idle");
  const [error, setError] = useState<string | null>(null);
  const [createdSessionId, setCreatedSessionId] = useState<string | null>(null);

  const canSubmit =
    jobDescription.trim().length > 0 && (resumeText.trim().length > 0 || Boolean(resumeFile));

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit || state !== "idle") return;

    setError(null);
    setCreatedSessionId(null);

    try {
      setState("creating");
      const session = await api.createSession({
        job_description: jobDescription,
        resume_text: resumeText.trim() || null,
        role_title: roleTitle.trim() || null,
        company_name: companyName.trim() || null,
      });
      setCreatedSessionId(session.session_id);

      if (resumeFile) {
        setState("uploading");
        await api.uploadResume(session.session_id, resumeFile);
      }

      setState("preparing");
      await api.prepareSession(session.session_id);
      setState("done");
      router.push(`/session/${session.session_id}/match`);
    } catch (err) {
      setState("idle");
      const message = err instanceof Error ? err.message : "Unknown setup error";
      setError(message);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-5xl flex-col px-6 py-10">
      <header className="mb-8 border-b border-[var(--border)] pb-5">
        <Link href="/" className="text-sm text-[var(--muted)]">
          CueSpark Interview Coach
        </Link>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight">Setup benchmark demo</h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--muted)]">
          Paste a job description and resume evidence, then prepare a session for benchmark
          comparison against curated role archetypes.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="grid gap-5 lg:grid-cols-[1fr_360px]">
        <section className="space-y-5">
          <Field label="Job description" required>
            <textarea
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
              className="min-h-64 w-full resize-y rounded border border-[var(--border)] bg-black/30 px-4 py-3 text-sm leading-6 outline-none focus:border-[var(--accent)]"
              placeholder="Paste the JD, role expectations, required skills, and seniority signals."
            />
          </Field>

          <Field label="Resume paste input" required={!resumeFile}>
            <textarea
              value={resumeText}
              onChange={(event) => setResumeText(event.target.value)}
              className="min-h-56 w-full resize-y rounded border border-[var(--border)] bg-black/30 px-4 py-3 text-sm leading-6 outline-none focus:border-[var(--accent)]"
              placeholder="Paste resume text, project evidence, metrics, tools, and ownership details."
            />
          </Field>
        </section>

        <aside className="space-y-5">
          <Field label="Role title">
            <input
              value={roleTitle}
              onChange={(event) => setRoleTitle(event.target.value)}
              className="w-full rounded border border-[var(--border)] bg-black/30 px-3 py-2 text-sm outline-none focus:border-[var(--accent)]"
              placeholder="Senior Backend Engineer"
            />
          </Field>

          <Field label="Company">
            <input
              value={companyName}
              onChange={(event) => setCompanyName(event.target.value)}
              className="w-full rounded border border-[var(--border)] bg-black/30 px-3 py-2 text-sm outline-none focus:border-[var(--accent)]"
              placeholder="Optional"
            />
          </Field>

          <Field label="Resume file upload">
            <input
              type="file"
              accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
              onChange={(event) => setResumeFile(event.target.files?.[0] ?? null)}
              className="block w-full text-sm text-[var(--muted)] file:mr-4 file:rounded file:border-0 file:bg-[var(--accent)] file:px-4 file:py-2 file:text-black"
            />
          </Field>

          <section className="rounded border border-[var(--border)] bg-black/20 p-4">
            <h2 className="text-sm font-semibold">Benchmark slice</h2>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
              This demo highlights gaps against a role benchmark corpus: missing skills,
              weak evidence, missing metrics, ownership risk, and question targets.
            </p>
          </section>

          <button
            type="submit"
            disabled={!canSubmit || state !== "idle"}
            className="w-full rounded bg-[var(--accent)] px-4 py-3 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-50"
          >
            {state === "idle" ? "Create and prepare session" : statusLabel(state)}
          </button>

          {createdSessionId && (
            <div className="rounded border border-[var(--border)] p-4 text-sm">
              <div className="text-[var(--muted)]">Session</div>
              <Link href={`/session/${createdSessionId}/match`} className="break-all">
                {createdSessionId}
              </Link>
            </div>
          )}

          {error && (
            <div className="rounded border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-200">
              {error}
            </div>
          )}
        </aside>
      </form>
    </main>
  );
}

function Field({
  label,
  required,
  children,
}: {
  label: string;
  required?: boolean;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium">
        {label}
        {required ? <span className="text-[var(--accent)]"> *</span> : null}
      </span>
      {children}
    </label>
  );
}

function statusLabel(state: SubmitState) {
  if (state === "creating") return "Creating session...";
  if (state === "uploading") return "Uploading resume...";
  if (state === "preparing") return "Starting preparation...";
  if (state === "done") return "Opening session...";
  return "Create and prepare session";
}
