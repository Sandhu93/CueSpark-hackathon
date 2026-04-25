# 16 — Multimodal Evaluation Orchestrator

## Purpose

CueSpark should evolve from a benchmark-preparation demo into a workable interview product that can evaluate candidate responses across multiple modalities.

The core idea remains:

```txt
JD + Resume + Benchmark Profiles -> Benchmark Gaps -> Interview Questions -> Candidate Response -> Readiness Report
```

The new product layer is:

```txt
Candidate Response = audio + optional video signals + optional written text + optional code
```

Each modality is evaluated by a specialized analyzer, and a final orchestrator combines the outputs into a benchmark-aware readiness score.

## Current State

The application has completed the benchmark-preparation pipeline through on-demand TTS.

The next product milestone should not be a generic chatbot interview. It should be a structured interview execution loop that captures candidate responses and evaluates them using modality-specific analyzers.

## Product Positioning

Use this positioning:

```txt
CueSpark is a benchmark-driven, multimodal interview readiness platform.
```

Do not position it as:

```txt
emotion detector
confidence detector
personality detector
lie detector
```

Preferred language:

```txt
observable communication signals
visual presence signals
audio fluency signals
answer structure
benchmark gap coverage
code quality and correctness
```

## Response Modalities

Each interview question should define the response mode it expects.

Suggested values:

```txt
spoken_answer
written_answer
code_answer
mixed_answer
```

Examples:

### Spoken answer

Used for HR, behavioral, project, resume-gap, and most benchmark-gap questions.

Captured data:

- audio recording
- transcript
- optional sampled video signals

### Written answer

Used for case-study, explanation, pseudocode, stakeholder communication, product thinking, and non-technical written tasks.

Captured data:

- text answer
- optional audio/video explanation

### Code answer

Used for programming and technical implementation questions.

Captured data:

- code from Monaco editor
- selected language
- optional explanation text
- optional audio/video explanation

### Mixed answer

Used when a candidate writes or codes and explains verbally.

Captured data:

- audio
- transcript
- text/code artifact
- optional video signals

## Evaluation Agents

### 1. Audio Agent

Input:

- audio file
- transcript
- question context

Outputs:

- transcript
- speaking pace
- filler word count
- pause/hesitation markers
- clarity score
- structure score
- communication signal score

The audio agent should not claim emotion or true confidence.

### 2. Video Signal Agent

Input:

- short frame samples or frontend-computed metadata
- question timing metadata

Outputs:

- face in frame
- lighting quality
- camera presence
- eye contact proxy
- posture stability
- distraction indicators
- visual communication signal score

The video agent should not claim emotion, personality, truthfulness, or true confidence.

### 3. Text Answer Agent

Input:

- written answer
- question context
- benchmark gap references

Outputs:

- relevance score
- completeness score
- structure score
- specificity score
- evidence score
- clarity score

### 4. Code Evaluation Agent

Input:

- code answer
- programming language
- problem statement
- optional test cases
- candidate explanation

Outputs:

- correctness score
- edge-case handling score
- complexity score
- readability score
- testability score
- explanation score

For early production, prefer static review and optional safe sample tests. Do not execute arbitrary code on the main backend.

### 5. Benchmark Gap Agent

Input:

- question
- benchmark gap references
- transcript/text/code/evaluation outputs

Outputs:

- benchmark gap coverage score
- whether the candidate directly addressed the tested gap
- evidence quality
- risk if answer remains weak

This is the core CueSpark differentiator.

### 6. Final Evaluation Orchestrator

Input:

- question metadata
- response modality
- audio analysis result
- video signal result
- text analysis result
- code analysis result
- benchmark gap analysis result

Output:

- final answer score
- category scores
- strict feedback
- improvement suggestions
- report-ready summary

## Scoring Principle

Scoring should be dynamic based on response mode.

### Spoken answer example

```txt
benchmark gap coverage: 30%
answer relevance: 20%
evidence/examples: 20%
communication clarity: 15%
role-specific depth: 10%
visual/audio professionalism: 5%
```

### Code answer example

```txt
code correctness: 35%
reasoning/explanation: 20%
complexity: 15%
edge cases: 15%
readability/testability: 10%
benchmark relevance: 5%
```

### Written answer example

```txt
relevance: 25%
structure: 20%
evidence/specificity: 20%
completeness: 15%
benchmark gap coverage: 15%
clarity: 5%
```

## Data Capture Policy

For MVP:

- store audio files in MinIO
- store transcripts in Postgres
- store text and code responses in Postgres
- store video analysis summaries in Postgres
- avoid storing full video files initially unless explicitly required
- optionally sample frames locally or compute browser-side metadata later

## Privacy and Safety

Do not claim:

- emotion detection
- true confidence detection
- personality detection
- truthfulness detection
- hiring guarantee

Use:

- observable communication signal
- visual presence signal
- eye contact proxy
- posture stability
- speech pace
- filler words
- answer structure

## Recommended Implementation Path

Since the app is currently complete through on-demand TTS, implement this in layers:

```txt
Phase 4A — Response schema and modality model
Phase 4B — Audio answer capture and transcription
Phase 4C — Text answer capture and analysis
Phase 4D — Code answer capture and static code analysis
Phase 4E — Video signal capture MVP
Phase 5A — Agent result storage
Phase 5B — Final evaluation orchestrator
Phase 5C — Final multimodal readiness report
```

Do not try to build all agents at once. Audio + transcript + benchmark-aware answer evaluation should be the first real product milestone.
