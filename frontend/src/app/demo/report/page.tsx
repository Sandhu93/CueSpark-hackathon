import Link from "next/link";

import {
  mockBenchmarkComparison,
  mockFinalReport,
  mockSession,
} from "@/lib/demo/mock-data";

const scoreCards = [
  {
    label: "JD-resume match",
    value: mockFinalReport.jdResumeMatchScore,
    detail: "How directly the resume maps to the posted role requirements.",
  },
  {
    label: "Benchmark similarity",
    value: mockFinalReport.benchmarkSimilarityScore,
    detail: "How closely the evidence matches the role benchmark corpus.",
  },
  {
    label: "Resume competitiveness",
    value: mockFinalReport.resumeCompetitivenessScore,
    detail: "How strong the resume looks against curated top-candidate archetypes.",
  },
  {
    label: "Evidence strength",
    value: mockFinalReport.evidenceStrengthScore,
    detail: "How concrete the proof is across metrics, scale, ownership, and impact.",
  },
];

const secondaryScores = [
  ["Role-specific depth", mockFinalReport.roleSpecificDepthScore],
  ["Communication clarity", mockFinalReport.communicationClarityScore],
  ["Benchmark gap coverage", mockFinalReport.benchmarkGapCoverageScore],
] satisfies Array<[string, number]>;

const strongestAnswer = [...mockFinalReport.answerFeedback].sort((a, b) => b.score - a.score)[0];
const weakestAnswer = [...mockFinalReport.answerFeedback].sort((a, b) => a.score - b.score)[0];

export default function DemoReportPage() {
  return (
    <main className="min-h-screen">
      <section className="border-b border-[var(--border)]">
        <div className="mx-auto w-full max-w-6xl px-6 py-8">
          <nav className="mb-8 flex flex-wrap items-center gap-4 text-sm">
            <Link href="/demo/interview" className="text-[var(--muted)]">
              Interview room
            </Link>
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
                Final Readiness Report
              </h1>
              <p className="mt-5 max-w-3xl text-base leading-7 text-[var(--muted)]">
                {mockFinalReport.summary}
              </p>
            </div>

            <aside className="rounded border border-[var(--border)] bg-black/20 p-5">
              <div className="text-xs uppercase text-[var(--muted)]">Overall readiness score</div>
              <div className="mt-2 text-6xl font-semibold">{mockFinalReport.readinessScore}</div>
              <div className="mt-1 text-sm text-[var(--muted)]">out of 100</div>
              <div className="mt-5 rounded border border-[var(--border)] bg-black/20 p-4">
                <div className="text-xs uppercase text-[var(--muted)]">Hiring recommendation</div>
                <div className="mt-2 text-2xl font-semibold">
                  {formatRecommendation(mockFinalReport.hiringRecommendation)}
                </div>
                <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                  Mock readiness signal only. This is a strict preparation diagnostic, not a
                  hiring guarantee.
                </p>
              </div>
            </aside>
          </div>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-4 px-6 py-8 sm:grid-cols-2 lg:grid-cols-4">
        {scoreCards.map((card) => (
          <ScoreCard key={card.label} {...card} />
        ))}
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-5 px-6 pb-8 lg:grid-cols-[1fr_360px]">
        <section className="rounded border border-[var(--border)] bg-black/20 p-5">
          <h2 className="text-lg font-semibold">Interview risk areas</h2>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
            These risks matter because a strict interviewer will look for benchmark-level proof:
            clear ownership, measurable impact, and role-specific judgment under constraints.
          </p>
          <ul className="mt-5 space-y-3">
            {mockFinalReport.interviewRiskAreas.map((risk) => (
              <li key={risk} className="rounded border border-[var(--border)] bg-black/20 p-4">
                <div className="text-xs uppercase text-red-200">Risk</div>
                <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{risk}</p>
              </li>
            ))}
          </ul>
        </section>

        <aside className="rounded border border-[var(--border)] bg-black/20 p-5">
          <h2 className="text-lg font-semibold">Benchmark depth checks</h2>
          <dl className="mt-4 space-y-3">
            {secondaryScores.map(([label, value]) => (
              <div key={label} className="rounded border border-[var(--border)] p-3">
                <dt className="text-xs uppercase text-[var(--muted)]">{label}</dt>
                <dd className="mt-2 text-2xl font-semibold">{value}/100</dd>
              </div>
            ))}
          </dl>
          <p className="mt-4 text-sm leading-6 text-[var(--muted)]">
            Hiring bar gap:{" "}
            <span className="font-semibold text-red-200">
              {mockBenchmarkComparison.hiringBarGap.toUpperCase()}
            </span>
          </p>
        </aside>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-5 px-6 pb-8 lg:grid-cols-2">
        <AnswerSummary title="Strongest answer" feedback={strongestAnswer} tone="strong" />
        <AnswerSummary title="Weakest answer" feedback={weakestAnswer} tone="risk" />
      </section>

      <section className="mx-auto w-full max-w-6xl px-6 pb-8">
        <div className="rounded border border-[var(--border)] bg-black/20 p-5">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold">Answer-by-answer feedback preview</h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--muted)]">
                Each answer is scored against the question target and the benchmark gap it was
                meant to validate.
              </p>
            </div>
            <Link
              href="/setup"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black"
            >
              Try real setup flow
            </Link>
          </div>

          <div className="mt-5 grid gap-4 lg:grid-cols-3">
            {mockFinalReport.answerFeedback.map((feedback) => (
              <article key={feedback.questionId} className="rounded border border-[var(--border)] p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="text-sm font-medium">Question {feedback.questionNumber}</div>
                  <div className="rounded border border-[var(--border)] px-2 py-1 text-xs">
                    {feedback.score}/100
                  </div>
                </div>
                <div className="mt-3 text-xs uppercase text-[var(--muted)]">
                  {formatLabel(feedback.category)}
                </div>
                <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                  {feedback.strictFeedback}
                </p>
                <div className="mt-4 rounded border border-[var(--border)] bg-black/20 p-3">
                  <div className="text-xs uppercase text-[var(--muted)]">Benchmark gap coverage</div>
                  <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
                    {feedback.benchmarkGapCoverage}
                  </p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-5 px-6 pb-8 lg:grid-cols-[1fr_360px]">
        <section className="rounded border border-[var(--border)] bg-black/20 p-5">
          <h2 className="text-lg font-semibold">Resume improvement suggestions</h2>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
            The resume needs stronger benchmark-style evidence before applying: metrics, scope,
            ownership, and impact.
          </p>

          <div className="mt-5 grid gap-4">
            <ResumeBulletCard label="Weak resume bullet" value={mockFinalReport.resumeBulletUpgrade.weakBullet} />
            <ResumeBulletCard
              label="Benchmark-style improved bullet"
              value={mockFinalReport.resumeBulletUpgrade.improvedBullet}
              accented
            />
            <ResumeBulletCard
              label="Missing evidence or metric"
              value={mockFinalReport.resumeBulletUpgrade.missingEvidenceExplanation}
            />
          </div>
        </section>

        <aside className="rounded border border-[var(--border)] bg-black/20 p-5">
          <h2 className="text-lg font-semibold">Top improvement priorities</h2>
          <ul className="mt-4 space-y-3">
            {mockFinalReport.topImprovementPriorities.map((priority) => (
              <li key={priority} className="rounded border border-[var(--border)] bg-black/20 p-3 text-sm leading-6">
                {priority}
              </li>
            ))}
          </ul>
        </aside>
      </section>

      <section className="mx-auto w-full max-w-6xl px-6 pb-14">
        <div className="rounded border border-[var(--border)] bg-black/20 p-5">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold">7-day preparation plan</h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--muted)]">
                Practice before applying by closing the highest-risk benchmark gaps first.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link href="/demo/interview" className="rounded border border-[var(--border)] px-4 py-2 text-sm">
                Back to interview
              </Link>
              <Link href="/demo" className="rounded border border-[var(--border)] px-4 py-2 text-sm">
                Back to demo
              </Link>
            </div>
          </div>

          <ol className="mt-5 grid gap-3 md:grid-cols-2 lg:grid-cols-4">
            {mockFinalReport.preparationPlan.map((item, index) => (
              <li key={item} className="rounded border border-[var(--border)] bg-black/20 p-4">
                <div className="text-xs uppercase text-[var(--accent)]">Day {index + 1}</div>
                <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{item}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>
    </main>
  );
}

function ScoreCard({ label, value, detail }: { label: string; value: number; detail: string }) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="text-xs uppercase text-[var(--muted)]">{label}</div>
      <div className="mt-2 text-3xl font-semibold">{value}/100</div>
      <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{detail}</p>
    </section>
  );
}

function AnswerSummary({
  title,
  feedback,
  tone,
}: {
  title: string;
  feedback: (typeof mockFinalReport.answerFeedback)[number];
  tone: "strong" | "risk";
}) {
  const toneClass = tone === "strong" ? "text-[var(--accent)]" : "text-red-200";

  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="text-xs uppercase text-[var(--muted)]">{title}</div>
      <div className={`mt-2 text-3xl font-semibold ${toneClass}`}>{feedback.score}/100</div>
      <div className="mt-2 text-sm">Question {feedback.questionNumber}</div>
      <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{feedback.strictFeedback}</p>
      <p className="mt-3 rounded border border-[var(--border)] bg-black/20 p-3 text-sm leading-6 text-[var(--muted)]">
        {feedback.benchmarkGapCoverage}
      </p>
    </section>
  );
}

function ResumeBulletCard({
  label,
  value,
  accented,
}: {
  label: string;
  value: string;
  accented?: boolean;
}) {
  return (
    <div className="rounded border border-[var(--border)] bg-black/20 p-4">
      <div className={`text-xs uppercase ${accented ? "text-[var(--accent)]" : "text-[var(--muted)]"}`}>
        {label}
      </div>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{value}</p>
    </div>
  );
}

function formatRecommendation(value: string) {
  return value.replaceAll("_", " ").toUpperCase();
}

function formatLabel(value: string) {
  return value.replaceAll("_", " ");
}
