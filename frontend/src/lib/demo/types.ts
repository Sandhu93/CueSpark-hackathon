export type DemoSessionStatus = "demo_preview";

export type DemoQuestionCategory =
  | "technical"
  | "project_experience"
  | "behavioral"
  | "hr"
  | "resume_gap"
  | "jd_skill_validation"
  | "benchmark_gap_validation";

export type DemoDifficulty = "easy" | "medium" | "hard";

export type DemoHiringRecommendation = "strong_yes" | "yes" | "maybe" | "no";

export interface DemoSession {
  id: string;
  status: DemoSessionStatus;
  roleTitle: string;
  roleKey: string;
  companyName: string;
  candidateName: string;
  jobDescriptionExcerpt: string;
  resumeSummary: string;
  demoModeLabel: string;
}

export interface DemoBenchmarkProfile {
  id: string;
  profileName: string;
  roleTitle: string;
  seniorityLevel: string;
  qualityScore: number;
  archetypeSummary: string;
}

export interface DemoBenchmarkComparison {
  sessionId: string;
  roleKey: string;
  benchmarkSimilarityScore: number;
  resumeCompetitivenessScore: number;
  evidenceStrengthScore: number;
  hiringBarGap: "low" | "moderate" | "high";
  benchmarkProfiles: DemoBenchmarkProfile[];
  missingSkills: string[];
  weakSkills: string[];
  missingMetrics: string[];
  weakOwnershipSignals: string[];
  interviewRiskAreas: string[];
  recommendedResumeFixes: string[];
  questionTargets: string[];
  benchmarkExplanation: string;
}

export interface DemoScoreTrend {
  label: string;
  values: number[];
}

export interface DemoBenchmarkCoverageItem {
  label: string;
  candidateScore: number;
  benchmarkScore: number;
}

export interface DemoBenchmarkGapItem {
  label: string;
  impactScore: number;
  severity: "high" | "medium" | "low";
  detail: string;
}

export interface DemoEvidenceDistributionItem {
  label: string;
  count: number;
  percent: number;
  tone: "strong" | "weak" | "missing";
}

export interface DemoBenchmarkProfileMatch {
  profileName: string;
  profileSummary: string;
  matchScore: number;
  matchLabel: string;
}

export interface DemoQuestionTargetCount {
  label: string;
  count: number;
}

export interface DemoDashboardData {
  scoreTrends: DemoScoreTrend[];
  benchmarkCoverage: DemoBenchmarkCoverageItem[];
  topBenchmarkGaps: DemoBenchmarkGapItem[];
  evidenceDistribution: DemoEvidenceDistributionItem[];
  benchmarkProfileMatches: DemoBenchmarkProfileMatch[];
  questionTargetCounts: DemoQuestionTargetCount[];
  interviewStrategyChips: string[];
}

export interface DemoWorkflowStep {
  label: string;
  description: string;
}

export interface DemoSetupPreview {
  workflowSteps: DemoWorkflowStep[];
  jdPreview: string;
  resumePreview: string;
  interviewerLensPreview: string;
  preparationChecklist: string[];
  interviewerLensChips: string[];
}

export interface DemoInterviewQuestion {
  id: string;
  questionNumber: number;
  category: DemoQuestionCategory;
  difficulty: DemoDifficulty;
  questionText: string;
  whyThisWasAsked: string;
  benchmarkGapRefs: string[];
  expectedSignal: string;
}

export interface DemoAnswerTranscript {
  questionId: string;
  transcript: string;
  evaluationPreview: string;
  addressedBenchmarkGap: boolean;
}

export interface DemoTranscriptLine {
  time: string;
  text: string;
}

export interface DemoInterviewControl {
  label: string;
  token: string;
}

export interface DemoInterviewRoomData {
  mockTimer: string;
  currentQuestionNumber: number;
  totalQuestions: number;
  interviewerPanel: string;
  likelyFollowUp: string;
  transcriptLines: DemoTranscriptLine[];
  workspaceTitle: string;
  workspaceMode: string;
  workspaceLanguage: string;
  workspaceContent: string;
  bottomControls: DemoInterviewControl[];
}

export interface DemoCommunicationSignals {
  faceInFrame: "stable" | "intermittent" | "not_detected";
  lightingQuality: "good" | "mixed" | "poor";
  eyeContactProxy: "steady" | "mixed" | "low";
  postureStability: "stable" | "shifting" | "unstable";
  speakingPaceWpm: number;
  fillerWordCount: number;
  answerStructure: "clear" | "partial" | "unstructured";
  signalExplanation: string;
}

export interface DemoAnswerFeedback {
  questionId: string;
  questionNumber: number;
  category: DemoQuestionCategory;
  score: number;
  strictFeedback: string;
  benchmarkGapCoverage: string;
}

export interface DemoResumeBulletUpgrade {
  weakBullet: string;
  improvedBullet: string;
  missingEvidenceExplanation: string;
}

export interface DemoFinalReport {
  sessionId: string;
  readinessScore: number;
  hiringRecommendation: DemoHiringRecommendation;
  summary: string;
  jdResumeMatchScore: number;
  benchmarkSimilarityScore: number;
  resumeCompetitivenessScore: number;
  evidenceStrengthScore: number;
  roleSpecificDepthScore: number;
  communicationClarityScore: number;
  benchmarkGapCoverageScore: number;
  interviewRiskAreas: string[];
  answerFeedback: DemoAnswerFeedback[];
  resumeFeedback: string[];
  resumeBulletUpgrade: DemoResumeBulletUpgrade;
  topImprovementPriorities: string[];
  preparationPlan: string[];
}
