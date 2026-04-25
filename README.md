# CueSpark Interview Coach

> A voice-based AI mock interview platform that analyzes a job description and resume, conducts a turn-based interview using human-like AI voice, transcribes candidate answers, evaluates performance, and generates a strict interviewer-style readiness report.

CueSpark Interview Coach is built with **FastAPI**, **Next.js**, **PostgreSQL + pgvector**, **Redis/RQ workers**, **MinIO**, and **OpenAI audio/LLM services**.

The first version is intentionally focused: **single-session mock interview**, no login, no billing, no recruiter dashboard, no real-time video room.

---

## 1. Product Summary

CueSpark Interview Coach helps job seekers and experienced professionals prepare for interviews when they do not have access to an expert mentor or interviewer.

The system accepts:

- A manually pasted **job description**
- A pasted or uploaded **resume/CV**
- Spoken candidate answers during the mock interview

It produces:

- JD-resume match score
- Role and candidate gap analysis
- Personalized interview questions
- AI-spoken interviewer questions
- Candidate answer transcript
- Strict answer evaluation
- Communication signal analysis
- Final interview readiness report

---

## 2. Core Scope

### In Scope for v1

- Manual job description input
- Resume upload and paste fallback
- Resume parsing for PDF/DOCX/text
- OCR-ready document status, but no OCR pipeline yet
- JD and resume chunking
- Embedding storage using PostgreSQL + pgvector
- Mixed interview generation
- Turn-based voice interview
- OpenAI-generated interviewer voice
- Candidate answer audio upload
- Candidate answer transcription
- Strict answer-by-answer evaluation
- Final readiness report
- Single-session demo mode without authentication

### Out of Scope for v1

- User login/accounts
- Billing/subscriptions
- Recruiter dashboard
- Real-time conversational interview
- Google Meet-style video room
- Monaco editor
- Code compiler
- Full OCR pipeline
- Video confidence analysis
- Emotion detection
- Custom voice cloning

---

## 3. Interview Categories

CueSpark generates a mixed interview across these categories:

| Category | Purpose |
| --- | --- |
| `technical` | Tests role-specific technical or functional competency |
| `project_experience` | Validates claimed experience and ownership |
| `behavioral` | Tests decision-making, conflict handling, accountability |
| `hr` | Checks motivation, communication, salary/notice-period style readiness |
| `resume_gap` | Probes unexplained gaps, weak areas, vague claims |
| `jd_skill_validation` | Checks direct alignment with required JD skills |

For non-software roles, `technical` means **role-specific competency**, not programming.

---

## 4. System Architecture

<p align="center">
<svg width="960" height="520" viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CueSpark system architecture diagram">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.16"/>
    </filter>
    <linearGradient id="blue" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#2563eb"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <linearGradient id="green" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>
    <linearGradient id="purple" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#7c3aed"/>
      <stop offset="100%" stop-color="#6d28d9"/>
    </linearGradient>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#475569" />
    </marker>
    <style>
      .title{font:700 22px Inter,Arial,sans-serif;fill:#0f172a}.label{font:700 15px Inter,Arial,sans-serif;fill:#fff}.sub{font:500 12px Inter,Arial,sans-serif;fill:#e2e8f0}.dark{font:700 15px Inter,Arial,sans-serif;fill:#0f172a}.muted{font:500 12px Inter,Arial,sans-serif;fill:#475569}.box{rx:18;filter:url(#shadow)}.line{stroke:#475569;stroke-width:2.4;fill:none;marker-end:url(#arrow)}
    </style>
  </defs>

  <rect width="960" height="520" fill="#f8fafc"/>
  <text x="40" y="46" class="title">CueSpark Interview Coach — System Architecture</text>

  <rect x="40" y="95" width="180" height="96" class="box" fill="url(#blue)"/>
  <text x="130" y="132" text-anchor="middle" class="label">Next.js Frontend</text>
  <text x="130" y="156" text-anchor="middle" class="sub">Setup · Interview · Report</text>

  <rect x="330" y="95" width="180" height="96" class="box" fill="url(#green)"/>
  <text x="420" y="132" text-anchor="middle" class="label">FastAPI Backend</text>
  <text x="420" y="156" text-anchor="middle" class="sub">REST APIs · Orchestration</text>

  <rect x="630" y="95" width="250" height="96" class="box" fill="url(#purple)"/>
  <text x="755" y="132" text-anchor="middle" class="label">OpenAI Services</text>
  <text x="755" y="156" text-anchor="middle" class="sub">LLM · TTS · Transcription · Embeddings</text>

  <path d="M220 143 H330" class="line"/>
  <path d="M510 143 H630" class="line"/>

  <rect x="70" y="285" width="180" height="96" class="box" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="160" y="322" text-anchor="middle" class="dark">MinIO Storage</text>
  <text x="160" y="346" text-anchor="middle" class="muted">Resume · Audio · Reports</text>

  <rect x="310" y="285" width="180" height="96" class="box" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="400" y="322" text-anchor="middle" class="dark">Redis + RQ</text>
  <text x="400" y="346" text-anchor="middle" class="muted">Background Jobs</text>

  <rect x="550" y="285" width="180" height="96" class="box" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="640" y="322" text-anchor="middle" class="dark">Worker</text>
  <text x="640" y="346" text-anchor="middle" class="muted">Parse · Embed · Evaluate</text>

  <rect x="770" y="285" width="150" height="96" class="box" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="845" y="322" text-anchor="middle" class="dark">Postgres</text>
  <text x="845" y="346" text-anchor="middle" class="muted">Tables + pgvector</text>

  <path d="M390 191 C360 230 250 250 180 285" class="line"/>
  <path d="M420 191 V285" class="line"/>
  <path d="M490 333 H550" class="line"/>
  <path d="M730 333 H770" class="line"/>
  <path d="M640 285 C660 238 700 215 755 191" class="line"/>
  <path d="M755 191 C790 220 830 240 845 285" class="line"/>

  <rect x="40" y="430" width="880" height="48" rx="14" fill="#e2e8f0"/>
  <text x="480" y="460" text-anchor="middle" class="dark">Frontend calls product APIs. Backend enqueues long-running jobs. Worker performs AI/file/database operations.</text>
</svg>
</p>

---

## 5. Product Flow

<p align="center">
<svg width="960" height="360" viewBox="0 0 960 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CueSpark interview product flow diagram">
  <defs>
    <marker id="arrow2" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#334155" />
    </marker>
    <filter id="s2" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#0f172a" flood-opacity="0.13"/>
    </filter>
    <style>
      .h{font:700 22px Inter,Arial,sans-serif;fill:#0f172a}.t{font:700 14px Inter,Arial,sans-serif;fill:#0f172a}.m{font:500 11px Inter,Arial,sans-serif;fill:#475569}.node{rx:16;filter:url(#s2);fill:#fff;stroke:#cbd5e1}.line{stroke:#334155;stroke-width:2.2;fill:none;marker-end:url(#arrow2)}.pill{font:700 11px Inter,Arial,sans-serif;fill:#fff}
    </style>
  </defs>

  <rect width="960" height="360" fill="#f8fafc"/>
  <text x="40" y="42" class="h">Candidate Journey</text>

  <rect x="40" y="95" width="135" height="82" class="node"/>
  <text x="108" y="126" text-anchor="middle" class="t">Add JD</text>
  <text x="108" y="149" text-anchor="middle" class="m">Manual paste</text>

  <rect x="210" y="95" width="135" height="82" class="node"/>
  <text x="278" y="126" text-anchor="middle" class="t">Add Resume</text>
  <text x="278" y="149" text-anchor="middle" class="m">Upload or paste</text>

  <rect x="380" y="95" width="135" height="82" class="node"/>
  <text x="448" y="126" text-anchor="middle" class="t">Analyze Fit</text>
  <text x="448" y="149" text-anchor="middle" class="m">Score + gaps</text>

  <rect x="550" y="95" width="135" height="82" class="node"/>
  <text x="618" y="126" text-anchor="middle" class="t">Generate Plan</text>
  <text x="618" y="149" text-anchor="middle" class="m">10 questions</text>

  <rect x="720" y="95" width="160" height="82" class="node"/>
  <text x="800" y="126" text-anchor="middle" class="t">Start Interview</text>
  <text x="800" y="149" text-anchor="middle" class="m">Turn-based voice</text>

  <path d="M175 136 H210" class="line"/>
  <path d="M345 136 H380" class="line"/>
  <path d="M515 136 H550" class="line"/>
  <path d="M685 136 H720" class="line"/>

  <rect x="165" y="245" width="160" height="82" class="node"/>
  <text x="245" y="276" text-anchor="middle" class="t">Record Answer</text>
  <text x="245" y="299" text-anchor="middle" class="m">Candidate audio</text>

  <rect x="400" y="245" width="160" height="82" class="node"/>
  <text x="480" y="276" text-anchor="middle" class="t">Transcribe</text>
  <text x="480" y="299" text-anchor="middle" class="m">OpenAI STT</text>

  <rect x="635" y="245" width="160" height="82" class="node"/>
  <text x="715" y="276" text-anchor="middle" class="t">Evaluate</text>
  <text x="715" y="299" text-anchor="middle" class="m">Strict feedback</text>

  <path d="M800 177 C790 220 725 235 715 245" class="line"/>
  <path d="M715 245 C630 210 335 210 245 245" class="line"/>
  <path d="M325 286 H400" class="line"/>
  <path d="M560 286 H635" class="line"/>

  <rect x="814" y="256" width="82" height="28" rx="14" fill="#2563eb"/>
  <text x="855" y="275" text-anchor="middle" class="pill">Report</text>
</svg>
</p>

---

## 6. AI and Audio Pipeline

<p align="center">
<svg width="960" height="440" viewBox="0 0 960 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AI audio and evaluation pipeline diagram">
  <defs>
    <filter id="s3" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#0f172a" flood-opacity="0.13"/>
    </filter>
    <marker id="arrow3" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#475569" />
    </marker>
    <style>
      .h{font:700 22px Inter,Arial,sans-serif;fill:#0f172a}.t{font:700 14px Inter,Arial,sans-serif;fill:#0f172a}.m{font:500 11px Inter,Arial,sans-serif;fill:#475569}.node{rx:16;filter:url(#s3);fill:#fff;stroke:#cbd5e1}.ai{rx:16;filter:url(#s3);fill:#eef2ff;stroke:#818cf8}.store{rx:16;filter:url(#s3);fill:#ecfdf5;stroke:#34d399}.line{stroke:#475569;stroke-width:2.2;fill:none;marker-end:url(#arrow3)}
    </style>
  </defs>

  <rect width="960" height="440" fill="#f8fafc"/>
  <text x="40" y="42" class="h">AI Voice, Transcription, and Evaluation Pipeline</text>

  <rect x="50" y="100" width="170" height="76" class="node"/>
  <text x="135" y="130" text-anchor="middle" class="t">Question Text</text>
  <text x="135" y="153" text-anchor="middle" class="m">Generated from JD + resume</text>

  <rect x="295" y="100" width="170" height="76" class="ai"/>
  <text x="380" y="130" text-anchor="middle" class="t">OpenAI TTS</text>
  <text x="380" y="153" text-anchor="middle" class="m">Human-like interviewer voice</text>

  <rect x="540" y="100" width="170" height="76" class="store"/>
  <text x="625" y="130" text-anchor="middle" class="t">Store Audio</text>
  <text x="625" y="153" text-anchor="middle" class="m">MinIO question MP3</text>

  <rect x="760" y="100" width="150" height="76" class="node"/>
  <text x="835" y="130" text-anchor="middle" class="t">Play in UI</text>
  <text x="835" y="153" text-anchor="middle" class="m">Candidate listens</text>

  <path d="M220 138 H295" class="line"/>
  <path d="M465 138 H540" class="line"/>
  <path d="M710 138 H760" class="line"/>

  <rect x="70" y="260" width="170" height="76" class="node"/>
  <text x="155" y="290" text-anchor="middle" class="t">Record Answer</text>
  <text x="155" y="313" text-anchor="middle" class="m">Browser microphone</text>

  <rect x="305" y="260" width="170" height="76" class="store"/>
  <text x="390" y="290" text-anchor="middle" class="t">Upload Audio</text>
  <text x="390" y="313" text-anchor="middle" class="m">MinIO answer file</text>

  <rect x="540" y="260" width="170" height="76" class="ai"/>
  <text x="625" y="290" text-anchor="middle" class="t">Transcribe</text>
  <text x="625" y="313" text-anchor="middle" class="m">OpenAI STT</text>

  <rect x="760" y="260" width="150" height="76" class="ai"/>
  <text x="835" y="290" text-anchor="middle" class="t">Evaluate</text>
  <text x="835" y="313" text-anchor="middle" class="m">Rubric + context</text>

  <path d="M835 176 C850 215 220 220 155 260" class="line"/>
  <path d="M240 298 H305" class="line"/>
  <path d="M475 298 H540" class="line"/>
  <path d="M710 298 H760" class="line"/>
</svg>
</p>

Recommended OpenAI usage:

| Capability | Recommended Model |
| --- | --- |
| Interviewer voice | `gpt-4o-mini-tts` |
| Candidate transcription | `gpt-4o-transcribe` |
| Lower-cost transcription fallback | `gpt-4o-mini-transcribe` |
| Legacy transcription fallback | `whisper-1` |
| Embeddings | `text-embedding-3-small` |
| Evaluation / reasoning | `gpt-4o-mini` or stronger model when needed |

---

## 7. Database and Storage Design

<p align="center">
<svg width="960" height="500" viewBox="0 0 960 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Database and object storage design diagram">
  <defs>
    <filter id="s4" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#0f172a" flood-opacity="0.13"/>
    </filter>
    <marker id="arrow4" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#64748b" />
    </marker>
    <style>
      .h{font:700 22px Inter,Arial,sans-serif;fill:#0f172a}.t{font:700 14px Inter,Arial,sans-serif;fill:#0f172a}.m{font:500 11px Inter,Arial,sans-serif;fill:#475569}.db{rx:16;filter:url(#s4);fill:#eff6ff;stroke:#60a5fa}.obj{rx:16;filter:url(#s4);fill:#f0fdf4;stroke:#4ade80}.vec{rx:16;filter:url(#s4);fill:#faf5ff;stroke:#c084fc}.line{stroke:#64748b;stroke-width:2.1;fill:none;marker-end:url(#arrow4)}
    </style>
  </defs>

  <rect width="960" height="500" fill="#f8fafc"/>
  <text x="40" y="42" class="h">Structured Data, Vector Data, and File Storage</text>

  <rect x="60" y="105" width="205" height="70" class="db"/>
  <text x="162" y="134" text-anchor="middle" class="t">interview_sessions</text>
  <text x="162" y="155" text-anchor="middle" class="m">Session status + summary</text>

  <rect x="60" y="215" width="205" height="70" class="db"/>
  <text x="162" y="244" text-anchor="middle" class="t">documents</text>
  <text x="162" y="265" text-anchor="middle" class="m">JD/resume text + parse status</text>

  <rect x="60" y="325" width="205" height="70" class="db"/>
  <text x="162" y="354" text-anchor="middle" class="t">interview_questions</text>
  <text x="162" y="375" text-anchor="middle" class="m">Question plan + TTS key</text>

  <rect x="365" y="105" width="205" height="70" class="db"/>
  <text x="468" y="134" text-anchor="middle" class="t">candidate_answers</text>
  <text x="468" y="155" text-anchor="middle" class="m">Audio key + transcript</text>

  <rect x="365" y="215" width="205" height="70" class="db"/>
  <text x="468" y="244" text-anchor="middle" class="t">answer_evaluations</text>
  <text x="468" y="265" text-anchor="middle" class="m">Scores + strict feedback</text>

  <rect x="365" y="325" width="205" height="70" class="db"/>
  <text x="468" y="354" text-anchor="middle" class="t">interview_reports</text>
  <text x="468" y="375" text-anchor="middle" class="m">Final readiness report</text>

  <rect x="675" y="105" width="205" height="100" class="vec"/>
  <text x="778" y="139" text-anchor="middle" class="t">embedding_chunks</text>
  <text x="778" y="162" text-anchor="middle" class="m">JD · resume · answers</text>
  <text x="778" y="182" text-anchor="middle" class="m">rubric · question bank</text>

  <rect x="675" y="275" width="205" height="100" class="obj"/>
  <text x="778" y="309" text-anchor="middle" class="t">MinIO</text>
  <text x="778" y="332" text-anchor="middle" class="m">resumes/original/...</text>
  <text x="778" y="352" text-anchor="middle" class="m">audio/questions · answers</text>

  <path d="M265 140 H365" class="line"/>
  <path d="M265 250 H365" class="line"/>
  <path d="M265 360 H365" class="line"/>
  <path d="M570 140 H675" class="line"/>
  <path d="M570 250 C630 250 635 325 675 325" class="line"/>
  <path d="M570 360 C630 360 635 325 675 325" class="line"/>
  <path d="M265 250 C410 430 640 420 778 375" class="line"/>
</svg>
</p>

Core tables:

```txt
interview_sessions
materials / documents
interview_questions
candidate_answers
answer_evaluations
interview_reports
embedding_chunks
```

Suggested MinIO object paths:

```txt
resumes/original/{session_id}/{filename}
audio/questions/{question_id}.mp3
audio/answers/{answer_id}.webm
reports/{session_id}.json
```

---

## 8. Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js App Router |
| Backend API | FastAPI |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Queue | Redis + RQ |
| Worker | Python RQ worker |
| Object Storage | MinIO |
| AI Provider | OpenAI |
| Interviewer Voice | OpenAI TTS |
| Transcription | OpenAI transcription / Whisper-compatible flow |
| Local Runtime | Docker Compose |

---

## 9. Quick Start

```bash
cp .env.example .env
docker compose up --build
```

| Service | URL |
| --- | --- |
| Web | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MinIO Console | http://localhost:9001 |
| Postgres | localhost:5432 |
| Redis | localhost:6379 |

Default MinIO credentials:

```txt
minioadmin / minioadmin
```

Change these in `.env` before deploying outside local development.

---

## 10. Required Environment Variables

```env
OPENAI_API_KEY=

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=cuespark_interview
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=cuespark
MINIO_SECURE=false

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## 11. Project Layout

```txt
.
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routers
│   │   ├── core/             # config, logging, db, redis, storage clients
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic request/response contracts
│   │   ├── services/         # business logic and AI services
│   │   ├── tasks/            # background jobs
│   │   └── workers/          # worker entrypoints
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # UI components
│   │   ├── hooks/            # frontend hooks
│   │   └── lib/              # API client and utilities
│   ├── package.json
│   └── Dockerfile
│
├── docs/                     # project architecture and implementation docs
├── tasks/                    # phase-based implementation tasks
├── infra/
│   └── minio-init.sh          # creates default MinIO bucket
├── docker-compose.yml
├── .env.example
├── AGENTS.md                 # Codex/AI development instructions
└── README.md
```

---

## 12. Backend Modules

Expected backend modules:

```txt
backend/app/api/
├── sessions.py
├── documents.py
├── interview.py
├── audio.py
├── reports.py

backend/app/services/
├── openai_client.py
├── document_parser.py
├── chunking.py
├── embeddings.py
├── match_analyzer.py
├── question_generator.py
├── tts.py
├── transcription.py
├── communication_analysis.py
├── answer_evaluator.py
├── report_generator.py

backend/app/tasks/
├── prepare_session.py
├── generate_question_audio.py
├── transcribe_answer.py
├── evaluate_answer.py
├── generate_report.py
```

Rules:

- Keep route handlers thin.
- Keep OpenAI calls inside service modules.
- Use workers for slow jobs.
- Store large artifacts in MinIO.
- Store structured state in Postgres.
- Store semantic chunks in pgvector.

---

## 13. Frontend Routes

Expected frontend flow:

```txt
/
  Landing / start page

/setup
  JD and resume input

/session/[sessionId]/match
  Match score and interview readiness preview

/session/[sessionId]/interview
  Turn-based mock interview

/session/[sessionId]/report
  Final strict interviewer report
```

The interview page should support:

- Current question display
- Interview category label
- Audio playback for AI interviewer
- Candidate audio recording
- Upload and submit answer
- Transcript preview
- Strict feedback after evaluation
- Next question navigation

---

## 14. Background Job Flow

Long-running operations should run in the worker.

```txt
prepare_session
  parse resume
  chunk JD/resume
  generate embeddings
  calculate match score
  generate base questions

generate_question_audio
  create interviewer TTS audio
  store audio in MinIO

transcribe_answer
  send candidate audio for transcription
  store transcript

evaluate_answer
  evaluate answer using transcript, JD, resume, question, and rubric

generate_report
  generate final readiness report
```

Frontend should call product-specific endpoints. The backend may internally enqueue and track worker jobs.

---

## 15. Scoring Model

Each answer should be evaluated using a strict interviewer rubric.

Suggested answer score dimensions:

| Metric | Weight |
| --- | ---: |
| Relevance to question | 20% |
| Role-specific depth | 20% |
| Evidence and examples | 20% |
| Clarity and structure | 15% |
| JD alignment | 15% |
| Communication signal | 10% |

The final report should include:

1. Overall readiness score
2. Hiring-style recommendation
3. JD-resume match analysis
4. Interview performance summary
5. Answer-by-answer feedback
6. Skill gaps
7. Resume improvement suggestions
8. Suggested preparation plan

---

## 16. Communication Signals

The app may estimate communication quality from measurable signals:

- Transcript length
- Word count
- Speaking speed
- Filler words
- Repetition
- Structure
- Clarity
- Hesitation markers
- Relevance to the question

Use the phrase:

```txt
communication signal score
```

Do not claim:

```txt
emotion detection
true confidence detection
personality detection
psychological profiling
```

---

## 17. Evaluation Tone

The report tone should be **strict but professional**.

Preferred:

```txt
The answer lacks evidence of ownership and would not satisfy an experienced interviewer.
```

Avoid:

```txt
Good try! You can improve a little bit.
```

Avoid unsupported claims:

```txt
The candidate is confident.
```

Use measurable language:

```txt
The answer was structured, but it contained repeated hesitation markers and lacked role-specific evidence.
```

---

## 18. Documentation

Project documentation should live in:

```txt
docs/
```

Recommended docs:

```txt
docs/00-project-overview.md
docs/01-architecture.md
docs/02-backend-design.md
docs/03-database-design.md
docs/04-ai-audio-rag-design.md
docs/05-frontend-flow.md
docs/06-api-contracts.md
docs/07-codex-development-rules.md
```

---

## 19. Task-Based Development

Implementation tasks should live in:

```txt
tasks/
```

Recommended phase structure:

```txt
tasks/
├── phase0-foundation/
├── phase1-session-documents/
├── phase2-interview-engine/
├── phase3-answer-evaluation/
├── phase4-report-frontend/
└── phase5-future-scope/
```

When using Codex or another coding agent, give it one task file at a time.

Recommended instruction:

```txt
Read AGENTS.md, the relevant docs, and only the selected task file.
Implement only the selected task.
Do not add out-of-scope features.
Report changed files and verification steps.
```

---

## 20. Development Commands

```bash
make dev
```

Start the full local stack.

```bash
make logs
```

Tail service logs.

```bash
make shell-api
```

Open a shell inside the API container.

```bash
make worker-restart
```

Restart the worker after changing background tasks.

If Makefile commands are unavailable, use Docker Compose directly:

```bash
docker compose up --build
docker compose logs -f
docker compose restart worker
```

---

## 21. Development Rules

- Keep v1 single-session.
- Do not add login until explicitly required.
- Do not add billing.
- Do not add recruiter dashboards.
- Do not build real-time video interview mode yet.
- Do not build OCR now; only support `ocr_required` as a parse status.
- Do not hardcode OpenAI calls inside route handlers.
- Keep AI calls inside service modules.
- Use background workers for slow operations.
- Store large files in MinIO.
- Store structured data in Postgres.
- Store embeddings in pgvector.
- Keep frontend API calls inside `frontend/src/lib`.
- Prefer small, testable modules over large monolithic files.

---

## 22. First Stable Milestone

The first stable milestone is:

```txt
A candidate can paste a JD, upload or paste a resume, generate a personalized interview, hear AI-spoken questions, record spoken answers, receive transcriptions, get strict answer feedback, and view a final readiness report.
```

That is the core product.
