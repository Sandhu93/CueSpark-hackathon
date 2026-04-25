import Link from "next/link";

import { mockBenchmarkComparison, mockSession } from "@/lib/demo/mock-data";

const demoScreens = [
  {
    href: "/demo/benchmark",
    title: "Benchmark dashboard",
    description:
      "Shows benchmark similarity, evidence strength, missing skills, weak ownership signals, and question targets.",
  },
  {
    href: "/demo/interview",
    title: "Interview room",
    description:
      "Previews how benchmark gaps become strict interviewer questions and answer prompts.",
  },
  {
    href: "/demo/report",
    title: "Final readiness report",
    description:
      "Summarizes readiness, risk areas, answer feedback, resume fixes, and a preparation plan.",
  },
];

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
    <main className="min-h-screen">
      <section className="border-b border-[var(--border)]">
        <div className="mx-auto grid w-full max-w-6xl gap-8 px-6 py-12 lg:grid-cols-[1fr_360px] lg:py-16">
          <div>
            <div className="inline-flex rounded border border-[var(--border)] bg-black/30 px-3 py-1 text-xs font-medium text-[var(--accent)]">
              {mockSession.demoModeLabel}
            </div>
            <h1 className="mt-5 max-w-3xl text-4xl font-semibold tracking-tight sm:text-5xl">
              Product vision preview for benchmark-driven interview readiness.
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-7 text-[var(--muted)]">
              This is a mock-data product preview for hackathon judging. The real backend
              currently supports the benchmark-preparation pipeline. This preview demonstrates
              the full intended experience: benchmark dashboard, interview room, and final
              readiness report.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href="/demo/benchmark"
                className="rounded bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-black"
              >
                Open demo preview
              </Link>
              <Link
                href="/setup"
                className="rounded border border-[var(--border)] px-5 py-3 text-sm"
              >
                Use real setup flow
              </Link>
            </div>
          </div>

          <aside className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-sm font-semibold">Sample demo session</h2>
            <dl className="mt-4 space-y-3 text-sm">
              <Info label="Role" value={mockSession.roleTitle} />
              <Info label="Company" value={mockSession.companyName} />
              <Info label="Role key" value={mockSession.roleKey} />
              <Info
                label="Hiring bar gap"
                value={mockBenchmarkComparison.hiringBarGap.toUpperCase()}
              />
            </dl>
          </aside>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-5 px-6 py-10 lg:grid-cols-3">
        <Explainer
          title="What CueSpark is"
          body="CueSpark helps candidates practice against a role benchmark corpus, not just a generic AI interviewer prompt."
        />
        <Explainer
          title="Why benchmark-driven is different"
          body="It compares resume evidence against curated benchmark profiles, identifies weak proof, then uses those gaps to shape interview questions."
        />
        <Explainer
          title="What this preview shows"
          body="A complete product vision using mock data: benchmark gaps, a simulated interview room, and a strict final readiness report."
        />
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-5 px-6 pb-10 lg:grid-cols-[1fr_1fr]">
        <ListPanel title="Implemented backend flow" items={implementedNow} />
        <ListPanel title="Previewed with mock data" items={previewedNext} muted />
      </section>

      <section className="mx-auto w-full max-w-6xl px-6 pb-14">
        <div className="rounded border border-[var(--border)] bg-black/20 p-5">
          <h2 className="text-sm font-semibold">Demo navigation</h2>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            {demoScreens.map((screen) => (
              <Link
                key={screen.href}
                href={screen.href}
                className="rounded border border-[var(--border)] p-4 transition-colors hover:border-[var(--accent)]"
              >
                <div className="font-medium">{screen.title}</div>
                <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
                  {screen.description}
                </p>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </main>
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

function Explainer({ title, body }: { title: string; body: string }) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">{title}</h2>
      <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{body}</p>
    </section>
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
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">{title}</h2>
      <ul className="mt-4 space-y-2 text-sm leading-6">
        {items.map((item) => (
          <li key={item} className={muted ? "text-[var(--muted)]" : ""}>
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}
