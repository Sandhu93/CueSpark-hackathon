"use client";

import type { AgentResultRead, AgentType, CandidateAnswerRead } from "@/lib/types";

const agentLabels: Record<AgentType, string> = {
  audio: "Audio agent",
  video_signal: "Visual signal agent",
  text_answer: "Text answer agent",
  code_evaluation: "Code evaluation agent",
  benchmark_gap: "Benchmark gap agent",
  final_orchestrator: "Final evaluation",
};

const agentDescriptions: Record<AgentType, string> = {
  audio: "Transcript, speaking pace, filler words, and answer structure.",
  video_signal: "Observable visual signal metadata such as face in frame and lighting quality.",
  text_answer: "Relevance, evidence, specificity, completeness, and clarity.",
  code_evaluation: "Static code review for correctness, edge cases, complexity, and readability.",
  benchmark_gap: "Whether the answer addressed the benchmark gap being tested.",
  final_orchestrator: "Final answer-level score and strict feedback.",
};

export function AgentStatusPanel({
  answer,
  agentResults,
  onRefresh,
}: {
  answer: CandidateAnswerRead;
  agentResults: AgentResultRead[];
  onRefresh?: () => void;
}) {
  const relevantAgents = getRelevantAgents(answer, agentResults);

  return (
    <section className="rounded border border-[var(--border)] p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h4 className="text-sm font-semibold">Evaluation pipeline</h4>
          <p className="mt-1 text-sm text-[var(--muted)]">
            CueSpark runs only the agents relevant to this answer mode.
          </p>
        </div>
        {onRefresh && (
          <button
            onClick={onRefresh}
            className="rounded border border-[var(--border)] px-3 py-1 text-xs text-[var(--muted)]"
          >
            Refresh
          </button>
        )}
      </div>

      <div className="mt-4 space-y-2">
        {relevantAgents.map((agentType) => {
          const result = agentResults.find((item) => item.agent_type === agentType);
          const status = result?.status ?? "pending";
          return (
            <div
              key={agentType}
              className="grid gap-3 rounded border border-[var(--border)] bg-white/5 p-3 sm:grid-cols-[1fr_auto]"
            >
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-medium">{agentLabels[agentType]}</span>
                  <StatusPill status={status} />
                </div>
                <p className="mt-1 text-xs leading-5 text-[var(--muted)]">
                  {agentDescriptions[agentType]}
                </p>
              </div>
              <div className="text-sm text-[var(--muted)]">
                {result?.score !== null && result?.score !== undefined
                  ? `${result.score}/10`
                  : "No score yet"}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function getRelevantAgents(answer: CandidateAnswerRead, agentResults: AgentResultRead[]): AgentType[] {
  const agents = new Set<AgentType>();

  if (answer.answer_mode === "spoken_answer" || answer.answer_mode === "mixed_answer") {
    agents.add("audio");
  }
  if (answer.answer_mode === "written_answer" || answer.text_answer) {
    agents.add("text_answer");
  }
  if (answer.answer_mode === "code_answer" || answer.code_answer) {
    agents.add("code_evaluation");
  }
  if (hasVisualSignalMetadata(answer.visual_signal_metadata)) {
    agents.add("video_signal");
  }

  agentResults.forEach((result) => agents.add(result.agent_type));
  agents.add("benchmark_gap");
  agents.add("final_orchestrator");

  return Array.from(agents);
}

function hasVisualSignalMetadata(value: CandidateAnswerRead["visual_signal_metadata"]) {
  return Boolean(value && Object.keys(value).length > 0);
}

function StatusPill({ status }: { status: AgentResultRead["status"] | "pending" }) {
  const className =
    status === "succeeded"
      ? "border-emerald-400/40 text-emerald-200"
      : status === "failed"
        ? "border-red-400/40 text-red-200"
        : status === "running"
          ? "border-yellow-300/40 text-yellow-100"
          : "border-[var(--border)] text-[var(--muted)]";

  return (
    <span className={`rounded-full border px-2 py-0.5 text-xs capitalize ${className}`}>
      {status}
    </span>
  );
}
