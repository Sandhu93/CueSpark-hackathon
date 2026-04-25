import type {
  BenchmarkResponse,
  DocumentUploadResponse,
  Job,
  SessionCreateRequest,
  SessionCreateResponse,
  SessionRead,
} from "./types";

export type { Job } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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

  createSession: (payload: SessionCreateRequest) =>
    http<SessionCreateResponse>("/api/sessions", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getSession: (sessionId: string) => http<SessionRead>(`/api/sessions/${sessionId}`),

  prepareSession: (sessionId: string) =>
    http<Job>(`/api/sessions/${sessionId}/prepare`, {
      method: "POST",
    }),

  getBenchmark: (sessionId: string) =>
    http<BenchmarkResponse>(`/api/sessions/${sessionId}/benchmark`),

  uploadResume: async (sessionId: string, file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch(`${API_URL}/api/sessions/${sessionId}/resume`, {
      method: "POST",
      body: fd,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json() as Promise<DocumentUploadResponse>;
  },

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
