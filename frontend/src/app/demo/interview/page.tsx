import Link from "next/link";

import { ProgressBar } from "@/components/demo/dashboard-widgets";
import {
  mockAnswerTranscript,
  mockCommunicationSignals,
  mockInterviewQuestions,
  mockInterviewRoomData,
  mockSession,
} from "@/lib/demo/mock-data";

const currentQuestion = mockInterviewQuestions[0];

const signalRows = [
  ["Face in Frame", "Good", 86, "green"],
  ["Lighting Quality", "Good", 82, "green"],
  ["Eye Contact Proxy", formatLabel(mockCommunicationSignals.eyeContactProxy), 58, "amber"],
  ["Posture Stability", formatLabel(mockCommunicationSignals.postureStability), 78, "green"],
  ["Speaking Pace", `${mockCommunicationSignals.speakingPaceWpm} wpm`, 66, "amber"],
  ["Filler Words", `${mockCommunicationSignals.fillerWordCount} counted`, 46, "amber"],
  ["Answer Structure", formatLabel(mockCommunicationSignals.answerStructure), 74, "blue"],
] satisfies Array<[string, string, number, "green" | "amber" | "blue"]>;

export default function DemoInterviewPage() {
  return (
    <main className="min-h-screen px-4 py-4 lg:px-8">
      <section className="mb-4 rounded-lg bg-[#061a38] px-5 py-4 text-white shadow-sm">
        <div className="grid gap-4 lg:grid-cols-[1fr_1fr_1fr] lg:items-center">
          <div>
            <div className="flex items-center gap-2 text-sm font-semibold">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
              Interview in Progress
            </div>
            <div className="mt-2 text-sm text-blue-100">Mock timer: {mockInterviewRoomData.mockTimer}</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold">AI Interviewer</div>
            <div className="mt-1 text-sm text-blue-100">{mockInterviewRoomData.interviewerPanel}</div>
          </div>
          <div className="lg:text-right">
            <div className="text-sm font-semibold">
              Question {mockInterviewRoomData.currentQuestionNumber} of {mockInterviewRoomData.totalQuestions}
            </div>
            <div className="mt-3 flex gap-2 lg:justify-end">
              {Array.from({ length: mockInterviewRoomData.totalQuestions }).map((_, index) => (
                <span
                  key={index}
                  className={`h-2 w-10 rounded-full ${
                    index < mockInterviewRoomData.currentQuestionNumber ? "bg-blue-500" : "bg-white/20"
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-4 xl:grid-cols-[0.9fr_1.15fr_0.72fr]">
        <div className="space-y-4">
          <section className="rounded-lg border border-[var(--border)] bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white">
                  AI
                </div>
                <div>
                  <h1 className="text-base font-semibold text-slate-900">AI Interviewer</h1>
                  <div className="text-xs text-[var(--muted)]">Benchmark-driven question</div>
                </div>
              </div>
              <span className="rounded-full bg-red-50 px-3 py-1 text-xs font-semibold text-red-700">
                Strict Mode
              </span>
            </div>
            <div className="relative mt-5 rounded-lg bg-[#061a38] p-5 text-white">
              <div className="absolute -right-2 top-1/2 h-4 w-4 -translate-y-1/2 rotate-45 bg-[#061a38]" />
              <p className="text-lg font-semibold leading-8">{currentQuestion.questionText}</p>
              <div className="mt-6 text-sm leading-6 text-blue-100">
                Follow-up likely: {mockInterviewRoomData.likelyFollowUp}
              </div>
            </div>
            <div className="mt-5 flex flex-wrap gap-2">
              <Badge>{formatLabel(currentQuestion.category)}</Badge>
              <Badge>{currentQuestion.difficulty}</Badge>
              <Badge>expected signal: {currentQuestion.expectedSignal}</Badge>
            </div>
          </section>

          <section className="rounded-lg border border-[var(--border)] bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-base font-semibold text-slate-900">Live Transcript</h2>
              <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                Mocked
              </span>
            </div>
            <div className="mt-5 space-y-4">
              {mockInterviewRoomData.transcriptLines.map((line) => (
                <div key={line.time} className="grid grid-cols-[48px_1fr] gap-3 text-sm">
                  <span className="text-[var(--muted)]">{line.time}</span>
                  <span className="text-slate-700">{line.text}</span>
                </div>
              ))}
            </div>
            <div className="mt-8 flex items-center gap-3 text-sm text-blue-700">
              <span className="h-4 w-4 rounded-full border-2 border-blue-600 border-t-transparent" />
              AI is analyzing the mock response for the final report preview.
            </div>
          </section>
        </div>

        <div className="space-y-4">
          <section className="overflow-hidden rounded-lg border border-[var(--border)] bg-white shadow-sm">
            <div className="relative flex aspect-video items-center justify-center overflow-hidden bg-gradient-to-br from-slate-300 via-slate-200 to-slate-400">
              <div className="absolute left-4 top-4 rounded bg-black/70 px-3 py-1 text-xs font-semibold text-white">
                You
              </div>
              <div className="absolute right-4 top-4 rounded bg-black/70 px-3 py-1 text-xs font-semibold text-white">
                ● REC
              </div>
              <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/40 to-transparent" />
              <div className="relative flex h-40 w-40 items-center justify-center rounded-full bg-slate-900 text-5xl font-semibold text-white shadow-2xl">
                DC
              </div>
              <div className="absolute bottom-4 left-4 rounded bg-white/90 px-3 py-2 text-xs font-semibold text-slate-700">
                Static mock video tile - no camera access
              </div>
            </div>
          </section>

          <section className="rounded-lg border border-[var(--border)] bg-white p-5 shadow-sm">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h2 className="text-base font-semibold text-slate-900">{mockInterviewRoomData.workspaceTitle}</h2>
                <p className="mt-1 text-sm text-[var(--muted)]">
                  Choose the best structure for the answer. This is static and does not execute.
                </p>
              </div>
              <div className="flex gap-2 text-xs">
                <span className="rounded-md bg-blue-50 px-3 py-2 font-semibold text-blue-700">
                  {mockInterviewRoomData.workspaceMode}
                </span>
                <span className="rounded-md border border-[var(--border)] px-3 py-2 text-slate-600">
                  {mockInterviewRoomData.workspaceLanguage}
                </span>
              </div>
            </div>
            <pre className="mt-4 min-h-44 overflow-x-auto rounded-lg bg-slate-950 p-4 text-sm leading-7 text-blue-50">
              {mockInterviewRoomData.workspaceContent}
            </pre>
          </section>

          <section className="rounded-lg border border-[var(--border)] bg-white p-5 shadow-sm">
            <h2 className="text-base font-semibold text-slate-900">Why this question was asked</h2>
            <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{currentQuestion.whyThisWasAsked}</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {currentQuestion.benchmarkGapRefs.map((gap) => (
                <span key={gap} className="rounded-full bg-violet-50 px-3 py-1 text-xs font-semibold text-violet-700">
                  {gap}
                </span>
              ))}
            </div>
          </section>
        </div>

        <aside className="space-y-4">
          <section className="rounded-lg border border-[var(--border)] bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="text-base font-semibold text-slate-900">Communication Signals</h2>
                <p className="mt-1 text-xs text-[var(--muted)]">Observable only</p>
              </div>
              <span className="rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-700">i</span>
            </div>
            <div className="mt-5 space-y-4">
              {signalRows.map(([label, value, score, tone]) => (
                <div key={label}>
                  <div className="mb-2 flex items-center justify-between gap-3 text-sm">
                    <span className="font-medium text-slate-700">{label}</span>
                    <span className={tone === "green" ? "text-emerald-600" : tone === "amber" ? "text-amber-600" : "text-blue-600"}>
                      {value}
                    </span>
                  </div>
                  <ProgressBar value={score} tone={tone} />
                </div>
              ))}
            </div>
            <p className="mt-5 rounded-md bg-slate-50 p-3 text-xs leading-5 text-[var(--muted)]">
              Observable communication signals only - no emotion or true-confidence detection.
            </p>
          </section>

          <section className="rounded-lg border border-[var(--border)] bg-white p-5 shadow-sm">
            <h2 className="text-base font-semibold text-slate-900">Mock answer preview</h2>
            <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{mockAnswerTranscript.evaluationPreview}</p>
            <Link href="/demo/report" className="mt-5 inline-flex rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white">
              Continue to report
            </Link>
          </section>
        </aside>
      </section>

      <section className="sticky bottom-3 z-10 mt-4 rounded-lg bg-[#061a38] p-3 text-white shadow-xl">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap gap-2">
            {mockInterviewRoomData.bottomControls.slice(0, 4).map((control) => (
              <MockControl key={control.label} {...control} />
            ))}
          </div>
          <button type="button" className="rounded-md bg-red-500 px-8 py-3 text-sm font-semibold text-white">
            End Interview
          </button>
          <div className="flex flex-wrap gap-2">
            {mockInterviewRoomData.bottomControls.slice(4).map((control) => (
              <MockControl key={control.label} {...control} />
            ))}
          </div>
        </div>
        <div className="mt-3 text-xs text-blue-100">
          Tip: Structure your answer with context - action - impact - learnings. All controls are static mock UI.
        </div>
      </section>
    </main>
  );
}

function Badge({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
      {children}
    </span>
  );
}

function MockControl({ label, token }: { label: string; token: string }) {
  return (
    <button type="button" className="rounded-md px-3 py-2 text-center text-xs text-blue-100 hover:bg-white/10">
      <span className="block font-semibold text-white">{token}</span>
      <span>{label}</span>
    </button>
  );
}

function formatLabel(value: string) {
  return value.replaceAll("_", " ");
}
