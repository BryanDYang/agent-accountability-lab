# Milestone 1 Project Proposal

## Meeting Follow-Through Assistant

**Course:** CIS-5980

**Track:** AI Engineering

**Team:** Bryan Yang, Will Liu, and Guadalupe Cantera

**Status:** Working proposal for the new project direction

**Updated:** September 8, 2026

Course, track, and team names are carried forward from the previous proposal. Roles, schedule, budget, and evaluation targets below are proposed for team review. Official Canvas requirements and submission dates have not yet been verified.

## 1. Project Explanation and Motivation

Recurring research meetings produce commitments, decisions, and deadlines that are difficult to maintain across weeks. An advisor may promise to send papers, a student may agree to rerun an experiment, and both may leave without a dependable record of who owes what. Transcripts and summaries help people remember a meeting, but follow-through requires connecting later conversations to earlier commitments, recognizing changes, and preserving the evidence behind each update. The project sponsor already has a recording-to-transcript-and-summary tool; the proposed project builds the assistant layer that turns those individual meeting records into useful ongoing project memory.

We propose a meeting follow-through assistant for advisors, students, and small research teams. It will ingest meeting recordings, produce timestamped transcripts and concise summaries, extract named commitments and decisions, and maintain a living action-item list organized by person and project. When a later meeting reports progress, the assistant will match the statement to an existing item and update its status with a source citation, asking for review when the match is ambiguous. Users will also be able to ask questions about prior meetings and inspect the supporting transcript passages. The central engineering contribution is an evaluated workflow for maintaining commitments across meetings, with traceable changes, correction controls, and explicit uncertainty.

**Engineering question:** Can an assistant reliably maintain commitments across a sequence of meetings while reducing manual reconciliation and avoiding unsupported task updates?

## 2. Users and Example Workflow

The primary users are a PhD advisor and their students. A secondary development setting is our own consenting project team or study group.

1. Before recording, participants agree to recording and the intended processing and retention policy.
2. After Tuesday's meeting, a user uploads the recording and selects the project, attendees, meeting date, and timezone.
3. The assistant produces a transcript and a short summary with decisions and commitments. Users can correct speaker names and extraction errors.
4. The task board shows that the student owns the baseline rerun and the advisor owns sending two papers. Missing due dates remain unspecified.
5. A paper deadline five weeks away can seed a suggested backward plan. Suggested intermediate dates are labeled as proposals until accepted.
6. At the next meeting, “I finished the baseline rerun” updates the matching task to done if the owner, project, and evidence support the match. The update links to this new statement and retains the original commitment.
7. The advisor's unsent papers remain open and appear in an in-app pre-meeting brief. Silence never marks a task done or dropped.
8. A question such as “What did we decide about the baseline last month?” returns an answer with meeting and timestamp citations, or states that the available evidence is insufficient.

The MVP provides in-app summaries and reminders. Automatic email delivery and external calendar changes require a later integration and are outside the required demonstration.

## 3. Terms and Observable Outputs

| Term | Definition and output |
|---|---|
| Transcription | Converts speech into timestamped text; it does not establish speaker identity. |
| Transcript cleanup | Edits recognition errors, punctuation, and filler without changing meaning; it produces a separate cleaned version linked to the original segments. |
| Diarization | Separates stretches of audio by voice; it produces speaker labels, not names. |
| Speaker identification | Maps speaker labels to attendee names with user confirmation; an attendee list alone does not establish who spoke. |
| Action item | A named person's commitment to a specific task, with an optional due date, status, and source timestamp; an unowned suggestion remains a candidate for clarification. |
| Decision | A statement settling a question, stored with its source; a later reversal is a linked new decision rather than an overwrite. |
| Reconciliation | Matches a later statement to an existing commitment and proposes or records an evidenced change; similar wording alone is insufficient. |
| Summary | A concise account of discussion, decisions, and commitments evaluated for faithfulness, coverage, and usefulness. |
| Suggested plan | Proposed steps working backward from a confirmed deadline; its invented intermediate dates are not meeting commitments. |
| Consent | Recorded agreement by every participant to the stated recording and processing policy before audio processing; an upload alone is not evidence of everyone's agreement. |

## 4. Scope and Deliverable

### Required MVP

- Upload recorded audio and import existing timestamped transcripts.
- Transcribe and diarize audio, then let users confirm or correct speaker mappings.
- Generate structured decisions, commitments, and a concise summary with source references.
- Maintain open, done, and dropped tasks across meeting sequences, including owner and deadline changes.
- Present ambiguous matches for review and provide correction and undo with change history.
- Provide meeting, person, and project views, plus an in-app brief of outstanding and overdue items.
- Answer historical questions using retrieved evidence with clickable transcript timestamps.
- Generate a reviewable backward plan from a user-confirmed deadline.
- Demonstrate consent gating, selective exclusion, deletion, and project-scoped retrieval.
- Deliver a local application, reproducible evaluation fixtures, measured results, and setup documentation.

### Stretch goals

iPhone capture, Zoom ingestion, slide-aware summaries, calendar/task-service integration, and automatic scheduled notifications. Voice-profile enrollment is also deferred; manual speaker confirmation is sufficient for the MVP.

### Boundaries

The project will not train a speech model, infer productivity scores, monitor people without consent, deploy a production multi-tenant service, or claim to establish real-world task completion beyond what participants report. Initial evaluation covers English-language small-group meetings; broader language and setting claims require additional evidence.

## 5. Architecture and AI Engineering

```text
Recording + attendees + date/timezone + consent record
                         |
             Consent gate and private storage
                         |
       Transcription -> diarization -> speaker confirmation
                         |
       Original segments + aligned cleaned transcript
                         |
        Structured summary, decision, and task extraction
                         |
        Retrieve existing tasks within the same project
                         |
         Match later mentions and propose state changes
                         |
       Validate evidence -> apply or request human review
                         |
       Task history + person/project views + meeting brief

Historical question -> project-scoped retrieval -> cited answer
Confirmed deadline -> suggested plan -> user acceptance
```

The AI work comprises structured extraction, semantic task matching, evidence-grounded summarization, and retrieval-augmented answers. Application code validates schemas, source references, project boundaries, and permitted state transitions. Transcript content is untrusted data and cannot authorize tool execution or change system instructions.

Each task has a stable ID, project ID, owner ID, description, nullable due date, status, and original source segment. Each update records the task ID, previous and new values, evidence segment, meeting date, processing time, and whether a user or model proposed and accepted it. Unresolved candidates are kept separately from accepted tasks. An update cannot reference a nonexistent segment or silently move a task into another project.

Processing is idempotent: re-uploading or retrying a meeting must not duplicate accepted tasks. Meetings are reconciled in event order; importing older meetings must not silently overwrite newer task state. Speaker and transcript corrections invalidate dependent outputs for review or recomputation. Search indexes and cached outputs follow source deletions.

### Preliminary implementation choices

| Layer | Proposed choice and purpose |
|---|---|
| Interface | React, TypeScript, and a consistent accessible component library for transcript, task, and review views |
| Service | Python with FastAPI and schema validation for ingestion, extraction, and task operations |
| Speech | Inspect the sponsor's existing pipeline first; use Whisper and pyannote.audio if reuse is unavailable or unsuitable |
| Persistence | SQLite for the local MVP, local private audio storage, and timestamped transcript segments |
| Retrieval | Project-filtered text search plus embeddings when pilot evidence justifies semantic retrieval; keep source IDs attached throughout |
| Model integration | One configured LLM behind a small adapter, with structured outputs and bounded retries; exact model selected after a quality/cost pilot |
| Verification | Pytest for extraction/state behavior and Playwright for upload, review, correction, and citation workflows |
| Observability | Record model/prompt versions, usage, processing failures, stage latency, and cost per hour of audio |

No sponsor code is assumed available or licensed until inspected. Transcript imports allow development of the core follow-through workflow while audio integration proceeds. Prompt caching is an optional measured optimization after correctness is established.

## 6. Evaluation Plan

### Data and experimental design

Target 18 short meetings arranged into six independent three-meeting project sequences, using consenting team meetings and purpose-recorded scenarios. Split whole sequences into three development, one validation, and two held-out test sequences. Keep scenario variants and overlapping source material together to prevent leakage. These are pilot-scale targets, not a claim of statistical representativeness. Report counts and uncertainty, and expand the held-out set if feasible.

Two team members independently annotate the held-out commitments, owners, deadlines, decisions, links between meetings, and state changes, then resolve disagreements before scoring. Include completion, partial completion, reassignment, changed deadlines, dropped tasks, duplicate mentions, similar tasks in different projects, uncertain speakers, negation, and tasks never mentioned again. Include answerable and unanswerable historical questions. Freeze prompts and thresholds before held-out evaluation.

Compare two conditions using the same transcripts, model, and extraction settings:

1. **Independent meeting extraction:** Produce each meeting's summary and task list without reconciling earlier tasks.
2. **Persistent reconciliation:** Use the same extraction plus existing task state and source-backed updates.

Score both against the expected current task list after each meeting, counting duplicates, stale open items, unsupported changes, and missing tasks. Separately compare a simple lexical task matcher with semantic reconciliation to test the value of the matching component. Evaluate on corrected transcripts and raw pipeline outputs to distinguish reasoning failures from speech and speaker errors.

### Metrics and provisional success criteria

These are proposed acceptance targets, not measured results. Calibrate them on development and validation data before freezing the test protocol.

| Output | Measurement | Proposed target |
|---|---|---|
| Extracted commitments | Precision and recall against adjudicated tasks; a match requires the correct owner and equivalent commitment | Precision >= 90%, recall >= 80% |
| Cross-meeting updates | Correct task link and requested field/status change among automatic updates | Precision >= 95%; also report recall and automatic-update coverage |
| Current task list | Correct owner, description, status, and supported due date after each meeting | Higher state accuracy than independent extraction; report absolute difference and raw counts |
| False completion | Unsupported done transitions divided by all automatic done transitions | Zero observed in the held-out demo set, with sample size reported |
| Human review burden | Fraction of candidate updates requiring review and review time | Report alongside accuracy; no success claim from routing everything to review |
| Historical answers | Correct answer and citations that support each substantive claim | >= 90% supported-answer rate; separately score abstention on unanswerable questions |
| Summaries | Human rubric for faithfulness, coverage, and usefulness | Mean >= 4/5 on each dimension, with no invented owner or deadline in the final demo |
| Audio and speakers | Word error rate on selected hand-transcribed segments; diarization error and owner-attribution accuracy | Report by recording condition; diagnose impact on downstream task errors |
| Plans | Confirmed final deadline respected; suggested dates labeled; no unaccepted step becomes a commitment | All deterministic checks pass |
| System behavior | Duplicate ingestion, correction, deletion, consent gating, project isolation, citation navigation | All required end-to-end scenarios pass |
| Efficiency | End-to-end and stage latency, tokens, cost per audio hour, and manual reconciliation time | Report hardware/model and median/range; set operational budget after pilot |

Summary rubric anchors: **1** = materially incorrect or unusable, **3** = mostly correct but requires substantive editing, **5** = faithful and immediately useful. Scores 2 and 4 represent intermediate quality. Reviewers score dimensions separately. An LLM judge may assist error triage but will not replace human ground truth for ownership, dates, completion, or citation support.

### Minimum end-to-end demonstration

Run a three-meeting sequence in which the first meeting creates two owned tasks and a decision, the second completes one task and changes the other's deadline, and the third leaves the remaining task open. Include an ambiguous mention that requests review, a cited historical question, and a correction. Re-import a recording to demonstrate no duplication, then delete a meeting to demonstrate removal of associated searchable content and explicit handling of dependent task evidence.

## 7. Related Work and Product Positioning

The following references inform component selection and evaluation; they are not evidence that the complete proposed workflow already works.

| Source | Relevance and boundary |
|---|---|
| [Whisper, Radford et al., 2022](https://arxiv.org/abs/2212.04356) | Speech recognition foundation; assess our recordings rather than assuming accurate domain terminology or speaker attribution. |
| [pyannote.audio](https://github.com/pyannote/pyannote-audio) | Speaker diarization tools; named attendee mapping remains a separate step. |
| [QMSum, Zhong et al., 2021](https://arxiv.org/abs/2104.05938) | Query-based meeting summarization benchmark for retrieval and summary experiments; does not establish our longitudinal task-state ground truth. |
| [MeetingBank, Hu et al., 2023](https://arxiv.org/abs/2305.17529) | Public meeting summarization benchmark; municipal meetings differ from recurring advisor/student meetings. |
| [AMI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/corpus/) | Candidate meeting audio and annotation source; inspect available annotations and permitted use before selecting a subset. |

Preliminary product review, checked September 8, 2026:

| Product | Documented strength | Implication for this proposal |
|---|---|---|
| [Otter](https://help.otter.ai/hc/en-us/articles/25983095114519-Action-Items-Overview) | Consolidates assigned action items across conversations. | A cross-meeting task list alone is not a differentiator; evaluate evidence-backed updates from subsequent speech. |
| [Granola](https://docs.granola.ai/help-center/getting-more-from-your-notes/chatting-with-your-meetings) | Supports questions across meeting notes, action items, and follow-ups. | Historical meeting chat alone is not a differentiator; focus on explicit task state and corrections. |
| [Zoom AI Companion](https://news.zoom.com/zoom-agentic-ai/) | Describes task action, memory, and meeting action-item capture. | Broad claims that existing assistants stop at summaries are not defensible. |
| [Google Meet notes](https://support.google.com/meet/answer/14754931?hl=en) | Produces meeting notes, summaries, and suggested next steps. | Test longitudinal reconciliation directly rather than inferring limitations from a notes feature description. |

Our proposed distinction is a transparent, evaluated research-team workflow for matching later statements to prior commitments, resolving uncertainty, and inspecting task-change evidence. Product documentation does not establish which competitors support every detail of this workflow. A small hands-on comparison remains planned; we will not claim that no existing product tracks actions across meetings.

## 8. Data, Licensing, and Responsible Use

**Collection and consent:** Use our own consenting team or study-group meetings and purpose-recorded scenarios. For this project, require every participant's explicit agreement before recording and before processing uploaded audio, including disclosure of any external model provider. Offer a non-recorded alternative and deletion requests without penalty. This is our product policy, not a statement of jurisdiction-specific legal sufficiency; confirm institutional requirements before collecting research-group data.

**Privacy:** Exclude student evaluations, health discussions, unpublished sensitive research, employer information, and other confidential material from development recordings. Give users a chance to exclude segments before external LLM processing. Automatic sensitive-content detection is assistive and cannot guarantee detection. Keep real recordings, transcripts, embeddings, and consent records outside Git and public demonstrations. Use fictional names and purpose-recorded examples for distributable artifacts.

**Storage and deletion:** Default to local use on encrypted storage with restricted access. Proposed retention is raw audio for 30 days and retained transcripts/tasks until the participant requests deletion or the project ends, subject to participant agreement. Deletion removes associated indexes and cached outputs; unsupported surviving tasks are flagged for review. Do not retain deleted sensitive text merely to preserve an audit trail. Document provider retention and backup limitations before any upload to an external service.

**Access:** Keep the first release single-user and local. Shared access is deferred until authorization is implemented. Within that release, all retrieval and task matching must enforce project boundaries. Summary sharing is an explicit user action.

**Licensing:** Before using the sponsor's code, public datasets, model weights, or libraries, record the exact source, version, license or terms, access requirements, and redistribution permissions. Public availability alone does not imply permission to redistribute. Keep third-party assets separate from the repository's own license, and publish dataset references or preparation instructions when redistribution is not permitted.

**Reliability and misuse:** Show uncertainty, source evidence, and corrections. Do not treat inferred task status as verified real-world performance or use the tool for student ranking. Test overlapping speech, accents, jargon, and pronoun ambiguity; report coverage limits. Generated plans remain suggestions. Model outputs cannot send messages, delete source material, or alter external calendars without a user-directed workflow.

## 9. Team, Timeline, and Budget

### Proposed ownership

| Member | Primary responsibility | First implementation checkpoint |
|---|---|---|
| Will Liu | Data contracts, extraction, and reconciliation | Task schema, source references, update rules, and ambiguous-match handling |
| Bryan Yang | Application, storage, and pipeline integration | Transcript-to-task vertical slice with editable tasks and timestamp navigation |
| Guadalupe Cantera | Evaluation, data preparation, and quality | Consent/data protocol, sequence fixtures, annotation guide, and pilot metrics |

All members review the proposal, consent practices, evaluation claims, and final demo. These assignments adapt the previous team's roles and need team confirmation.

### Relative course timeline

| Period | Deliverable |
|---|---|
| Weeks 1-2 / Milestone 1 | Proposal, scope, preliminary product review, team roles, and rubric verification; confirm sponsor-code access and data permissions before collection |
| Weeks 3-5 / first implementation checkpoint | Consented sample sequence, transcript import, task extraction, persistence, editable UI, and initial audio integration |
| Weeks 6-8 | Cross-meeting reconciliation, review/undo, person/project views, and citation-based search |
| Weeks 9-10 | Suggested deadline plans, meeting brief, privacy/deletion checks, and validation pilot; freeze evaluation protocol |
| Weeks 11-12 | Held-out evaluation, baseline comparison, failure analysis, and reliability fixes |
| Weeks 13-14 | Reproduce clean setup, finalize results and limitations, and prepare report and demonstration |

Week numbers describe proposed project phases, not verified course dates. Confirm the official milestone schedule before assigning calendar deadlines.

### Planning budget

Assume existing team laptops, no required hardware purchase, and local deployment. Propose a **$150 total project spending cap**: up to $100 for model/transcription usage, $30 for optional compute or demo hosting, and $20 contingency. These are allocations, not vendor price quotes or approved spending. No paid resource has been provisioned.

Run a small pilot first, measure cost per audio hour and per reconciliation/question run, and calculate the affordable evaluation volume including retries and repeated runs. Start with the proposed 18 short recordings and at most three repeated model runs per evaluation condition where affordable. Cache unchanged transcripts and reduce secondary experiments before reducing the core held-out comparison. Record actual charges separately from estimated local compute cost.

## 10. Risks and Mitigations

| Risk | Response |
|---|---|
| Incorrect speaker assignment gives a task to the wrong person | Confirm speaker mappings, preserve unknown identities, and evaluate owner attribution separately. |
| Similar tasks are incorrectly merged or completed | Require project/owner/evidence consistency; review ambiguity and prioritize update precision. |
| Silence or partial progress is mistaken for completion | Require explicit supported state changes; include negative and partial-completion fixtures. |
| Summaries or cleanup invent meaning | Preserve raw segments, attach evidence, and manually score faithfulness. |
| Too little longitudinal data | Purpose-record linked scenarios and clearly separate controlled results from natural-meeting results. |
| Audio integration delays the central contribution | Start with timestamped transcript imports while maintaining an audio-to-task final demo requirement. |
| The proposal duplicates existing products | Compare documented capabilities honestly and emphasize measurable reconciliation behavior. |
| Scope exceeds the available term | Prioritize the three-meeting task lifecycle; defer external integrations, slides, and native capture. |

## 11. Milestone 1 Readiness and Requested Feedback

### Draft completed

- [x] Two-paragraph explanation and motivation
- [x] Defined terms, user story, scope, and architecture
- [x] Measurable AI outputs, baselines, annotation plan, and provisional targets
- [x] Preliminary related work and sourced product positioning
- [x] Data, consent, licensing, ethics, and deletion plan
- [x] Proposed ownership, timeline, budget, and risks

### Before submission

- [ ] Verify official Canvas rubric, required length, deadline, and submission format.
- [ ] Confirm team roles and review the new direction with teaching staff.
- [ ] Confirm access and permitted reuse of the sponsor's code, or commit to the independent pipeline.
- [ ] Confirm recording participants and institutional data requirements before collection.
- [ ] Create any pitch deck and combined PDF required by the official rubric.

Requested teaching-staff feedback: Is longitudinal commitment reconciliation an appropriate central contribution? Is the proposed small sequence dataset sufficient for the intended claims? Should backward planning remain required or become a stretch goal? Is transcript-first development acceptable provided the final demo includes audio ingestion?
