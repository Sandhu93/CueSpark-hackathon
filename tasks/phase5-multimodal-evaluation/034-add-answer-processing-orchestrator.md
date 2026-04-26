# Task: Add Answer Processing Orchestrator

## Goal

Make candidate answer submission trigger the correct downstream processing pipeline automatically.

Right now answer submission may create a `candidate_answers` row and return a stored/pending status, but the full product flow requires the relevant modality agents, benchmark gap analysis, and final evaluation to run after submission.

This task connects answer capture to the multimodal evaluation pipeline.

## Why This Task Exists

CueSpark's production flow should be:

```txt
Candidate submits answer
  -> answer stored
  -> relevant modality agents run
  -> benchmark gap coverage agent runs
  -> final evaluation orchestrator runs
  -> answer status becomes evaluated or failed
```

Without this task, the frontend can submit answers but feedback may not appear automatically.

## Scope

Implement only:

- Add an answer processing orchestration task, for example:

```txt
backend/app/tasks/process_answer_pipeline.py
```

- Enqueue the processing pipeline after successful answer submission.
- Decide which agent steps to run based on:
  - `answer_mode`
  - question `response_mode`
  - `requires_audio`
  - `requires_text`
  - `requires_code`
  - `requires_video`
  - presence of submitted audio/text/code/visual metadata
- Run or enqueue relevant steps:
  - audio agent for spoken/mixed audio answers
  - text answer agent for written/mixed text answers
  - code evaluation agent for code/mixed code answers
  - video signal agent only when visual metadata exists or `requires_video=true`
  - benchmark gap coverage agent after primary modality agents
  - final evaluation orchestrator after benchmark gap coverage
- Update answer processing status through the lifecycle.
- Store failures in agent result rows or answer processing metadata.
- Keep the pipeline idempotent enough that retry does not create duplicate conflicting outputs.

## Recommended MVP Approach

For the first production version, prefer a single worker-level orchestration task:

```txt
process_answer_pipeline(answer_id)
```

Inside that worker task, call the required services in order and store `agent_results` as each step completes.

This is simpler than trying to build complex RQ job chaining immediately.

Later, each agent can become a separate queue job if scaling requires it.

## Out of Scope

Do not implement:

- New agent analysis logic if the agent service already exists.
- New frontend UI.
- Report generation.
- PDF export.
- Email export.
- WebRTC.
- Full video upload.
- Sandboxed code execution.

## Files Likely Involved

- `backend/app/api/interview.py`
- `backend/app/tasks/process_answer_pipeline.py`
- `backend/app/tasks/__init__.py` or task registry file
- `backend/app/models/answer.py`
- `backend/app/models/question.py`
- `backend/app/models/agent_result.py`
- `backend/app/services/audio_agent.py`
- `backend/app/services/text_answer_agent.py`
- `backend/app/services/code_evaluation_agent.py`
- `backend/app/services/video_signal_agent.py`
- `backend/app/services/benchmark_gap_agent.py`
- `backend/app/services/final_evaluation_orchestrator.py`
- `backend/tests/`

## Processing Status Guidance

Use or align with existing statuses:

```txt
stored
queued
processing
transcribing
running_agents
evaluating
evaluated
failed
```

If the model currently only supports fewer statuses, keep the implementation compatible and avoid unnecessary schema churn unless a previous task already added these states.

## Pipeline Logic

Pseudo-flow:

```python
submit_answer(...):
    answer = create_candidate_answer(...)
    enqueue(process_answer_pipeline, answer.id)
    return {
        "answer_id": answer.id,
        "processing_status": "queued"
    }
```

Worker flow:

```python
process_answer_pipeline(answer_id):
    answer = load_answer(answer_id)
    question = load_question(answer.question_id)

    mark_answer_processing(answer)

    if answer_has_audio_or_question_requires_audio:
        run_audio_agent(answer)

    if answer_has_text_or_question_requires_text:
        run_text_answer_agent(answer)

    if answer_has_code_or_question_requires_code:
        run_code_evaluation_agent(answer)

    if answer_has_visual_metadata_or_question_requires_video:
        run_video_signal_agent(answer)

    run_benchmark_gap_agent(answer, question)
    run_final_evaluation_orchestrator(answer)

    mark_answer_evaluated(answer)
```

## Idempotency Rules

- Do not create duplicate successful `agent_results` for the same `answer_id + agent_type` if one already exists.
- Retrying a failed pipeline may replace failed agent results or create a new attempt depending on existing project patterns.
- The final answer evaluation should be updated or replaced predictably.
- Avoid deleting original submitted content.

## Acceptance Criteria

- [ ] Answer submission enqueues processing automatically.
- [ ] Spoken answers trigger audio agent, benchmark gap agent, and final evaluator.
- [ ] Written answers trigger text answer agent, benchmark gap agent, and final evaluator.
- [ ] Code answers trigger code evaluation agent, benchmark gap agent, and final evaluator.
- [ ] Mixed answers trigger only the relevant available/required modality agents.
- [ ] Optional video signal processing runs only when data exists or is required.
- [ ] Processing status progresses from stored/queued to evaluated or failed.
- [ ] Failed agent steps are stored clearly.
- [ ] Re-running the pipeline does not create confusing duplicate results.
- [ ] No report generation is implemented in this task.

## Verification

Run:

```bash
pytest backend/tests
```

Manual checks:

```bash
# Submit spoken answer and confirm processing is queued
POST /api/questions/{question_id}/answers

# Fetch answer and confirm agent results/evaluation appear after worker runs
GET /api/answers/{answer_id}
```

Test at least:

- spoken answer
- written answer
- code answer
- mixed answer where supported

## Notes for Codex

- This is an integration task, not a new AI capability task.
- Reuse existing agent services and schemas.
- Keep route handlers thin.
- Prefer one worker orchestration task for MVP simplicity.
- Do not generate the final session report automatically unless a later task explicitly asks for it.
