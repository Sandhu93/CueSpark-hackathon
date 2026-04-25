# 04 — AI, Audio, and RAG Design

## AI Design Principle

The AI must behave like a strict interviewer, not a friendly chatbot.

Every AI action should have:

- Clear input contract.
- Versioned prompt.
- Typed output schema.
- Stored result.
- Retry path.

## Recommended Model Roles

Configuration should be centralized in settings.

```text
Chat / reasoning:      OPENAI_CHAT_MODEL
TTS:                   OPENAI_TTS_MODEL
TTS voice:             OPENAI_TTS_VOICE
Transcription:         OPENAI_TRANSCRIBE_MODEL
Embeddings:            OPENAI_EMBEDDING_MODEL
```

Suggested initial values:

```text
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TTS_VOICE=marin
OPENAI_TRANSCRIBE_MODEL=gpt-4o-transcribe
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## AI Pipeline

### 1. Role/JD/Resume Analysis

Input:

- Job description text.
- Resume text.

Output:

```json
{
  "role_title": "string",
  "seniority_level": "entry | junior | mid | senior | lead | executive | unknown",
  "domain": "string",
  "must_have_skills": ["string"],
  "nice_to_have_skills": ["string"],
  "responsibilities": ["string"],
  "candidate_strengths": ["string"],
  "candidate_gaps": ["string"],
  "risk_areas": ["string"],
  "match_score": 0
}
```

### 2. Interview Plan Generation

Generate 10 base questions across these categories:

- `technical`
- `project_experience`
- `behavioral`
- `hr`
- `resume_gap`
- `jd_skill_validation`

Each question must include:

```json
{
  "question_number": 1,
  "category": "jd_skill_validation",
  "question_text": "string",
  "expected_signal": "what a strong answer should prove",
  "difficulty": "easy | medium | hard",
  "provenance": {
    "based_on": ["jd_required_skill", "resume_claim", "resume_gap"],
    "reason": "why this question matters"
  }
}
```

### 3. TTS Generation

Input:

- Question text.
- Interviewer style instruction.

Style:

```text
Speak like a strict but professional senior interviewer. Use a natural human-like delivery. Avoid cheerfulness, exaggerated emotion, and robotic pacing. Keep the tone calm, precise, and serious.
```

Output:

- Audio bytes stored in MinIO.
- `tts_object_key` stored on `interview_questions`.

### 4. Candidate Transcription

Input:

- Candidate answer audio from MinIO.

Output:

- Transcript.
- Optional duration metadata.
- Transcription status.

Transcription should not evaluate the answer. Keep transcription and evaluation separate.

### 5. Communication Signal Analysis

Use deterministic analysis where possible:

```text
word_count
words_per_minute
filler_word_count
hesitation_markers
answer_length_category
```

Filler words list:

```text
um, uh, like, basically, actually, you know, I mean, sort of, kind of, maybe, probably
```

The LLM may assess structure and clarity, but measurable signals should be computed in code.

### 6. Answer Evaluation

Evaluate each answer against:

- Original question.
- Question category.
- Expected signal.
- JD context.
- Resume context.
- Candidate transcript.
- Communication signals.
- Strict scoring rubric.

Scoring dimensions:

```text
relevance_score: 0-10
role_depth_score: 0-10
evidence_score: 0-10
structure_score: 0-10
jd_alignment_score: 0-10
communication_signal_score: 0-10
overall_score: 0-10
```

Strict feedback examples:

Good:

```text
The answer gives a relevant example, but it does not prove measurable ownership. A stronger response should include the problem, your specific action, and the result.
```

Avoid:

```text
Great job! You did amazing.
```

### 7. Final Report

Aggregate:

- Match analysis.
- All questions.
- All transcripts.
- All evaluations.
- Resume gaps.
- Skill gaps.

Output:

```json
{
  "readiness_score": 0,
  "hiring_recommendation": "maybe",
  "summary": "string",
  "jd_resume_match_summary": "string",
  "interview_performance_summary": "string",
  "skill_gaps": [],
  "answer_feedback": [],
  "resume_feedback": [],
  "improvement_plan": []
}
```

## Embeddings Strategy

Store embeddings for:

- JD chunks.
- Resume chunks.
- Candidate answer chunks.
- Evaluation rubric chunks.
- Question bank chunks.

Initial retrieval use cases:

1. Retrieve JD/resume chunks relevant to a question.
2. Retrieve rubric chunks for evaluation.
3. Retrieve similar prior question-bank chunks.
4. Retrieve previous answer chunks later for progress tracking.

## Chunking Rules

Start simple:

```text
chunk size: 500-900 words
chunk overlap: 80-120 words
preserve section labels when known
metadata: source, section, owner_type, session_id
```

Do not over-optimize chunking before the core interview flow works.

## Prompt Versioning

Prompt templates should include version identifiers.

Example:

```python
PROMPT_VERSION = "interview_plan_v1"
```

Store prompt version in output metadata when possible.
