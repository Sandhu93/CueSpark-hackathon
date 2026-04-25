import type {
  DemoAnswerTranscript,
  DemoBenchmarkComparison,
  DemoCommunicationSignals,
  DemoDashboardData,
  DemoFinalReport,
  DemoInterviewRoomData,
  DemoInterviewQuestion,
  DemoSession,
  DemoSetupPreview,
} from "./types";

export const mockSession: DemoSession = {
  id: "demo-session-backend-001",
  status: "demo_preview",
  roleTitle: "Senior Backend Engineer",
  roleKey: "backend_developer",
  companyName: "Aster Cloud Systems",
  candidateName: "Demo Candidate",
  demoModeLabel: "Demo Preview / Mock Data Mode",
  jobDescriptionExcerpt:
    "Own backend services for a multi-tenant SaaS platform, improve API reliability, lead incident response, and define service-level metrics with product and platform teams.",
  resumeSummary:
    "Python backend engineer with FastAPI and PostgreSQL experience. Resume shows API delivery and reliability work, but has limited quantified impact, scale details, and explicit end-to-end ownership evidence.",
};

export const mockBenchmarkComparison: DemoBenchmarkComparison = {
  sessionId: mockSession.id,
  roleKey: mockSession.roleKey,
  benchmarkSimilarityScore: 54,
  resumeCompetitivenessScore: 48,
  evidenceStrengthScore: 39,
  hiringBarGap: "high",
  benchmarkExplanation:
    "This mock comparison uses curated benchmark profiles and top-candidate archetypes to identify evidence gaps against the role benchmark corpus. It is not based on hired resumes or scraped personal profiles.",
  benchmarkProfiles: [
    {
      id: "demo-benchmark-01",
      profileName: "Backend Archetype - Platform Owner",
      roleTitle: "Senior Backend Engineer",
      seniorityLevel: "senior",
      qualityScore: 91,
      archetypeSummary:
        "Shows service ownership, latency metrics, incident leadership, and cross-team platform delivery.",
    },
    {
      id: "demo-benchmark-02",
      profileName: "Backend Archetype - Reliability Builder",
      roleTitle: "Backend Engineer",
      seniorityLevel: "mid-senior",
      qualityScore: 88,
      archetypeSummary:
        "Strong evidence of SLO design, observability work, on-call improvements, and production debugging depth.",
    },
    {
      id: "demo-benchmark-03",
      profileName: "Backend Archetype - Product-Facing API Lead",
      roleTitle: "Backend Engineer",
      seniorityLevel: "senior",
      qualityScore: 86,
      archetypeSummary:
        "Connects API design decisions to customer workflows, adoption metrics, and delivery trade-offs.",
    },
  ],
  missingSkills: [
    "Distributed systems trade-off discussion",
    "Observability and SLO design",
    "Capacity planning for high-traffic APIs",
  ],
  weakSkills: [
    "Incident response examples lack technical depth",
    "Cross-team influence is stated but not evidenced",
    "API reliability work lacks before-and-after metrics",
  ],
  missingMetrics: [
    "Latency or throughput improvement numbers",
    "Error-rate reduction evidence",
    "Scale of users, requests, services, or data volume",
  ],
  weakOwnershipSignals: [
    "No clear final decision ownership for architecture choices",
    "Limited evidence of owning production outcomes after launch",
    "No explicit ownership of roadmap, SLOs, or incident follow-through",
  ],
  interviewRiskAreas: [
    "Candidate may describe implementation work without showing senior-level ownership.",
    "Candidate may struggle to quantify backend reliability impact.",
    "Candidate may not connect technical decisions to product or business outcomes.",
  ],
  recommendedResumeFixes: [
    "Add measurable reliability outcomes such as p95 latency, uptime, error-rate, or incident reduction.",
    "Name the ownership scope for each major project: services, team size, stakeholders, and decision rights.",
    "Add one example where a backend trade-off changed product or customer outcomes.",
  ],
  questionTargets: [
    "Validate end-to-end ownership of a backend service.",
    "Probe missing reliability metrics and production impact.",
    "Test observability depth and SLO reasoning.",
    "Check ability to explain architecture trade-offs to stakeholders.",
    "Assess incident response maturity under pressure.",
  ],
};

export const mockDashboardData: DemoDashboardData = {
  scoreTrends: [
    { label: "Benchmark Similarity", values: [50, 53, 56, 61, 58, 54] },
    { label: "Resume Competitiveness", values: [42, 45, 51, 49, 52, 48] },
    { label: "Evidence Strength", values: [44, 43, 46, 41, 37, 39] },
    { label: "Hiring Bar Gap", values: [65, 62, 58, 49, 45, 42] },
  ],
  benchmarkCoverage: [
    { label: "Ownership", candidateScore: 42, benchmarkScore: 78 },
    { label: "Business Impact", candidateScore: 38, benchmarkScore: 72 },
    { label: "System Design", candidateScore: 60, benchmarkScore: 68 },
    { label: "Trade-offs", candidateScore: 45, benchmarkScore: 65 },
    { label: "Production Depth", candidateScore: 46, benchmarkScore: 70 },
    { label: "Communication", candidateScore: 65, benchmarkScore: 75 },
  ],
  topBenchmarkGaps: [
    {
      label: "Missing metrics",
      impactScore: 86,
      severity: "high",
      detail: "No latency, throughput, availability, or error-rate proof.",
    },
    {
      label: "Weak ownership proof",
      impactScore: 78,
      severity: "high",
      detail: "Resume states delivery but not decision rights or post-launch accountability.",
    },
    {
      label: "Architecture trade-offs",
      impactScore: 64,
      severity: "medium",
      detail: "Limited explanation of alternatives, constraints, and operating cost.",
    },
    {
      label: "Production evidence missing",
      impactScore: 60,
      severity: "medium",
      detail: "Few examples of incidents, debugging, SLOs, or on-call follow-through.",
    },
  ],
  evidenceDistribution: [
    { label: "Strong Evidence", count: 32, percent: 25, tone: "strong" },
    { label: "Weak Evidence", count: 51, percent: 40, tone: "weak" },
    { label: "Missing Evidence", count: 45, percent: 35, tone: "missing" },
  ],
  benchmarkProfileMatches: [
    {
      profileName: "Backend Eng. 01",
      profileSummary: "Mid-level API owner",
      matchScore: 62,
      matchLabel: "Best Match",
    },
    {
      profileName: "Backend Eng. 02",
      profileSummary: "Product-facing API builder",
      matchScore: 58,
      matchLabel: "Close Match",
    },
    {
      profileName: "Backend Eng. 03",
      profileSummary: "Platform reliability owner",
      matchScore: 45,
      matchLabel: "Possible Match",
    },
    {
      profileName: "Backend Eng. 04",
      profileSummary: "Data infrastructure engineer",
      matchScore: 31,
      matchLabel: "Low Match",
    },
  ],
  questionTargetCounts: [
    { label: "Ownership and accountability", count: 8 },
    { label: "System design depth", count: 7 },
    { label: "Production debugging", count: 6 },
    { label: "Metrics and impact", count: 6 },
    { label: "Cross-functional leadership", count: 5 },
  ],
  interviewStrategyChips: [
    "ownership proof",
    "metrics",
    "production depth",
    "business impact",
    "architecture decisions",
  ],
};

export const mockSetupPreview: DemoSetupPreview = {
  workflowSteps: [
    { label: "Setup", description: "Provide inputs" },
    { label: "Match", description: "Resume alignment" },
    { label: "Benchmark", description: "Gap analysis" },
    { label: "Interview", description: "AI-powered session" },
    { label: "Report", description: "Readiness output" },
  ],
  jdPreview:
    "We are hiring a Senior Backend Engineer with FastAPI, PostgreSQL, scalable APIs, debugging, ownership, and production systems experience.",
  resumePreview:
    "Candidate has built APIs, worked with PostgreSQL, supported backend services, and contributed to reliability improvements across product teams.",
  interviewerLensPreview:
    "Panel emphasis: ownership, architecture trade-offs, production debugging, stakeholder communication, and measurable backend impact.",
  preparationChecklist: [
    "Benchmark gap analysis",
    "Targeted interview questions",
    "Resume signal review",
    "Role-specific risk areas",
  ],
  interviewerLensChips: ["User-provided context", "Likely focus areas", "Panel emphasis"],
};

export const mockInterviewRoomData: DemoInterviewRoomData = {
  mockTimer: "28:47",
  currentQuestionNumber: 3,
  totalQuestions: 8,
  interviewerPanel: "Engineering Manager Panel",
  likelyFollowUp: "Impact metrics, trade-offs, failures, stakeholder management",
  transcriptLines: [
    {
      time: "00:24",
      text: "I led the scaling of our ingestion platform to handle a large increase in data volume.",
    },
    {
      time: "00:32",
      text: "The key challenge was maintaining reliability while improving latency.",
    },
    {
      time: "00:45",
      text: "I introduced event-driven processing and added tracing around the slow path.",
    },
    {
      time: "01:02",
      text: "We improved processing speed and reduced timeout errors after rollout.",
    },
  ],
  workspaceTitle: "Response Workspace",
  workspaceMode: "Text Response",
  workspaceLanguage: "Structured notes",
  workspaceContent:
    "Context: payments API reliability work\nAction: tracing, slow-query isolation, cache, SLO dashboard\nImpact: p95 latency reduced, timeout errors lowered\nTrade-off: added cache invalidation complexity and monitoring guardrails",
  bottomControls: [
    { label: "Mute", token: "Mic" },
    { label: "Stop Video", token: "Cam" },
    { label: "Share Screen", token: "Scr" },
    { label: "Notes", token: "N" },
    { label: "Pause", token: "II" },
    { label: "Settings", token: "Set" },
  ],
};

export const mockInterviewQuestions: DemoInterviewQuestion[] = [
  {
    id: "demo-question-01",
    questionNumber: 1,
    category: "benchmark_gap_validation",
    difficulty: "hard",
    questionText:
      "Your resume mentions API reliability work, but does not show measurable outcomes. Walk me through one reliability improvement you owned and quantify the before-and-after impact.",
    whyThisWasAsked:
      "Benchmark profiles for this role usually show concrete reliability metrics such as latency, uptime, error rate, or incident reduction.",
    benchmarkGapRefs: ["missing reliability metrics", "weak ownership proof"],
    expectedSignal:
      "Specific service context, baseline metric, action taken, measurable result, and ownership boundaries.",
  },
  {
    id: "demo-question-02",
    questionNumber: 2,
    category: "technical",
    difficulty: "hard",
    questionText:
      "Describe a backend architecture decision where you had to choose between speed of delivery and long-term maintainability. What trade-off did you make?",
    whyThisWasAsked:
      "The benchmark corpus shows stronger candidates explain trade-offs, not only implementation details.",
    benchmarkGapRefs: ["distributed systems trade-off discussion"],
    expectedSignal:
      "Clear alternatives, constraints, decision criteria, stakeholder impact, and outcome measurement.",
  },
  {
    id: "demo-question-03",
    questionNumber: 3,
    category: "project_experience",
    difficulty: "medium",
    questionText:
      "Tell me about a service or API you owned after launch. How did you monitor it, improve it, and handle production issues?",
    whyThisWasAsked:
      "The resume shows delivery, but benchmark profiles show stronger post-launch ownership and operational maturity.",
    benchmarkGapRefs: ["post-launch ownership", "observability and SLO design"],
    expectedSignal:
      "Monitoring approach, alert quality, incident response, follow-up fixes, and user or system impact.",
  },
  {
    id: "demo-question-04",
    questionNumber: 4,
    category: "jd_skill_validation",
    difficulty: "medium",
    questionText:
      "The job requires cross-functional backend leadership. Give an example where you influenced product or platform stakeholders without direct authority.",
    whyThisWasAsked:
      "Cross-team influence is mentioned, but evidence is weaker than the role benchmark expects.",
    benchmarkGapRefs: ["weak cross-team influence evidence"],
    expectedSignal:
      "Stakeholder map, disagreement or constraint, communication approach, decision outcome, and measurable effect.",
  },
  {
    id: "demo-question-05",
    questionNumber: 5,
    category: "behavioral",
    difficulty: "hard",
    questionText:
      "Tell me about a production incident where your first hypothesis was wrong. What did you do next?",
    whyThisWasAsked:
      "Strict interviewers will test whether the candidate can reason under pressure, revise assumptions, and drive follow-through.",
    benchmarkGapRefs: ["incident response maturity"],
    expectedSignal:
      "Structured debugging, calm escalation, evidence-based reasoning, communication, and preventive follow-up.",
  },
];

export const mockAnswerTranscript: DemoAnswerTranscript = {
  questionId: "demo-question-01",
  addressedBenchmarkGap: true,
  transcript:
    "In my last role I owned the payments API used by three internal product teams. The baseline p95 latency was around 820 milliseconds during peak traffic. I added request tracing, found two slow database joins, introduced a cache for merchant configuration, and worked with QA to load test the path. After rollout, p95 latency dropped to about 430 milliseconds and timeout errors reduced by roughly 28 percent. I also added dashboards and an alert tied to the latency SLO so the team could catch regressions early.",
  evaluationPreview:
    "Good quantified answer. The candidate gave service context, baseline, actions, and measurable outcome. Ownership scope is present, but stakeholder and trade-off details could be sharper.",
};

export const mockCommunicationSignals: DemoCommunicationSignals = {
  faceInFrame: "stable",
  lightingQuality: "good",
  eyeContactProxy: "mixed",
  postureStability: "stable",
  speakingPaceWpm: 142,
  fillerWordCount: 6,
  answerStructure: "clear",
  signalExplanation:
    "These are observable communication signals for demo presentation only: framing, lighting, eye contact proxy, posture stability, speaking pace, filler words, and answer structure. They do not detect emotion, true confidence, or personality.",
};

export const mockFinalReport: DemoFinalReport = {
  sessionId: mockSession.id,
  readinessScore: 67,
  hiringRecommendation: "maybe",
  summary:
    "The candidate shows credible backend implementation experience and some reliability ownership, but the resume and interview still need stronger evidence of senior-level ownership, production scale, and measurable business or system impact.",
  jdResumeMatchScore: 72,
  benchmarkSimilarityScore: mockBenchmarkComparison.benchmarkSimilarityScore,
  resumeCompetitivenessScore: mockBenchmarkComparison.resumeCompetitivenessScore,
  evidenceStrengthScore: mockBenchmarkComparison.evidenceStrengthScore,
  roleSpecificDepthScore: 70,
  communicationClarityScore: 76,
  benchmarkGapCoverageScore: 61,
  interviewRiskAreas: mockBenchmarkComparison.interviewRiskAreas,
  answerFeedback: [
    {
      questionId: "demo-question-01",
      questionNumber: 1,
      category: "benchmark_gap_validation",
      score: 78,
      strictFeedback:
        "Strongest answer. The candidate quantified latency and error-rate improvement, but should explain decision ownership and rollout risk more clearly.",
      benchmarkGapCoverage:
        "Partially closes the missing metrics gap and gives useful reliability evidence.",
    },
    {
      questionId: "demo-question-02",
      questionNumber: 2,
      category: "technical",
      score: 64,
      strictFeedback:
        "The trade-off discussion was understandable but too general. A senior candidate should compare alternatives and name the operational cost of the decision.",
      benchmarkGapCoverage:
        "Does not fully close the distributed systems trade-off gap.",
    },
    {
      questionId: "demo-question-04",
      questionNumber: 4,
      category: "jd_skill_validation",
      score: 59,
      strictFeedback:
        "Stakeholder influence example lacked conflict, measurable outcome, and clear decision rights.",
      benchmarkGapCoverage:
        "Weak coverage of cross-team leadership evidence.",
    },
  ],
  resumeFeedback: [
    "Add quantified backend reliability outcomes for at least two projects.",
    "Show ownership scope: services owned, stakeholders, incident responsibility, and post-launch accountability.",
    "Replace generic API delivery bullets with proof of scale, constraints, and impact.",
  ],
  resumeBulletUpgrade: {
    weakBullet: "Built and maintained backend APIs for internal teams.",
    improvedBullet:
      "Owned the payments API used by three product teams, reducing p95 latency from 820ms to 430ms and timeout errors by 28% through tracing, query tuning, caching, and SLO-backed monitoring.",
    missingEvidenceExplanation:
      "The weak bullet names implementation work but misses benchmark-level evidence: service scope, ownership boundary, baseline metric, measurable improvement, and post-launch accountability.",
  },
  topImprovementPriorities: [
    "Quantify backend reliability impact with before-and-after metrics.",
    "Clarify senior-level ownership, decision rights, and production accountability.",
    "Prepare deeper trade-off stories that connect technical choices to product outcomes.",
  ],
  preparationPlan: [
    "Rewrite the top three backend project bullets with scope, metrics, and ownership boundaries.",
    "Prepare two STAR stories around production incidents with metrics and follow-up actions.",
    "Practice one architecture trade-off story with alternatives, constraints, and measurable outcome.",
    "Build a concise SLO and observability explanation for one owned service.",
    "Prepare one stakeholder influence example where there was disagreement or ambiguity.",
    "Practice answering reliability impact questions without drifting into generic implementation detail.",
    "Run a final mock interview pass focused on benchmark gaps: ownership, metrics, scale, and trade-offs.",
  ],
};
