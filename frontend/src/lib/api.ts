const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type JobStatus = "queued" | "running" | "succeeded" | "failed";

export interface Job {
  id: string;
  kind: string;
  status: JobStatus;
  input: Record<string, unknown>;
  result: Record<string, unknown>;
  error: string | null;
  created_at: string;
  updated_at: string;
}

export interface UploadInitResponse {
  object_key: string;
  upload_url: string;
  public_url: string;
}

async function http<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () => http<{ status: string; env: string }>("/health"),

  initUpload: (filename: string, contentType: string) =>
    http<UploadInitResponse>("/uploads/init", {
      method: "POST",
      body: JSON.stringify({ filename, content_type: contentType }),
    }),

  directUpload: async (file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch(`${API_URL}/uploads/direct`, {
      method: "POST",
      body: fd,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json() as Promise<{ object_key: string; public_url: string; size: number }>;
  },

  createJob: (kind: string, input: Record<string, unknown> = {}) =>
    http<Job>("/jobs", {
      method: "POST",
      body: JSON.stringify({ kind, input }),
    }),

  getJob: (id: string) => http<Job>(`/jobs/${id}`),
};

/**
 * Upload a file to a presigned URL using PUT. Use after api.initUpload().
 */
export async function putToPresigned(url: string, file: File): Promise<void> {
  const res = await fetch(url, {
    method: "PUT",
    body: file,
    headers: { "Content-Type": file.type || "application/octet-stream" },
  });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
}
