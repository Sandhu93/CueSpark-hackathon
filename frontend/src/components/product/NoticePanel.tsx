"use client";

import type React from "react";

type NoticeTone = "neutral" | "error" | "warning";

export function NoticePanel({
  title,
  children,
  tone = "neutral",
  action,
}: {
  title: string;
  children: React.ReactNode;
  tone?: NoticeTone;
  action?: React.ReactNode;
}) {
  const toneClass =
    tone === "error"
      ? "border-red-500/40 bg-red-500/10 text-red-100"
      : tone === "warning"
        ? "border-yellow-400/40 bg-yellow-400/10 text-yellow-100"
        : "border-[var(--border)] bg-black/20 text-[var(--muted)]";

  return (
    <section className={`rounded border p-5 text-sm leading-6 ${toneClass}`}>
      <h2 className="font-semibold text-[var(--fg)]">{title}</h2>
      <div className="mt-2">{children}</div>
      {action && <div className="mt-4 flex flex-wrap gap-3">{action}</div>}
    </section>
  );
}

export function SafetyCopy({ recommendation = false }: { recommendation?: boolean }) {
  return (
    <p className="rounded border border-[var(--border)] bg-black/20 p-3 text-xs leading-5 text-[var(--muted)]">
      Observable communication and visual presence signals only. CueSpark does not
      detect emotion, personality, truthfulness, or true confidence.
      {recommendation ? " This is preparation guidance, not a hiring guarantee." : ""}
    </p>
  );
}
