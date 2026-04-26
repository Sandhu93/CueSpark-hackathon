import type {
  AgentResultsResponse,
  AnswerSubmitResponse,
  BenchmarkResponse,
  CandidateAnswerRead,
  CodeAnswerSubmit,
  DocumentUploadResponse,
  Job,
  MixedAnswerSubmit,
  MultimodalReportRead,
  QuestionsResponse,
  SessionCreateRequest,
  SessionCreateResponse,
  SessionRead,
  SpokenAnswerSubmit,
  TtsResponse,
  WrittenAnswerSubmit,
} from "./types";

export type {
  AgentResultRead,
  AgentResultsResponse,
  AnswerEvaluationRead,
  AnswerSubmitResponse,
  CandidateAnswerRead,
  Job,
  MultimodalReportRead,
  QuestionRead,
  QuestionsResponse,
  ResponseMode,
  TtsResponse,
} from "./types";

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

async function httpForm<T>(path: string, body: FormData): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    body,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  return res.json() as Promise<T>;
}

function appendOptional(formData: FormData, key: string, value: string | number | undefined): void {
  if (value === undefined) return;
  formData.append(key, String(value));
}

function appendVisualSignalMetadata(
  formData: FormData,
  metadata: Record<string, unknown> | undefined,
): void {
  if (!metadata) return;
  formData.append("visual_signal_metadata", JSON.stringify(metadata));
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

  listQuestions: (sessionId: string) =>
    http<QuestionsResponse>(`/api/sessions/${sessionId}/questions`),

  generateQuestionTts: (questionId: string) =>
    http<TtsResponse>(`/api/questions/${questionId}/tts`, {
      method: "POST",
    }),

  getQuestionTts: (questionId: string) =>
    http<TtsResponse>(`/api/questions/${questionId}/tts`),

  submitSpokenAnswer: (questionId: string, payload: SpokenAnswerSubmit) => {
    const fd = new FormData();
    fd.append("answer_mode", "spoken_answer");
    fd.append("audio", payload.audio);
    appendOptional(fd, "duration_seconds", payload.duration_seconds);
    appendVisualSignalMetadata(fd, payload.visual_signal_metadata);
    return httpForm<AnswerSubmitResponse>(`/api/questions/${questionId}/answers`, fd);
  },

  submitWrittenAnswer: (questionId: string, payload: WrittenAnswerSubmit) =>
    http<AnswerSubmitResponse>(`/api/questions/${questionId}/answers`, {
      method: "POST",
      body: JSON.stringify({
        answer_mode: "written_answer",
        text_answer: payload.text_answer,
        visual_signal_metadata: payload.visual_signal_metadata,
      }),
    }),

  submitCodeAnswer: (questionId: string, payload: CodeAnswerSubmit) =>
    http<AnswerSubmitResponse>(`/api/questions/${questionId}/answers`, {
      method: "POST",
      body: JSON.stringify({
        answer_mode: "code_answer",
        code_answer: payload.code_answer,
        code_language: payload.code_language,
        text_answer: payload.text_answer,
        visual_signal_metadata: payload.visual_signal_metadata,
      }),
    }),

  submitMixedAnswer: (questionId: string, payload: MixedAnswerSubmit) => {
    const fd = new FormData();
    fd.append("answer_mode", "mixed_answer");
    if (payload.audio) fd.append("audio", payload.audio);
    appendOptional(fd, "text_answer", payload.text_answer);
    appendOptional(fd, "code_answer", payload.code_answer);
    appendOptional(fd, "code_language", payload.code_language);
    appendOptional(fd, "duration_seconds", payload.duration_seconds);
    appendVisualSignalMetadata(fd, payload.visual_signal_metadata);
    return httpForm<AnswerSubmitResponse>(`/api/questions/${questionId}/answers`, fd);
  },

  getAnswer: (answerId: string) =>
    http<CandidateAnswerRead>(`/api/answers/${answerId}`),

  getAnswerAgentResults: (answerId: string) =>
    http<AgentResultsResponse>(`/api/answers/${answerId}/agent-results`),

  generateReport: (sessionId: string) =>
    http<Job>(`/api/sessions/${sessionId}/report`, {
      method: "POST",
    }),

  getReport: (sessionId: string) =>
    http<MultimodalReportRead>(`/api/sessions/${sessionId}/report`),

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
