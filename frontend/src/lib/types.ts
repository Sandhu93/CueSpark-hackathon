export type SessionStatus =
  | "draft"
  | "preparing"
  | "ready"
  | "in_progress"
  | "evaluating"
  | "report_ready"
  | "completed"
  | "failed";

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

export interface SessionCreateRequest {
  job_description: string;
  resume_text?: string | null;
  role_title?: string | null;
  company_name?: string | null;
}

export interface SessionCreateResponse {
  session_id: string;
  status: SessionStatus;
}

export interface SessionRead {
  id: string;
  status: SessionStatus;
  role_title: string | null;
  role_key: string | null;
  company_name: string | null;
  job_description_text: string;
  resume_text: string | null;
  match_score: number | null;
  benchmark_similarity_score: number | null;
  resume_competitiveness_score: number | null;
  evidence_strength_score: number | null;
  current_question_index: number;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface DocumentUploadResponse {
  document_id: string;
  parse_status: "pending" | "parsed" | "failed" | "ocr_required" | string;
}

export interface BenchmarkProfileSummary {
  id: string;
  profile_name: string;
  role_title: string;
  seniority_level: string;
  quality_score: number | null;
}

export interface BenchmarkComparisonResponse {
  session_id: string;
  role_key: string;
  benchmark_similarity_score: number | null;
  resume_competitiveness_score: number | null;
  evidence_strength_score: number | null;
  benchmark_profiles: BenchmarkProfileSummary[];
  missing_skills: string[];
  weak_skills: string[];
  missing_metrics: string[];
  weak_ownership_signals: string[];
  interview_risk_areas: string[];
  recommended_resume_fixes: string[];
  question_targets: string[];
}

export interface BenchmarkPendingResponse {
  session_id: string;
  status: "pending";
}

export type BenchmarkResponse = BenchmarkComparisonResponse | BenchmarkPendingResponse;

export function isBenchmarkComparison(
  value: BenchmarkResponse,
): value is BenchmarkComparisonResponse {
  return "role_key" in value;
}
