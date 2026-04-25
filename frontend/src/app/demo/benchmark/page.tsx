import Link from "next/link";

import { mockBenchmarkComparison, mockSession } from "@/lib/demo/mock-data";

const scoreCards = [
  {
    label: "Benchmark Similarity",
    value: `${mockBenchmarkComparison.benchmarkSimilarityScore}/100`,
    detail: "How closely the resume evidence maps to the role benchmark corpus.",
  },
  {
    label: "Resume Competitiveness",
    value: `${mockBenchmarkComparison.resumeCompetitivenessScore}/100`,
    detail: "How strong the candidate proof looks against curated top-candidate archetypes.",
  },
  {
    label: "Evidence Strength",
    value: `${mockBenchmarkComparison.evidenceStrengthScore}/100`,
    detail: "How much concrete proof, metrics, project scale, and ownership evidence is present.",
  },
  {
    label: "Hiring Bar Gap",
    value: mockBenchmarkComparison.hiringBarGap.toUpperCase(),
    detail: "The gap between current evidence and the expected benchmark signal for this role.",
    tone: "risk",
  },
] satisfies Array<{
  label: string;
  value: string;
  detail: string;
  tone?: "risk";
}>;

const gapSections = [
  {
    title: "Missing skills",
    description: "Role-specific capabilities the benchmark corpus expects to see.",
    items: mockBenchmarkComparison.missingSkills,
  },
  {
    title: "Weak evidence",
    description: "Claims that need stronger proof, depth, or examples.",
    items: mockBenchmarkComparison.weakSkills,
  },
  {
    title: "Missing metrics",
    description: "Measurable outcomes a strict interviewer will ask for.",
    items: mockBenchmarkComparison.missingMetrics,
  },
  {
    title: "Weak ownership signals",
    description: "Places where final responsibility and post-launch ownership are unclear.",
    items: mockBenchmarkComparison.weakOwnershipSignals,
  },
  {
    title: "Interview risk areas",
    description: "Likely doubt areas after comparing the resume to benchmark profiles.",
    items: mockBenchmarkComparison.interviewRiskAreas,
  },
  {
    title: "Recommended resume fixes",
    description: "Targeted edits that would close evidence gaps before applying.",
    items: mockBenchmarkComparison.recommendedResumeFixes,
  },
];

export default function DemoBenchmarkPage() {
  return (
    <main className="min-h-screen">
      <section className="border-b border-[var(--border)]">
        <div className="mx-auto w-full max-w-6xl px-6 py-10">
          <nav className="mb-8 flex flex-wrap items-center gap-4 text-sm">
            <Link href="/demo" className="text-[var(--muted)]">
              Demo
            </Link>
            <Link href="/setup" className="text-[var(--muted)]">
              Real setup
            </Link>
          </nav>

          <div className="grid gap-8 lg:grid-cols-[1fr_360px]">
            <div>
              <div className="inline-flex rounded border border-[var(--border)] bg-black/30 px-3 py-1 text-xs font-medium text-[var(--accent)]">
                {mockSession.demoModeLabel}
              </div>
              <h1 className="mt-5 text-4xl font-semibold tracking-tight sm:text-5xl">
                Candidate vs Hiring Benchmark
              </h1>
              <p className="mt-5 max-w-3xl text-base leading-7 text-[var(--muted)]">
                CueSpark compares candidate evidence against a role benchmark corpus, identifies
                evidence gaps, then turns those gaps into strict interviewer question targets.
              </p>
            </div>

            <aside className="rounded border border-[var(--border)] bg-black/20 p-5">
              <h2 className="text-sm font-semibold">Demo candidate context</h2>
              <dl className="mt-4 space-y-3 text-sm">
                <Info label="Role" value={mockSession.roleTitle} />
                <Info label="Company" value={mockSession.companyName} />
                <Info label="Role key" value={mockSession.roleKey} />
              </dl>
            </aside>
          </div>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-4 px-6 py-8 sm:grid-cols-2 lg:grid-cols-4">
        {scoreCards.map((card) => (
          <ScoreCard key={card.label} {...card} />
        ))}
      </section>

      <section className="mx-auto w-full max-w-6xl px-6 pb-8">
        <div className="rounded border border-[var(--border)] bg-black/20 p-5">
          <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
            <div>
              <h2 className="text-lg font-semibold">This is not a generic mock interview</h2>
              <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                {mockBenchmarkComparison.benchmarkExplanation}
              </p>
              <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                The interview strategy is built from benchmark-driven evidence gaps: missing
                skills, weak proof, missing metrics, ownership risk, and role-specific question
                targets.
              </p>
            </div>
            <div className="rounded border border-[var(--border)] p-4">
              <div className="text-xs uppercase text-[var(--muted)]">Hiring bar gap</div>
              <div className="mt-2 text-3xl font-semibold text-red-200">
                {mockBenchmarkComparison.hiringBarGap.toUpperCase()}
              </div>
              <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                The candidate has credible backend experience, but the proof is below the
                senior benchmark on metrics, ownership, and scale.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-4 px-6 pb-8 lg:grid-cols-2">
        {gapSections.map((section) => (
          <ListPanel key={section.title} {...section} />
        ))}
      </section>

      <section className="mx-auto w-full max-w-6xl px-6 pb-8">
        <div className="rounded border border-[var(--border)] bg-black/20 p-5">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold">Question targets from benchmark gaps</h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--muted)]">
                These targets show how CueSpark turns hiring-bar evidence gaps into a strict,
                benchmark-driven interview.
              </p>
            </div>
            <Link
              href="/demo/interview"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black"
            >
              Continue to demo interview
            </Link>
          </div>
          <ol className="mt-5 grid gap-3 lg:grid-cols-2">
            {mockBenchmarkComparison.questionTargets.map((target, index) => (
              <li
                key={target}
                className="rounded border border-[var(--border)] bg-black/20 p-4 text-sm leading-6"
              >
                <span className="mr-2 text-[var(--accent)]">{index + 1}.</span>
                {target}
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-6 pb-14">
        <div className="rounded border border-[var(--border)] bg-black/20 p-5">
          <h2 className="text-lg font-semibold">Curated benchmark profile summaries</h2>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
            Safe demo wording: these are benchmark profiles and curated top-candidate
            archetypes, not hired resumes or scraped personal profiles.
          </p>
          <div className="mt-5 grid gap-3 md:grid-cols-3">
            {mockBenchmarkComparison.benchmarkProfiles.map((profile) => (
              <article key={profile.id} className="rounded border border-[var(--border)] p-4">
                <div className="text-sm font-medium">{profile.profileName}</div>
                <div className="mt-1 text-xs text-[var(--muted)]">
                  {profile.roleTitle} - {profile.seniorityLevel}
                </div>
                <div className="mt-3 text-sm">Quality score: {profile.qualityScore}/100</div>
                <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                  {profile.archetypeSummary}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

function ScoreCard({
  label,
  value,
  detail,
  tone,
}: {
  label: string;
  value: string;
  detail: string;
  tone?: "risk";
}) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="text-xs uppercase text-[var(--muted)]">{label}</div>
      <div className={`mt-2 text-3xl font-semibold ${tone === "risk" ? "text-red-200" : ""}`}>
        {value}
      </div>
      <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{detail}</p>
    </section>
  );
}

function ListPanel({
  title,
  description,
  items,
}: {
  title: string;
  description: string;
  items: string[];
}) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">{title}</h2>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{description}</p>
      <ul className="mt-4 space-y-2 text-sm leading-6">
        {items.map((item) => (
          <li key={item} className="rounded border border-[var(--border)] bg-black/20 px-3 py-2">
            {item}
          </li>
        ))}
      </ul>
    </section>
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
