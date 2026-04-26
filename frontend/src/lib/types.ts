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

export type ResponseMode = "spoken_answer" | "written_answer" | "code_answer" | "mixed_answer";

export type QuestionCategory =
  | "technical"
  | "project_experience"
  | "behavioral"
  | "hr"
  | "resume_gap"
  | "jd_skill_validation"
  | "benchmark_gap_validation";

export type QuestionSource = "base_plan" | "adaptive_followup" | "manual" | "benchmark_gap";

export type AgentType =
  | "audio"
  | "video_signal"
  | "text_answer"
  | "code_evaluation"
  | "benchmark_gap"
  | "final_orchestrator";

export type AgentResultStatus = "pending" | "running" | "succeeded" | "failed";

export type HiringRecommendation = "strong_yes" | "yes" | "maybe" | "no" | "strong_no";

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

export interface QuestionRead {
  id: string;
  session_id: string;
  question_number: number;
  category: QuestionCategory;
  question_text: string;
  expected_signal: string | null;
  difficulty: string | null;
  source: QuestionSource;
  benchmark_gap_refs: unknown[];
  why_this_was_asked: string | null;
  response_mode: ResponseMode;
  requires_audio: boolean;
  requires_video: boolean;
  requires_text: boolean;
  requires_code: boolean;
  tts_object_key?: string | null;
  tts_audio_url?: string | null;
  created_at?: string;
}

export interface QuestionsResponse {
  questions: QuestionRead[];
}

export interface TtsResponse {
  question_id: string;
  audio_url: string;
}

export interface VisualSignalMetadata {
  face_in_frame_ratio?: number;
  lighting_quality?: "good" | "moderate" | "poor" | string;
  eye_contact_proxy?: "steady" | "moderate" | "low" | string;
  posture_stability?: "steady" | "moderate" | "unstable" | string;
  camera_presence?: "stable" | "intermittent" | "absent" | string;
  distraction_markers?: string[];
  [key: string]: unknown;
}

export interface AnswerSubmitResponse {
  answer_id: string;
  processing_status?: string;
  status?: "queued" | "pending" | "stored" | string;
  job_id?: string | null;
}

export interface SpokenAnswerSubmit {
  audio: File;
  duration_seconds?: number;
  visual_signal_metadata?: VisualSignalMetadata;
}

export interface WrittenAnswerSubmit {
  text_answer: string;
  visual_signal_metadata?: VisualSignalMetadata;
}

export interface CodeAnswerSubmit {
  code_answer: string;
  code_language: string;
  text_answer?: string;
  visual_signal_metadata?: VisualSignalMetadata;
}

export interface MixedAnswerSubmit {
  audio?: File;
  text_answer?: string;
  code_answer?: string;
  code_language?: string;
  duration_seconds?: number;
  visual_signal_metadata?: VisualSignalMetadata;
}

export interface AgentResultRead {
  id?: string;
  answer_id?: string;
  agent_type: AgentType;
  status: AgentResultStatus;
  score: number | null;
  payload: Record<string, unknown>;
  error?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface AnswerEvaluationRead {
  id?: string;
  answer_id?: string;
  relevance_score?: number | null;
  role_depth_score?: number | null;
  evidence_score?: number | null;
  structure_score?: number | null;
  clarity_score?: number | null;
  jd_alignment_score?: number | null;
  benchmark_gap_coverage_score?: number | null;
  communication_score?: number | null;
  communication_signal_score?: number | null;
  code_quality_score?: number | null;
  written_answer_score?: number | null;
  visual_signal_score?: number | null;
  overall_score: number | null;
  strengths?: string | string[] | null;
  weaknesses?: string | string[] | null;
  strict_feedback: string | null;
  improved_answer?: string | null;
  red_flags?: string[] | null;
  benchmark_gap_summary?: string | null;
  communication_summary?: string | null;
  modality_breakdown?: Record<string, unknown>;
  created_at?: string;
}

export interface CandidateAnswerRead {
  id: string;
  session_id: string;
  question_id: string;
  audio_object_key?: string | null;
  answer_mode: ResponseMode;
  transcript: string | null;
  text_answer: string | null;
  code_answer: string | null;
  code_language: string | null;
  duration_seconds: number | null;
  word_count: number | null;
  words_per_minute: number | null;
  filler_word_count: number | null;
  communication_metrics?: Record<string, unknown>;
  communication_metadata?: Record<string, unknown>;
  visual_signal_metadata: VisualSignalMetadata | Record<string, unknown>;
  agent_results?: AgentResultRead[];
  evaluation?: AnswerEvaluationRead | null;
  created_at: string;
}

export interface AgentResultsResponse {
  answer_id: string;
  agent_results: AgentResultRead[];
}

export interface MultimodalReportRead {
  id?: string;
  session_id?: string;
  readiness_score: number | null;
  hiring_recommendation: HiringRecommendation | null;
  summary: string | null;
  jd_resume_match_summary?: string | null;
  benchmark_similarity_score: number | null;
  resume_competitiveness_score: number | null;
  evidence_strength_score: number | null;
  skill_gaps: unknown[];
  benchmark_gaps: unknown[];
  interview_risk_areas: unknown[];
  answer_feedback: unknown[];
  resume_feedback: string | unknown[] | null;
  benchmark_gap_coverage_summary?: string | null;
  communication_summary?: Record<string, unknown>;
  audio_communication_summary?: string | null;
  visual_signal_summary: string | Record<string, unknown> | null;
  written_answer_summary?: Record<string, unknown>;
  written_answer_quality_summary?: string | null;
  code_answer_summary?: Record<string, unknown>;
  code_answer_quality_summary?: string | null;
  multimodal_summary?: Record<string, unknown>;
  improvement_plan: string | unknown[] | null;
  created_at?: string;
}
