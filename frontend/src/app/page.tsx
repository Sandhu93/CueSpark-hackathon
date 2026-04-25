import Link from "next/link";

const capabilities = [
  "Create a single interview session from a pasted job description.",
  "Paste resume text or upload a PDF, DOCX, or TXT resume.",
  "Show session status, match fields, and role signals returned by the API.",
  "Display the benchmark gap dashboard when comparison data exists.",
];

const pending = [
  "Full preparation job endpoint",
  "Interview question playback",
  "Candidate audio recording",
  "Answer evaluation and final report",
];

export default function Home() {
  return (
    <main className="min-h-screen">
      <section className="border-b border-[var(--border)]">
        <div className="mx-auto grid w-full max-w-6xl gap-10 px-6 py-14 lg:grid-cols-[1fr_380px] lg:py-20">
          <div>
            <p className="text-sm font-medium text-[var(--accent)]">CueSpark Interview Coach</p>
            <h1 className="mt-4 max-w-3xl text-4xl font-semibold tracking-tight sm:text-5xl">
              Benchmark-driven interview readiness from JD and resume evidence.
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-7 text-[var(--muted)]">
              This demo focuses on what the backend has already built: session intake,
              document ingestion, match status fields, and benchmark comparison output.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href="/setup"
                className="rounded bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-black"
              >
                Start demo
              </Link>
              <a
                href="http://localhost:8000/health"
                className="rounded border border-[var(--border)] px-5 py-3 text-sm"
              >
                Check API health
              </a>
            </div>
          </div>

          <aside className="rounded border border-[var(--border)] bg-black/20 p-5">
            <h2 className="text-sm font-semibold">Current demo path</h2>
            <ol className="mt-4 space-y-3 text-sm leading-6 text-[var(--muted)]">
              <li>1. Paste JD and resume evidence.</li>
              <li>2. Create a session and optionally upload a resume file.</li>
              <li>3. Review match/session status.</li>
              <li>4. Open benchmark gaps when the backend has written them.</li>
            </ol>
          </aside>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-5 px-6 py-10 lg:grid-cols-2">
        <InfoPanel title="Built backend surface" items={capabilities} />
        <InfoPanel title="Not in this demo yet" items={pending} muted />
      </section>
    </main>
  );
}

function InfoPanel({
  title,
  items,
  muted,
}: {
  title: string;
  items: string[];
  muted?: boolean;
}) {
  return (
    <section className="rounded border border-[var(--border)] bg-black/20 p-5">
      <h2 className="text-sm font-semibold">{title}</h2>
      <ul className="mt-4 space-y-2 text-sm leading-6">
        {items.map((item) => (
          <li key={item} className={muted ? "text-[var(--muted)]" : ""}>
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}
