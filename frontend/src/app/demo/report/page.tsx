import Link from "next/link";

import {
  DashboardCard,
  EvidenceDistribution,
  MetricCard,
  ProgressBar,
  ScoreGauge,
} from "@/components/demo/dashboard-widgets";
import {
  mockBenchmarkComparison,
  mockDashboardData,
  mockFinalReport,
  mockSession,
} from "@/lib/demo/mock-data";

const strongestAnswer = [...mockFinalReport.answerFeedback].sort((a, b) => b.score - a.score)[0];
const weakestAnswer = [...mockFinalReport.answerFeedback].sort((a, b) => a.score - b.score)[0];

export default function DemoReportPage() {
  return (
    <main className="min-h-screen px-4 py-6 lg:px-8">
      <section className="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wide text-blue-700">
            {mockSession.demoModeLabel}
          </div>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950 lg:text-4xl">
            Final Benchmark-Aware Readiness Report
          </h1>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-[var(--muted)]">
            Strict interviewer-style output: benchmark-driven, evidence-focused, and designed to
            close the most important readiness gaps before applying.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/demo/interview" className="rounded-md border border-[var(--border)] bg-white px-4 py-2 text-sm font-semibold text-slate-700">
            Back to interview
          </Link>
          <Link href="/setup" className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white">
            Real setup
          </Link>
        </div>
      </section>

      <section className="mb-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <DashboardCard>
          <h2 className="text-sm font-semibold text-slate-900">Readiness Score</h2>
          <ScoreGauge value={mockFinalReport.readinessScore} tone="amber" />
          <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
            Needs stronger proof before strong-hire readiness.
          </p>
          <span className="mt-3 inline-flex rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700">
            Borderline
          </span>
        </DashboardCard>
        <MetricCard
          title="Benchmark Similarity"
          value={mockFinalReport.benchmarkSimilarityScore}
          detail="Below benchmark profile average for senior backend ownership."
          trend={mockDashboardData.scoreTrends[0].values}
          tone="purple"
        />
        <MetricCard
          title="Evidence Strength"
          value={mockFinalReport.evidenceStrengthScore}
          detail="High-priority gap: measurable impact and ownership evidence."
          trend={mockDashboardData.scoreTrends[2].values}
          tone="red"
        />
        <DashboardCard className="bg-amber-50">
          <div className="text-sm font-semibold text-slate-900">Hiring Recommendation</div>
          <div className="mt-5 text-4xl font-semibold text-amber-600">
            {formatRecommendation(mockFinalReport.hiringRecommendation)}
          </div>
          <p className="mt-4 text-sm leading-6 text-amber-900">
            Borderline signal. Close key gaps in ownership and measurable impact.
          </p>
          <p className="mt-4 text-xs leading-5 text-amber-800">
            Mock readiness signal only, not a hiring guarantee.
          </p>
        </DashboardCard>
      </section>

      <section className="mb-5 grid gap-4 xl:grid-cols-[1.25fr_0.9fr_0.9fr]">
        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Benchmark gap summary</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">Candidate score against benchmark average.</p>
          <div className="mt-5 space-y-4">
            {mockDashboardData.benchmarkCoverage.map((item) => (
              <div key={item.label} className="grid gap-2 md:grid-cols-[130px_1fr_52px] md:items-center">
                <div className="text-sm font-medium text-slate-700">{item.label}</div>
                <div className="space-y-1.5">
                  <ProgressBar value={item.benchmarkScore} tone="purple" />
                  <ProgressBar value={item.candidateScore} tone="blue" />
                </div>
                <div className="text-right text-sm font-semibold text-blue-700">{item.candidateScore}</div>
              </div>
            ))}
          </div>
          <div className="mt-5 rounded-md bg-blue-50 px-3 py-2 text-sm text-blue-700">
            Largest gaps: ownership, business impact, and architecture trade-offs.
          </div>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Interview risk areas</h2>
          <div className="mt-5 space-y-3">
            {mockFinalReport.interviewRiskAreas.map((risk, index) => (
              <div key={risk} className="rounded-md border border-[var(--border)] p-3">
                <div className="mb-2 flex items-center justify-between">
                  <span className={index < 2 ? "rounded-full bg-red-50 px-2 py-1 text-xs font-semibold text-red-700" : "rounded-full bg-amber-50 px-2 py-1 text-xs font-semibold text-amber-700"}>
                    {index < 2 ? "High" : "Medium"}
                  </span>
                  <span className="text-xs text-[var(--muted)]">Impact</span>
                </div>
                <p className="text-sm leading-6 text-[var(--muted)]">{risk}</p>
              </div>
            ))}
          </div>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Evidence upgrade suggestions</h2>
          <div className="mt-5 space-y-3">
            <EvidenceStep label="Before" value={mockFinalReport.resumeBulletUpgrade.weakBullet} tone="purple" />
            <EvidenceStep label="After" value={mockFinalReport.resumeBulletUpgrade.improvedBullet} tone="green" />
            <EvidenceStep
              label="Prepare"
              value={mockFinalReport.resumeBulletUpgrade.missingEvidenceExplanation}
              tone="blue"
            />
          </div>
        </DashboardCard>
      </section>

      <section className="mb-5 grid gap-4 xl:grid-cols-[1fr_0.85fr_0.85fr_0.85fr]">
        <DashboardCard>
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-base font-semibold text-slate-900">Answer-by-answer performance</h2>
            <Link href="/demo/interview" className="text-sm font-semibold text-blue-700">
              View interview
            </Link>
          </div>
          <div className="mt-5 space-y-4">
            {mockFinalReport.answerFeedback.map((feedback) => (
              <div key={feedback.questionId}>
                <div className="mb-2 flex items-center justify-between gap-4 text-sm">
                  <span className="text-slate-700">
                    Q{feedback.questionNumber}. {formatLabel(feedback.category)}
                  </span>
                  <span className="font-semibold text-slate-900">{feedback.score}/100</span>
                </div>
                <ProgressBar value={feedback.score} tone={feedback.score >= 75 ? "green" : feedback.score >= 60 ? "amber" : "red"} />
              </div>
            ))}
          </div>
          <div className="mt-5 grid gap-3 md:grid-cols-2">
            <AnswerCallout title="Strongest answer" score={strongestAnswer.score} body={strongestAnswer.benchmarkGapCoverage} />
            <AnswerCallout title="Weakest answer" score={weakestAnswer.score} body={weakestAnswer.benchmarkGapCoverage} />
          </div>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Evidence distribution</h2>
          <div className="mt-6">
            <EvidenceDistribution items={mockDashboardData.evidenceDistribution} />
          </div>
          <p className="mt-5 text-sm leading-6 text-[var(--muted)]">
            Missing and weak evidence dominate the diagnostic.
          </p>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Resume rewrite priorities</h2>
          <ul className="mt-5 space-y-3">
            {mockFinalReport.resumeFeedback.map((item) => (
              <li key={item} className="rounded-md bg-blue-50 px-3 py-2 text-sm leading-6 text-blue-800">
                {item}
              </li>
            ))}
          </ul>
          <Link href="/demo/benchmark" className="mt-5 inline-flex text-sm font-semibold text-blue-700">
            See benchmark gaps
          </Link>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Preparation plan</h2>
          <ol id="prep-plan" className="mt-5 space-y-3">
            {mockFinalReport.preparationPlan.slice(0, 4).map((item, index) => (
              <li key={item} className="flex gap-3 text-sm leading-6">
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-blue-600 text-xs font-semibold text-white">
                  {index + 1}
                </span>
                <span className="text-[var(--muted)]">{item}</span>
              </li>
            ))}
          </ol>
          <p className="mt-5 rounded-md bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700">
            Strengthen evidence to close the gap.
          </p>
        </DashboardCard>
      </section>

      <section className="grid gap-4 xl:grid-cols-[1fr_1fr]">
        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Strict summary</h2>
          <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{mockFinalReport.summary}</p>
        </DashboardCard>

        <DashboardCard>
          <h2 className="text-base font-semibold text-slate-900">Benchmark context</h2>
          <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
            Hiring bar gap:{" "}
            <span className="font-semibold text-red-600">
              {mockBenchmarkComparison.hiringBarGap.toUpperCase()}
            </span>
            . The report is based on mock benchmark profiles and role benchmark corpus gaps for
            presentation only.
          </p>
        </DashboardCard>
      </section>
    </main>
  );
}

function EvidenceStep({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone: "purple" | "green" | "blue";
}) {
  const className =
    tone === "green"
      ? "bg-emerald-50 text-emerald-800"
      : tone === "purple"
        ? "bg-violet-50 text-violet-800"
        : "bg-blue-50 text-blue-800";

  return (
    <div className={`rounded-md px-3 py-3 ${className}`}>
      <div className="text-xs font-semibold uppercase">{label}</div>
      <p className="mt-2 text-sm leading-6">{value}</p>
    </div>
  );
}

function AnswerCallout({ title, score, body }: { title: string; score: number; body: string }) {
  return (
    <div className="rounded-md border border-[var(--border)] p-3">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm font-semibold text-slate-800">{title}</span>
        <span className="text-sm font-semibold text-blue-700">{score}/100</span>
      </div>
      <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{body}</p>
    </div>
  );
}

function formatRecommendation(value: string) {
  return value.replaceAll("_", " ").toUpperCase();
}

function formatLabel(value: string) {
  return value.replaceAll("_", " ");
}
