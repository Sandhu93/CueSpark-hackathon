"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import type React from "react";
import { useCallback, useEffect, useMemo, useState } from "react";

import { CodeAnswerCapture } from "@/components/interview/CodeAnswerCapture";
import { SpokenAnswerCapture } from "@/components/interview/SpokenAnswerCapture";
import { WrittenAnswerCapture } from "@/components/interview/WrittenAnswerCapture";
import { NoticePanel, SafetyCopy } from "@/components/product/NoticePanel";
import { SessionNav } from "@/components/product/SessionNav";
import { api } from "@/lib/api";
import type { QuestionRead, ResponseMode, SessionRead } from "@/lib/types";

type LoadState = "idle" | "loading" | "ready" | "error";
type EvaluationState = "not_submitted" | "submitted" | "processing" | "running_agents" | "evaluated" | "failed";

const responseModeLabels: Record<ResponseMode, string> = {
  spoken_answer: "Spoken answer",
  written_answer: "Written answer",
  code_answer: "Code answer",
  mixed_answer: "Mixed response",
};

export default function InterviewRoomPage() {
  const params = useParams<{ sessionId: string }>();
  const sessionId = params.sessionId;
  const [session, setSession] = useState<SessionRead | null>(null);
  const [questions, setQuestions] = useState<QuestionRead[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loadState, setLoadState] = useState<LoadState>("loading");
  const [error, setError] = useState<string | null>(null);
  const [ttsUrlByQuestionId, setTtsUrlByQuestionId] = useState<Record<string, string>>({});
  const [ttsLoading, setTtsLoading] = useState(false);
  const [ttsError, setTtsError] = useState<string | null>(null);
  const [evaluationState] = useState<EvaluationState>("not_submitted");

  const loadInterview = useCallback(
    async (active = true) => {
      setLoadState("loading");
      try {
        const [nextSession, questionResponse] = await Promise.all([
          api.getSession(sessionId),
          api.listQuestions(sessionId),
        ]);
        if (!active) return;
        setSession(nextSession);
        setQuestions(questionResponse.questions);
        setCurrentIndex(
          clampIndex(nextSession.current_question_index ?? 0, questionResponse.questions.length),
        );
        setError(null);
        setLoadState("ready");
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "Unable to load interview room");
        setLoadState("error");
      }
    },
    [sessionId],
  );

  useEffect(() => {
    let active = true;
    loadInterview(active);
    return () => {
      active = false;
    };
  }, [loadInterview]);

  const currentQuestion = questions[currentIndex] ?? null;
  const progressText = useMemo(() => {
    if (!currentQuestion) return "No question selected";
    return `Question ${currentIndex + 1} of ${questions.length}`;
  }, [currentIndex, currentQuestion, questions.length]);

  async function handleGenerateTts() {
    if (!currentQuestion) return;
    setTtsLoading(true);
    setTtsError(null);
    try {
      const result = await api.generateQuestionTts(currentQuestion.id);
      setTtsUrlByQuestionId((existing) => ({
        ...existing,
        [currentQuestion.id]: result.audio_url,
      }));
    } catch (err) {
      setTtsError(err instanceof Error ? err.message : "Unable to generate interviewer audio");
    } finally {
      setTtsLoading(false);
    }
  }

  function handlePlayTts() {
    if (!currentQuestion) return;
    const audioUrl = ttsUrlByQuestionId[currentQuestion.id] ?? currentQuestion.tts_audio_url;
    if (!audioUrl) return;
    const audio = new Audio(audioUrl);
    void audio.play().catch((err) => {
      setTtsError(err instanceof Error ? err.message : "Unable to play interviewer audio");
    });
  }

  return (
    <main className="mx-auto min-h-screen w-full max-w-6xl px-6 py-8">
      <header className="mb-6 border-b border-[var(--border)] pb-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <SessionNav sessionId={sessionId} active="interview" />
          <div className="rounded border border-[var(--border)] px-3 py-1 text-xs text-[var(--muted)]">
            {session?.status ? `Session ${session.status}` : "Loading session"}
          </div>
        </div>
        <div className="mt-5 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-[var(--accent)]">{progressText}</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight">Interview room</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-[var(--muted)]">
              Answer each benchmark-driven question in the response mode requested by the
              interview plan.
            </p>
          </div>
          {currentQuestion && (
            <ModePill responseMode={currentQuestion.response_mode} />
          )}
        </div>
      </header>

      {loadState === "loading" && <StatePanel>Loading interview questions...</StatePanel>}
      {loadState === "error" && error && (
        <NoticePanel
          title="Questions unavailable"
          tone="error"
          action={
            <>
              <button
                onClick={() => void loadInterview()}
                className="rounded border border-red-300/40 px-3 py-2 text-xs"
              >
                Refresh status
              </button>
              <Link
                href={`/session/${sessionId}/benchmark`}
                className="rounded border border-red-300/40 px-3 py-2 text-xs"
              >
                Back to benchmark dashboard
              </Link>
            </>
          }
        >
          {error}
        </NoticePanel>
      )}

      {loadState === "ready" && questions.length === 0 && (
        <NoticePanel
          title="No questions available"
          action={
            <>
              <button
                onClick={() => void loadInterview()}
                className="rounded border border-[var(--border)] px-3 py-2 text-xs"
              >
                Refresh status
              </button>
              <Link
                href={`/session/${sessionId}/match`}
                className="rounded border border-[var(--border)] px-3 py-2 text-xs"
              >
                Retry preparation
              </Link>
            </>
          }
        >
          No interview questions are available yet. Prepare the session first, then return to
          this room.
        </NoticePanel>
      )}

      {currentQuestion && (
        <div className="grid gap-5 lg:grid-cols-[1.35fr_0.85fr]">
          <section className="space-y-5">
            <QuestionPanel question={currentQuestion} />
            <ResponseCapturePanel question={currentQuestion} />
          </section>

          <aside className="space-y-5">
            <VoicePanel
              audioAvailable={Boolean(
                ttsUrlByQuestionId[currentQuestion.id] ?? currentQuestion.tts_audio_url,
              )}
              loading={ttsLoading}
              error={ttsError}
              onGenerate={handleGenerateTts}
              onPlay={handlePlayTts}
            />
            <EvaluationStatusPanel state={evaluationState} />
            <QuestionNavigation
              currentIndex={currentIndex}
              total={questions.length}
              reportHref={`/session/${sessionId}/report`}
              onPrevious={() => setCurrentIndex((index) => Math.max(0, index - 1))}
              onNext={() =>
                setCurrentIndex((index) => Math.min(questions.length - 1, index + 1))
              }
            />
          </aside>
        </div>
      )}
    </main>
  );
}

function QuestionPanel({ question }: { question: QuestionRead }) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="flex flex-wrap gap-2 text-xs">
        <Tag>{question.category.replaceAll("_", " ")}</Tag>
        <Tag>{question.difficulty ?? "difficulty pending"}</Tag>
        <Tag>{question.source.replaceAll("_", " ")}</Tag>
      </div>
      <h2 className="mt-4 text-2xl font-semibold leading-snug">{question.question_text}</h2>
      <InfoBlock title="Expected signal">
        {question.expected_signal || "No expected signal was returned for this question."}
      </InfoBlock>
      <InfoBlock title="Why this was asked">
        {question.why_this_was_asked ||
          "CueSpark generated this question from the session context and benchmark plan."}
      </InfoBlock>
      <div className="mt-5">
        <h3 className="text-sm font-semibold">Benchmark gap references</h3>
        {question.benchmark_gap_refs.length === 0 ? (
          <p className="mt-2 text-sm text-[var(--muted)]">No benchmark gap references returned.</p>
        ) : (
          <div className="mt-3 flex flex-wrap gap-2">
            {question.benchmark_gap_refs.map((ref, index) => (
              <span
                key={`${String(ref)}-${index}`}
                className="rounded-full border border-[var(--border)] px-3 py-1 text-xs text-[var(--muted)]"
              >
                {String(ref)}
              </span>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

function VoicePanel({
  audioAvailable,
  loading,
  error,
  onGenerate,
  onPlay,
}: {
  audioAvailable: boolean;
  loading: boolean;
  error: string | null;
  onGenerate: () => void;
  onPlay: () => void;
}) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">AI interviewer voice</h2>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
        Generate interviewer audio for this question, then play it before answering.
      </p>
      <div className="mt-4 flex flex-wrap gap-3">
        <button
          onClick={onGenerate}
          disabled={loading}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Generating..." : error ? "Retry TTS" : audioAvailable ? "Regenerate audio" : "Generate audio"}
        </button>
        <button
          onClick={onPlay}
          disabled={!audioAvailable}
          className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          Play audio
        </button>
      </div>
      {error && <p className="mt-3 text-sm text-red-200">{error}</p>}
    </section>
  );
}

function ResponseCapturePanel({ question }: { question: QuestionRead }) {
  const mode = question.response_mode;
  const showSpoken = question.requires_audio || mode === "spoken_answer" || mode === "mixed_answer";
  const showWritten = question.requires_text || mode === "written_answer" || mode === "mixed_answer";
  const showCode = question.requires_code || mode === "code_answer" || mode === "mixed_answer";
  const showVisual = question.requires_video;

  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-sm font-semibold">Response capture</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            Required mode: {responseModeLabels[mode]}
          </p>
        </div>
        <ModePill responseMode={mode} />
      </div>

      <div className="mt-5 grid gap-4">
        {showSpoken && (
          <SpokenAnswerCapture key={`spoken-${question.id}`} questionId={question.id} />
        )}
        {showWritten && (
          <WrittenAnswerCapture
            key={`written-${question.id}`}
            questionId={question.id}
            questionText={question.question_text}
          />
        )}
        {showCode && (
          <CodeAnswerCapture
            key={`code-${question.id}`}
            questionId={question.id}
            questionText={question.question_text}
          />
        )}
        {showVisual && (
          <CapturePlaceholder
            title="Visual signal metadata"
            status="Optional MVP"
            description="Future frontend capture can provide safe visual presence metadata. This page does not request camera access."
          />
        )}
        {(showSpoken || showVisual) && <SafetyCopy />}
      </div>
    </section>
  );
}

function EvaluationStatusPanel({ state }: { state: EvaluationState }) {
  const steps: { key: EvaluationState; label: string }[] = [
    { key: "not_submitted", label: "Not submitted" },
    { key: "submitted", label: "Submitted" },
    { key: "processing", label: "Processing" },
    { key: "running_agents", label: "Running agents" },
    { key: "evaluated", label: "Evaluated" },
    { key: "failed", label: "Failed" },
  ];

  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">Evaluation status</h2>
      <div className="mt-4 space-y-2">
        {steps.map((step) => (
          <div
            key={step.key}
            className={`rounded border px-3 py-2 text-sm ${
              step.key === state
                ? "border-[var(--accent)] text-[var(--fg)]"
                : "border-[var(--border)] text-[var(--muted)]"
            }`}
          >
            {step.label}
          </div>
        ))}
      </div>
    </section>
  );
}

function QuestionNavigation({
  currentIndex,
  total,
  reportHref,
  onPrevious,
  onNext,
}: {
  currentIndex: number;
  total: number;
  reportHref: string;
  onPrevious: () => void;
  onNext: () => void;
}) {
  const isFinalQuestion = total > 0 && currentIndex === total - 1;

  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">Question navigation</h2>
      <p className="mt-2 text-sm text-[var(--muted)]">
        {total === 0 ? "No questions" : `${currentIndex + 1} of ${total}`}
      </p>
      <div className="mt-4 flex gap-3">
        <button
          onClick={onPrevious}
          disabled={currentIndex === 0}
          className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          Previous
        </button>
        {isFinalQuestion ? (
          <Link
            href={reportHref}
            className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black"
          >
            Finish interview & open report
          </Link>
        ) : (
          <button
            onClick={onNext}
            disabled={total === 0}
            className="rounded border border-[var(--border)] px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
          >
            Next
          </button>
        )}
      </div>
    </section>
  );
}

function CapturePlaceholder({
  title,
  status,
  description,
}: {
  title: string;
  status: string;
  description: string;
}) {
  return (
    <div className="rounded border border-[var(--border)] p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h3 className="font-medium">{title}</h3>
        <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-[var(--muted)]">
          {status}
        </span>
      </div>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{description}</p>
    </div>
  );
}

function InfoBlock({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mt-5 rounded border border-[var(--border)] p-4">
      <h3 className="text-sm font-semibold">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{children}</p>
    </div>
  );
}

function Tag({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded-full border border-[var(--border)] px-3 py-1 text-[var(--muted)]">
      {children}
    </span>
  );
}

function ModePill({ responseMode }: { responseMode: ResponseMode }) {
  return (
    <div className="rounded-full border border-[var(--accent)] px-4 py-2 text-sm font-semibold text-[var(--accent)]">
      {responseModeLabels[responseMode]}
    </div>
  );
}

function StatePanel({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded border border-[var(--border)] bg-black/20 p-5 text-sm leading-6 text-[var(--muted)]">
      {children}
    </div>
  );
}

function ErrorPanel({ message }: { message: string }) {
  return (
    <div className="rounded border border-red-500/40 bg-red-500/10 p-5 text-sm text-red-200">
      {message}
    </div>
  );
}

function clampIndex(index: number, total: number) {
  if (total <= 0) return 0;
  return Math.min(Math.max(index, 0), total - 1);
}
