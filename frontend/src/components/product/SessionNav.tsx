"use client";

import Link from "next/link";

type ProductRoute = "setup" | "match" | "benchmark" | "interview" | "report";

export function SessionNav({
  sessionId,
  active,
}: {
  sessionId?: string;
  active: ProductRoute;
}) {
  const links = sessionId
    ? [
        { key: "setup", label: "Setup", href: "/setup" },
        { key: "match", label: "Match", href: `/session/${sessionId}/match` },
        { key: "benchmark", label: "Benchmark", href: `/session/${sessionId}/benchmark` },
        { key: "interview", label: "Interview", href: `/session/${sessionId}/interview` },
        { key: "report", label: "Report", href: `/session/${sessionId}/report` },
      ]
    : [{ key: "setup", label: "Setup", href: "/setup" }];

  return (
    <nav className="flex flex-wrap gap-3 text-sm">
      {links.map((link) => (
        <Link
          key={link.key}
          href={link.href}
          className={`rounded border px-3 py-1 ${
            link.key === active
              ? "border-[var(--accent)] text-[var(--accent)]"
              : "border-[var(--border)] text-[var(--muted)]"
          }`}
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
