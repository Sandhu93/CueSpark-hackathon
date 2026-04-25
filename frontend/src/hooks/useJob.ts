"use client";

import { useEffect, useState } from "react";
import { api, type Job } from "@/lib/api";

export function useJob(jobId: string | null, intervalMs = 1000) {
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout>;

    const tick = async () => {
      try {
        const j = await api.getJob(jobId);
        if (cancelled) return;
        setJob(j);
        if (j.status === "succeeded" || j.status === "failed") return;
        timer = setTimeout(tick, intervalMs);
      } catch (e) {
        if (!cancelled) setError(String(e));
      }
    };

    tick();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [jobId, intervalMs]);

  return { job, error };
}
