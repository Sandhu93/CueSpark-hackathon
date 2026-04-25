"use client";

import { useState } from "react";
import { api, putToPresigned } from "@/lib/api";
import { useJob } from "@/hooks/useJob";

export default function Home() {
  const [uploadUrl, setUploadUrl] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);

  const { job } = useJob(jobId);

  async function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const init = await api.initUpload(file.name, file.type);
      await putToPresigned(init.upload_url, file);
      setUploadUrl(init.public_url);
    } catch (err) {
      alert(`Upload failed: ${err}`);
    } finally {
      setUploading(false);
    }
  }

  async function startDummyJob() {
    const j = await api.createJob("dummy", { note: "kicked from web" });
    setJobId(j.id);
  }

  return (
    <main className="mx-auto max-w-2xl px-6 py-16 font-mono">
      <header className="mb-12">
        <h1 className="text-3xl font-bold tracking-tight">hackathon · template</h1>
        <p className="mt-2 text-[var(--muted)]">
          FastAPI · Next.js · Postgres · Redis · MinIO · Worker
        </p>
      </header>

      <section className="mb-10 rounded border border-[var(--border)] p-6">
        <h2 className="mb-4 text-lg">1 · Upload</h2>
        <input
          type="file"
          onChange={handleFile}
          disabled={uploading}
          className="block w-full text-sm file:mr-4 file:rounded file:border-0 file:bg-[var(--accent)] file:px-4 file:py-2 file:text-black"
        />
        {uploading && <p className="mt-3 text-[var(--muted)]">Uploading…</p>}
        {uploadUrl && (
          <p className="mt-3 break-all text-sm">
            <span className="text-[var(--muted)]">stored at:</span>{" "}
            <a href={uploadUrl} target="_blank" rel="noreferrer">{uploadUrl}</a>
          </p>
        )}
      </section>

      <section className="rounded border border-[var(--border)] p-6">
        <h2 className="mb-4 text-lg">2 · Run a background job</h2>
        <button
          onClick={startDummyJob}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm text-black"
        >
          enqueue dummy job
        </button>

        {job && (
          <div className="mt-6 space-y-1 text-sm">
            <div><span className="text-[var(--muted)]">id:</span> {job.id}</div>
            <div><span className="text-[var(--muted)]">status:</span> <Status value={job.status} /></div>
            {job.error && (
              <div className="text-red-400">error: {job.error}</div>
            )}
            {job.status === "succeeded" && (
              <pre className="mt-3 overflow-x-auto rounded bg-black/40 p-3 text-xs">
{JSON.stringify(job.result, null, 2)}
              </pre>
            )}
          </div>
        )}
      </section>
    </main>
  );
}

function Status({ value }: { value: string }) {
  const color =
    value === "succeeded" ? "text-emerald-400" :
    value === "failed"    ? "text-red-400" :
    value === "running"   ? "text-yellow-300" :
                            "text-[var(--muted)]";
  return <span className={color}>{value}</span>;
}
