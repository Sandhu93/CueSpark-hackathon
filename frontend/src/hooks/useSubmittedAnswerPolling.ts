"use client";

import { useEffect, useState } from "react";

import { api } from "@/lib/api";
import type { CandidateAnswerRead } from "@/lib/types";

export type AnswerProcessingState =
  | "idle"
  | "editing"
  | "uploading"
  | "processing"
  | "running_agents"
  | "evaluated"
  | "failed";

export function useSubmittedAnswerPolling(answerId: string | null) {
  const [answer, setAnswer] = useState<CandidateAnswerRead | null>(null);
  const [state, setState] = useState<AnswerProcessingState>("idle");

  async function refresh() {
    if (!answerId) return;
    const nextAnswer = await api.getAnswer(answerId);
    setAnswer(nextAnswer);
    setState(classifyAnswerState(nextAnswer));
  }

  useEffect(() => {
    if (!answerId || state === "evaluated" || state === "failed") return;
    const submittedAnswerId = answerId;
    let active = true;

    async function loadAnswer() {
      try {
        const nextAnswer = await api.getAnswer(submittedAnswerId);
        if (!active) return;
        setAnswer(nextAnswer);
        setState(classifyAnswerState(nextAnswer));
      } catch {
        if (active) setState("processing");
      }
    }

    loadAnswer();
    const timer = window.setInterval(loadAnswer, 2500);
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [answerId, state]);

  return { answer, state, setAnswer, setState, refresh };
}

function classifyAnswerState(answer: CandidateAnswerRead): AnswerProcessingState {
  if (answer.evaluation?.overall_score !== null && answer.evaluation?.overall_score !== undefined) {
    return "evaluated";
  }
  if (answer.agent_results?.some((result) => result.status === "running")) {
    return "running_agents";
  }
  if (answer.agent_results?.some((result) => result.status === "succeeded")) {
    return "running_agents";
  }
  return "processing";
}
