import Link from "next/link";

import { DashboardCard } from "@/components/demo/dashboard-widgets";
import {
  mockBenchmarkComparison,
  mockSession,
  mockSetupPreview,
} from "@/lib/demo/mock-data";

const implementedNow = [
  "Session setup with JD and resume input",
  "Resume paste and upload support",
  "Benchmark-preparation pipeline in the backend",
  "Benchmark comparison data model and dashboard API",
  "Benchmark-driven question generation foundation",
];

const previewedNext = [
  "Mock-data benchmark dashboard presentation",
  "Simulated benchmark-driven interview room",
  "Observable communication signal panel",
  "Final readiness report experience",
];

export default function DemoPage() {
  return (
    <main className="min-h-screen px-4 py-6 lg:px-8">
      <section className="mb-6 grid gap-6 xl:grid-cols-[1fr_360px]">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wide text-blue-700">
            {mockSession.demoModeLabel}
          </div>
          <h1 className="mt-2 max-w-4xl text-3xl font-semibold tracking-tight text-slate-950 lg:text-4xl">
            Start a Benchmark Interview
          </h1>
          <p className="mt-3 max-w-3xl text-sm leading-6 text-[var(--muted)]">
            Upload a resume, paste the job description, and let CueSpark detect the gap between
            the candidate and the hiring benchmark. This preview is static mock data for
            hackathon judging.
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <Link href="/demo/benchmark" className="rounded-md bg-blue-600 px-5 py-3 text-sm font-semibold text-white">
              Open benchmark dashboard
            </Link>
            <Link href="/setup" className="rounded-md border border-[var(--border)] bg-white px-5 py-3 text-sm font-semibold text-slate-700">
              Use real setup flow
            </Link>
          </div>
        </div>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Sample demo session</h2>
          <dl className="mt-4 space-y-3 text-sm">
            <Info label="Role" value={mockSession.roleTitle} />
            <Info label="Company" value={mockSession.companyName} />
            <Info label="Role key" value={mockSession.roleKey} />
            <Info label="Hiring bar gap" value={mockBenchmarkComparison.hiringBarGap.toUpperCase()} />
          </dl>
        </DashboardCard>
      </section>

      <section className="mb-6 rounded-lg border border-[var(--border)] bg-white p-5 shadow-sm">
        <ol className="grid gap-3 md:grid-cols-5">
          {mockSetupPreview.workflowSteps.map((step, index) => (
            <li
              key={step.label}
              className={`rounded-lg border p-4 ${
                index === 0 ? "border-blue-300 bg-blue-50" : "border-[var(--border)] bg-white"
              }`}
            >
              <div className="flex items-center gap-3">
                <span
                  className={`flex h-9 w-9 items-center justify-center rounded-full text-sm font-semibold ${
                    index === 0 ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-700"
                  }`}
                >
                  {index + 1}
                </span>
                <div>
                  <div className="text-sm font-semibold text-slate-900">{step.label}</div>
                  <div className="text-xs text-[var(--muted)]">{step.description}</div>
                </div>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="mb-6 grid gap-5 xl:grid-cols-2">
        <DashboardCard>
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-base font-semibold text-slate-900">Job Description</h2>
              <p className="mt-1 text-sm text-[var(--muted)]">Paste the full job description for best results.</p>
            </div>
            <span className="rounded-md border border-[var(--border)] bg-white px-3 py-2 text-xs font-semibold text-slate-600">
              Paste from clipboard
            </span>
          </div>
          <div className="mt-5 min-h-44 rounded-lg border border-[var(--border)] bg-slate-50 p-4 text-base leading-8 text-slate-700">
            {mockSetupPreview.jdPreview}
          </div>
          <p className="mt-4 text-xs text-[var(--muted)]">
            Include responsibilities, must-haves, tools, and nice-to-haves for higher accuracy.
          </p>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Resume Input</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">Upload or paste the candidate resume.</p>
          <div className="mt-5 rounded-lg border border-dashed border-blue-300 bg-blue-50 p-6 text-center">
            <div className="text-sm font-semibold text-blue-700">Upload PDF / DOCX / TXT</div>
            <div className="mt-1 text-xs text-blue-600">or paste resume text below</div>
          </div>
          <div className="mt-4 min-h-24 rounded-lg border border-[var(--border)] bg-slate-50 p-4 text-sm leading-6 text-slate-700">
            {mockSetupPreview.resumePreview}
          </div>
          <p className="mt-4 text-xs text-[var(--muted)]">
            Static preview only. The real setup flow remains at `/setup`.
          </p>
        </DashboardCard>
      </section>

      <section className="mb-6 grid gap-5 xl:grid-cols-2">
        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Optional: Interviewer Lens</h2>
          <p className="mt-1 text-sm leading-6 text-[var(--muted)]">
            Upload user-provided interviewer context or paste public profile context. No scraping.
          </p>
          <div className="mt-5 rounded-lg border border-dashed border-violet-300 bg-violet-50 p-5 text-sm font-semibold text-violet-700">
            Upload PDF / DOCX / TXT - or paste public profile context
          </div>
          <p className="mt-4 rounded-lg bg-slate-50 p-4 text-sm leading-6 text-slate-700">
            {mockSetupPreview.interviewerLensPreview}
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            {mockSetupPreview.interviewerLensChips.map((chip) => (
              <span key={chip} className="rounded-full bg-violet-50 px-3 py-1 text-xs font-semibold text-violet-700">
                {chip}
              </span>
            ))}
          </div>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">What CueSpark will prepare</h2>
          <ul className="mt-5 space-y-4">
            {mockSetupPreview.preparationChecklist.map((item) => (
              <li key={item} className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-600 text-xs font-semibold text-white">
                  ✓
                </span>
                <div>
                  <div className="text-sm font-semibold text-slate-900">{item}</div>
                  <div className="text-xs text-[var(--muted)]">
                    Built from resume, JD, role benchmark corpus, and safe user-provided context.
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </DashboardCard>
      </section>

      <section className="grid gap-5 xl:grid-cols-[1fr_1fr]">
        <ListPanel title="Implemented backend flow" items={implementedNow} />
        <ListPanel title="Previewed with mock data" items={previewedNext} muted />
      </section>
    </main>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-[var(--muted)]">{label}</dt>
      <dd className="mt-1 break-words font-semibold text-slate-900">{value}</dd>
    </div>
  );
}

function ListPanel({
  title,
  items,
  muted,
}: {
  title: string;
  items: string[];
  muted?: boolean;
}) {
  return (
    <DashboardCard>
      <h2 className="text-base font-semibold text-slate-900">{title}</h2>
      <ul className="mt-4 space-y-2 text-sm leading-6">
        {items.map((item) => (
          <li key={item} className={muted ? "text-[var(--muted)]" : "text-slate-800"}>
            {item}
          </li>
        ))}
      </ul>
    </DashboardCard>
  );
}
