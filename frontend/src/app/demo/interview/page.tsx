import Link from "next/link";

import {
  mockAnswerTranscript,
  mockCommunicationSignals,
  mockInterviewQuestions,
  mockSession,
} from "@/lib/demo/mock-data";

const currentQuestion = mockInterviewQuestions[0];

const signalRows = [
  ["Face in frame", mockCommunicationSignals.faceInFrame],
  ["Lighting quality", mockCommunicationSignals.lightingQuality],
  ["Eye contact proxy", mockCommunicationSignals.eyeContactProxy],
  ["Posture stability", mockCommunicationSignals.postureStability],
  ["Speaking pace", `${mockCommunicationSignals.speakingPaceWpm} wpm`],
  ["Filler words", `${mockCommunicationSignals.fillerWordCount} counted`],
  ["Answer structure", mockCommunicationSignals.answerStructure],
];

const waveformBars = [32, 48, 24, 68, 54, 38, 74, 42, 58, 28, 64, 46, 34, 72, 50, 30];

export default function DemoInterviewPage() {
  return (
    <main className="min-h-screen">
      <section className="border-b border-[var(--border)]">
        <div className="mx-auto w-full max-w-6xl px-6 py-8">
          <nav className="mb-8 flex flex-wrap items-center gap-4 text-sm">
            <Link href="/demo" className="text-[var(--muted)]">
              Demo
            </Link>
            <Link href="/demo/benchmark" className="text-[var(--muted)]">
              Benchmark dashboard
            </Link>
          </nav>

          <div className="flex flex-wrap items-end justify-between gap-5">
            <div>
              <div className="inline-flex rounded border border-[var(--border)] bg-black/30 px-3 py-1 text-xs font-medium text-[var(--accent)]">
                {mockSession.demoModeLabel}
              </div>
              <h1 className="mt-5 text-4xl font-semibold tracking-tight sm:text-5xl">
                Benchmark-Driven Interview Room
              </h1>
              <p className="mt-4 max-w-3xl text-base leading-7 text-[var(--muted)]">
                A simulated interview room showing how CueSpark turns benchmark gaps into
                strict interviewer questions, observable communication signals, and report-ready
                feedback.
              </p>
            </div>
            <Link
              href="/demo/report"
              className="rounded bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-black"
            >
              Continue to demo report
            </Link>
          </div>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-5 px-6 py-8 lg:grid-cols-[1fr_360px]">
        <div className="space-y-5">
          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <div className="text-xs uppercase text-[var(--muted)]">AI Interviewer Panel</div>
                <h2 className="mt-2 text-2xl font-semibold">
                  Question {currentQuestion.questionNumber}
                </h2>
              </div>
              <button
                type="button"
                className="rounded border border-[var(--border)] px-4 py-2 text-sm text-[var(--muted)]"
                aria-label="Mock play interviewer voice"
              >
                Play interviewer voice
              </button>
            </div>

            <div className="mt-5 flex flex-wrap gap-2 text-xs">
              <Badge>{formatLabel(currentQuestion.category)}</Badge>
              <Badge>{currentQuestion.difficulty}</Badge>
              <Badge>benchmark-driven</Badge>
            </div>

            <p className="mt-6 text-xl leading-8">{currentQuestion.questionText}</p>

            <div className="mt-6 rounded border border-[var(--border)] p-4">
              <div className="text-xs uppercase text-[var(--muted)]">Expected signal</div>
              <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
                {currentQuestion.expectedSignal}
              </p>
            </div>
          </section>

          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-lg font-semibold">Why this question was asked</h2>
            <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
              {currentQuestion.whyThisWasAsked}
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              {currentQuestion.benchmarkGapRefs.map((gap) => (
                <span
                  key={gap}
                  className="rounded border border-[var(--border)] bg-black/30 px-3 py-1 text-xs text-[var(--accent)]"
                >
                  {gap}
                </span>
              ))}
            </div>
          </section>

          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-semibold">Mock answer transcript preview</h2>
                <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
                  Sample candidate response. Detailed feedback is summarized in the final report.
                </p>
              </div>
              <Badge>{mockAnswerTranscript.addressedBenchmarkGap ? "gap addressed" : "gap missed"}</Badge>
            </div>
            <p className="mt-4 rounded border border-[var(--border)] bg-black/20 p-4 text-sm leading-6 text-[var(--muted)]">
              {mockAnswerTranscript.transcript}
            </p>
            <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
              {mockAnswerTranscript.evaluationPreview}
            </p>
          </section>
        </div>

        <aside className="space-y-5">
          <section className="overflow-hidden rounded border border-[var(--border)] bg-black/20">
            <div className="flex items-center justify-between border-b border-[var(--border)] px-4 py-3">
              <div className="text-sm font-medium">{mockSession.candidateName}</div>
              <div className="rounded bg-red-500/15 px-2 py-1 text-xs text-red-200">
                Simulated recording - 02:14
              </div>
            </div>
            <div className="relative flex aspect-video items-center justify-center bg-black/50">
              <div className="absolute left-4 top-4 rounded bg-black/60 px-2 py-1 text-xs text-[var(--muted)]">
                Static mock video tile
              </div>
              <div className="flex h-24 w-24 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--bg)] text-3xl font-semibold">
                DC
              </div>
            </div>
            <div className="border-t border-[var(--border)] p-4">
              <div className="mb-3 text-xs uppercase text-[var(--muted)]">Mock answer waveform</div>
              <div className="flex h-20 items-end gap-1 rounded border border-[var(--border)] bg-black/20 p-3">
                {waveformBars.map((height, index) => (
                  <div
                    key={`${height}-${index}`}
                    className="w-full rounded bg-[var(--accent)]/70"
                    style={{ height: `${height}%` }}
                  />
                ))}
              </div>
            </div>
          </section>

          <section className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-lg font-semibold">Communication signals</h2>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
              Observable communication signals only - no emotion or true-confidence detection.
            </p>
            <dl className="mt-4 space-y-3">
              {signalRows.map(([label, value]) => (
                <div
                  key={label}
                  className="flex items-center justify-between gap-4 rounded border border-[var(--border)] px-3 py-2 text-sm"
                >
                  <dt className="text-[var(--muted)]">{label}</dt>
                  <dd className="font-medium">{formatLabel(value)}</dd>
                </div>
              ))}
            </dl>
            <p className="mt-4 text-xs leading-5 text-[var(--muted)]">
              {mockCommunicationSignals.signalExplanation}
            </p>
          </section>
        </aside>
      </section>
    </main>
  );
}

function Badge({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded border border-[var(--border)] bg-black/30 px-3 py-1 text-xs text-[var(--muted)]">
      {children}
    </span>
  );
}

function formatLabel(value: string) {
  return value.replaceAll("_", " ");
}
