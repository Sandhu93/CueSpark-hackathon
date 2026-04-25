import Link from "next/link";

import {
  DashboardCard,
  EvidenceDistribution,
  MetricCard,
  ProgressBar,
} from "@/components/demo/dashboard-widgets";
import {
  mockBenchmarkComparison,
  mockDashboardData,
  mockSession,
} from "@/lib/demo/mock-data";

const metricCards = [
  {
    title: "Benchmark Similarity",
    value: mockBenchmarkComparison.benchmarkSimilarityScore,
    detail: "Below the role benchmark corpus average, mostly due to weak proof of scale and ownership.",
    trend: mockDashboardData.scoreTrends[0].values,
    tone: "purple" as const,
  },
  {
    title: "Resume Competitiveness",
    value: mockBenchmarkComparison.resumeCompetitivenessScore,
    detail: "Weak proof compared to curated top-candidate archetypes for this role.",
    trend: mockDashboardData.scoreTrends[1].values,
    tone: "blue" as const,
  },
  {
    title: "Evidence Strength",
    value: mockBenchmarkComparison.evidenceStrengthScore,
    detail: "Metrics and ownership are under-evidenced for a senior backend role.",
    trend: mockDashboardData.scoreTrends[2].values,
    tone: "red" as const,
  },
  {
    title: "Hiring Bar Gap",
    value: 42,
    detail: "Significant gap to the expected senior benchmark signal.",
    trend: mockDashboardData.scoreTrends[3].values,
    tone: "amber" as const,
  },
];

export default function DemoBenchmarkPage() {
  return (
    <main className="min-h-screen px-4 py-6 lg:px-8">
      <section className="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wide text-blue-700">
            {mockSession.demoModeLabel}
          </div>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950 lg:text-4xl">
            CueSpark Benchmark Gap Dashboard
          </h1>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-[var(--muted)]">
            Candidate vs job description vs curated benchmark profiles. CueSpark turns evidence
            gaps into targeted interview strategy and question targets.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/demo/interview" className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white">
            Start demo interview
          </Link>
          <Link href="/setup" className="rounded-md border border-[var(--border)] bg-white px-4 py-2 text-sm font-semibold text-slate-700">
            Real setup
          </Link>
        </div>
      </section>

      <section className="mb-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metricCards.map((card) => (
          <MetricCard key={card.title} {...card} />
        ))}
      </section>

      <section className="mb-5 grid gap-4 xl:grid-cols-[1.15fr_1fr_1fr]">
        <DashboardCard className="xl:col-span-1">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-base font-semibold text-slate-900">Benchmark coverage by competency</h2>
              <p className="mt-1 text-sm text-[var(--muted)]">Candidate evidence compared with benchmark average.</p>
            </div>
            <span className="rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-700">
              role corpus
            </span>
          </div>
          <div className="mt-5 space-y-4">
            {mockDashboardData.benchmarkCoverage.map((item) => (
              <div key={item.label}>
                <div className="mb-2 flex items-center justify-between text-sm">
                  <span className="font-medium text-slate-700">{item.label}</span>
                  <span className="text-xs text-slate-500">
                    {item.candidateScore} vs {item.benchmarkScore}
                  </span>
                </div>
                <div className="space-y-1.5">
                  <ProgressBar value={item.benchmarkScore} tone="purple" />
                  <ProgressBar value={item.candidateScore} tone="blue" />
                </div>
              </div>
            ))}
          </div>
          <div className="mt-5 flex gap-4 text-xs text-slate-500">
            <span>Benchmark average</span>
            <span>Candidate evidence</span>
          </div>
        </DashboardCard>

        <DashboardCard>
          <div className="flex items-center gap-2">
            <h2 className="text-base font-semibold text-slate-900">Top benchmark gaps</h2>
            <span className="rounded-full bg-red-50 px-2 py-1 text-xs font-semibold text-red-700">
              High Priority
            </span>
          </div>
          <div className="mt-5 space-y-4">
            {mockDashboardData.topBenchmarkGaps.map((gap) => (
              <div key={gap.label}>
                <div className="mb-2 flex items-center justify-between gap-3 text-sm">
                  <div>
                    <div className="font-medium text-slate-800">{gap.label}</div>
                    <div className="text-xs text-[var(--muted)]">{gap.detail}</div>
                  </div>
                  <span className={severityClass(gap.severity)}>{gap.impactScore}</span>
                </div>
                <ProgressBar value={gap.impactScore} tone={gap.severity === "high" ? "red" : "amber"} />
              </div>
            ))}
          </div>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Evidence distribution</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">Resume and interview proof quality in the demo corpus.</p>
          <div className="mt-6">
            <EvidenceDistribution items={mockDashboardData.evidenceDistribution} />
          </div>
          <div className="mt-6 rounded-md bg-red-50 p-3 text-sm font-medium text-red-700">
            Missing or weak evidence is the main hiring bar gap.
          </div>
        </DashboardCard>
      </section>

      <section className="mb-5 grid gap-4 xl:grid-cols-[1fr_1fr_1fr]">
        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Benchmark profile match</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            Safe demo profiles and curated top-candidate archetypes, not hired resumes.
          </p>
          <div className="mt-5 space-y-4">
            {mockDashboardData.benchmarkProfileMatches.map((profile) => (
              <div key={profile.profileName} className="rounded-md border border-[var(--border)] p-3">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-slate-900">{profile.profileName}</div>
                    <div className="text-xs text-[var(--muted)]">{profile.profileSummary}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-violet-700">{profile.matchScore}%</div>
                    <div className="text-xs text-[var(--muted)]">{profile.matchLabel}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Generated question targets</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            Question pressure points generated from benchmark gaps.
          </p>
          <div className="mt-5 space-y-3">
            {mockDashboardData.questionTargetCounts.map((target) => (
              <div key={target.label} className="flex items-center justify-between rounded-md border border-[var(--border)] px-3 py-2 text-sm">
                <span className="text-slate-700">{target.label}</span>
                <span className="rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-700">
                  {target.count}
                </span>
              </div>
            ))}
          </div>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Actionable recommendations</h2>
          <div className="mt-5 space-y-3">
            {mockBenchmarkComparison.recommendedResumeFixes.map((fix) => (
              <div key={fix} className="rounded-md border border-emerald-100 bg-emerald-50 px-3 py-2 text-sm leading-6 text-emerald-800">
                {fix}
              </div>
            ))}
          </div>
        </DashboardCard>
      </section>

      <section className="grid gap-4 xl:grid-cols-[1fr_1fr]">
        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Interview strategy</h2>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
            {mockBenchmarkComparison.benchmarkExplanation}
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {mockDashboardData.interviewStrategyChips.map((chip) => (
              <span key={chip} className="rounded-full bg-violet-50 px-3 py-1 text-xs font-semibold text-violet-700">
                {chip}
              </span>
            ))}
          </div>
        </DashboardCard>

        <DashboardCard>
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-base font-semibold text-slate-900">Next step</h2>
              <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
                Run the mock interview to validate ownership, metrics, production depth, and
                architecture trade-off evidence.
              </p>
            </div>
            <Link href="/demo/interview" className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white">
              Continue to interview
            </Link>
          </div>
        </DashboardCard>
      </section>
    </main>
  );
}

function severityClass(severity: "high" | "medium" | "low") {
  if (severity === "high") return "rounded-full bg-red-50 px-2 py-1 text-xs font-semibold text-red-700";
  if (severity === "medium") return "rounded-full bg-amber-50 px-2 py-1 text-xs font-semibold text-amber-700";
  return "rounded-full bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700";
}
