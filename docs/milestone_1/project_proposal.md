# Milestone 1 Project Proposal

**Course:** CIS-5980

**Track:** AI Engineering

**Team:** Will Liu, Guadalupe Cantera, and Bryan Yang

**Repository:** [github.com/BryanDYang/ai-capstone](https://github.com/BryanDYang/ai-capstone)

**Status:** Milestone 1 proposal incorporating team submission-draft input

**Updated:** September 12, 2026

## 1. Project Explanation and Motivation

Weekly research meetings produce commitments, professor suggestions, decisions, deadlines, and follow-up questions that are difficult to maintain across weeks. Researchers may report progress on something assigned several meetings earlier, refer to an old task using shorthand, change a deadline, or decide not to pursue a previous suggestion. Traditional meeting summaries can capture what happened in one meeting, but the user still has to connect those updates to earlier conversations and determine what is still open, what changed, and why. This matters in recurring research meetings because losing that context can lead to duplicated work, forgotten commitments, unclear ownership, and decisions whose original reasoning becomes difficult to recover. Our sponsor, CCB, already has a pipeline that records, transcribes, identifies speakers, cleans transcripts, and generates meeting summaries, so our project focuses on the follow-through problem rather than rebuilding the existing transcription pipeline.

We propose **\[PROJECT NAME\]**, a local-first meeting continuity system for research advisors and their teams. After a meeting is processed, the system extracts evidence-backed decisions, owned commitments, deadlines, and professor suggestions and stores them as structured project memory. When later meetings occur, it reconciles new statements with that existing state so that, for example, a completed task is updated instead of recreated, a changed deadline modifies the correct task, and a professor's suggestion remains separate until a researcher actually accepts it. Ambiguous matches are routed for human review rather than silently changing the record. Between meetings, the system automatically follows up with task owners through a user-enabled delivery channel on a configured schedule, adjusting reminders as commitments change. Users can inspect and correct the resulting history, generate a pre-meeting view of outstanding items, and ask historical questions that return supporting meeting and timestamp evidence. Our central AI-engineering question is whether this persistent, evidence-backed approach can maintain commitments across a sequence of meetings more reliably than treating every meeting independently, while reducing manual reconciliation and avoiding unsupported task updates.

**Engineering question:** Can an assistant reliably maintain commitments across a sequence of meetings while reducing manual reconciliation and avoiding unsupported task updates?

## 2. Project Charter

### Problem Statement

Recurring research meetings generate commitments, suggestions, decisions, and deadlines whose status changes over time. Existing meeting notes and summaries may capture individual meetings but still leave users responsible for connecting later updates to earlier commitments. Our project focuses on maintaining this longitudinal state accurately and with evidence.

### Target Users and Context

Our primary users are PhD advisors and the researchers or students who meet with them regularly. The intended setting is a recurring research-group meeting where participants need to remember what was decided, who committed to what, what remains unresolved, and how those items changed across meetings. Our own consenting project team or study groups will serve as a secondary development and evaluation setting.

### Value Proposition

The system turns a sequence of disconnected meeting artifacts into an evidence-backed project memory. Instead of requiring users to manually compare summaries from different weeks, it maintains the current state of commitments, decisions, deadlines, and suggestions while preserving where each item came from and how it changed.

The value of the system is reducing the manual work required to reconstruct what happened across previous meetings while keeping the underlying evidence available for verification. Success from the user's perspective means being able to open the system before or after a meeting and quickly understand what is still open, what was completed, blocked, dropped, or changed, who owns each commitment, which professor suggestions were actually accepted, what decisions were made and why, and what meeting evidence supports that information.

### End Deliverable

By the end of the capstone, we aim to deliver a reproducible local application consisting of a Python background service and CLI that imports timestamped meeting artifacts, associates them with project and calendar context, extracts structured decisions and commitments, reconciles later statements with persistent state, presents ambiguous cases for review, supports corrections and deletion, generates meeting and pre-meeting views, automatically sends scheduled follow-ups on outstanding commitments, and answers historical questions with source citations.

The final deliverable will also include a reproducible evaluation harness, labeled meeting sequences, baseline comparisons, measured results, setup documentation, and a live demonstration of the three-meeting task lifecycle.

## 3. Users and Example Workflow

The primary users are a PhD advisor and the researchers or students who meet with them weekly. A secondary development setting is our own consenting project team or study group.

1. Participants agree to recording, processing, and retention before the configured pipeline processes meeting artifacts.
2. After a weekly research sync, \[TBD\] detects a new artifact in a configured local folder and matches it to the project, calendar event, attendees, date, and timezone. Uncertain matches require review.
3. The upstream pipeline supplies a timestamped transcript. Users can confirm speaker names and correct recognition or extraction errors.
4. \[TBD\] records the decision to standardize on ViT-B/16, Will's commitment to rerun the baseline by Friday, and the advisor's commitment to send two papers. A recommendation to try mixed precision stays on a separate suggestion list until accepted.
5. At the next meeting, “The rerun finished early on the cluster” updates the matching task to done when the owner, project, and evidence support the match. The original commitment and new evidence remain linked.
6. The advisor's unsent papers remain open and roll into the next meeting brief. A stated new deadline updates the existing record; silence never marks an item done or dropped.
7. The CLI exposes runtime status, configuration, meeting history, evidence, and review controls. Proposed commands include labsync status, labsync config, labsync history, and labsync inspect \<meeting-id\>.
8. A question such as “What did we decide about the baseline last month, and why?” returns a dated decision, rationale, speaker attribution, and timestamp citation, or states that the available evidence is insufficient.

Calendar integration and automatic follow-up are required MVP capabilities. Once a user configures recipients, a delivery channel, and a schedule, the service sends reminders or status requests for outstanding commitments without requiring another meeting or a separate approval for each scheduled message. For example, Will receives a reminder before the baseline deadline; marking the task done cancels pending reminders. The MVP will support at least one delivery channel, selected during the integration checkpoint. Additional channels, native reminder synchronization, and broader calendar writes are stretch goals.

## 4. Terms and Observable Outputs

| **Term**         | **Definition and output**                                                                                                                                                                         |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Transcription          | Converts speech into timestamped text; it does not establish speaker identity.                                                                                                                          |
| Transcript cleanup     | Edits recognition errors, punctuation, and filler without changing meaning; it produces a separate cleaned version linked to the original segments.                                                     |
| Diarization            | Separates stretches of audio by voice; it produces speaker labels, not names.                                                                                                                           |
| Speaker identification | Maps speaker labels to attendee names with user confirmation; an attendee list alone does not establish who spoke.                                                                                      |
| Action item            | A named person's commitment to a specific task, with an optional due date, status, and source timestamp; an unowned suggestion remains a candidate for clarification.                                   |
| Suggestion             | A professor recommendation tracked with its source and intended researcher when explicit; it stays separate from commitments until accepted.                                                            |
| Decision               | A statement settling a question, stored with its source; a later reversal is a linked new decision rather than an overwrite.                                                                            |
| Reconciliation         | Matches a later statement to an existing commitment and proposes or records an evidenced change; similar wording alone is insufficient.                                                                 |
| Automatic follow-up    | Scheduled reminders or status requests sent to the configured owner of an outstanding commitment, with a task/evidence reference and a delivery record. Sending a reminder does not change task status. |
| Summary                | A concise account of discussion, decisions, and commitments evaluated for faithfulness, coverage, and usefulness.                                                                                       |
| Suggested plan         | Proposed steps working backward from a confirmed deadline; its invented intermediate dates are not meeting commitments.                                                                                 |
| Consent                | Recorded agreement by every participant to the stated recording and processing policy before audio processing; an upload alone is not evidence of everyone's agreement.                                 |

## 5. Scope and Deliverable

### Required MVP

- Run a local background service that watches a configured meeting-artifact folder, with a CLI for configuration, status, history, inspection, correction, and review.
- Integrate calendar context to associate meetings with projects, attendees, dates, and timezones.
- Import timestamped transcripts from the sponsor pipeline or manual imports and allow users to confirm or correct speaker mappings.
- Generate structured decisions, commitments, professor suggestions, and a concise meeting summary with source references.
- Maintain open, in-progress, blocked, done, and dropped tasks across meeting sequences.
- Track owner and deadline changes while preserving the original commitment and evidence.
- Keep professor suggestions separate from commitments until there is evidence that a researcher accepted them.
- Present ambiguous matches for human review.
- Support correction, undo, and change history.
- Provide inspection by meeting, person, and project.
- Generate a pre-meeting brief containing outstanding commitments and suggestions.
- Automatically send follow-ups for outstanding commitments through at least one user-enabled delivery channel. Support configurable recipients and schedules, pause/disable controls, delivery history, and duplicate prevention. Cancel or reschedule pending reminders after completion, dropping, reassignment, deadline changes, or source deletion.
- Answer historical questions using retrieved evidence with transcript timestamps and audio references when retained audio is available.
- Demonstrate consent gating, selective exclusion, deletion, and project-scoped retrieval.
- Deliver reproducible evaluation fixtures, measured results, and setup documentation.

### Stretch goals

Sophisticated diarization, voice-profile enrollment, backward planning, dedicated Zoom/iPhone capture, slide-aware summaries, additional follow-up delivery channels, native reminder synchronization, and broader calendar writes. Reuse the sponsor capture pipeline where permitted; implementing a new speech pipeline is secondary to the persistent-state workflow. Manual speaker confirmation is sufficient for the MVP.

### Explicitly Out of Scope

The project will not:

- Train a speech-recognition model from scratch.
- Fine-tune or pre-train a large language model as part of the required MVP.
- Generate productivity or performance scores.
- Rank students or researchers.
- Monitor meetings without participant consent.
- Deploy a production multi-tenant service.
- Treat meeting statements as independently verified proof that real-world work occurred.
- Claim broad performance across languages or meeting settings beyond those evaluated.

### Optional Focus Areas for AI Engineering

The following AI Engineering focus areas best represent the technical work planned for the project.

**Data**

- Build a small dataset from labeled examples we curate through annotated development and held-out meeting sequences.
- Collect new data under appropriate permissions and privacy practices using purpose-recorded, consenting team meetings or study groups.
- Use an existing public dataset such as QMSum as a supplementary benchmark only if its terms permit our intended use. It will not replace our longitudinal task-state annotations.

**Model and system**

- **Prompt engineering:** Schema-enforced structured extraction of decisions, commitments, suggestions, and evidence.
- **Retrieval-Augmented Generation:** Decision-ledger plus lexical/dense retrieval for historical Q&A.
- **Tool use/orchestration:** Coordinate transcript ingestion, structured extraction, persistent-state retrieval, reconciliation, evidence validation, and historical retrieval as separate stages of the application pipeline.

**Application and deployment**

- Command-line interface.
- Local-first, single-user deployment.

**Evaluation and responsible AI**

- Custom evaluation suite beyond the baseline harness.
- Robustness testing for ambiguous references, negation, partial completion, uncertain speakers, and related edge cases.
- Safety and hallucination checks, including attribution hallucination and unsupported claims.
- Latency, token usage, and cost profiling.

Bias analysis is not currently selected as a primary evaluation focus because the pilot-scale, purpose-recorded dataset is not large or diverse enough to support meaningful demographic bias claims. We will revisit this if the evaluation dataset grows substantially.

## 6. Architecture and AI Engineering

```text
Configured artifact folder + calendar context + consent record
|
Detect meeting -> consent gate -> project association
|
Sponsor transcript pipeline or timestamped import
|
Speaker confirmation + original/cleaned segments
|
Extract decisions, commitments, and professor suggestions
|
Retrieve project state -> match later mentions
|
Route: new / existing / suggestion / ambiguous
|
Validate evidence -> apply or request human review
|
Persistent project history
|
+-> CLI inspection + next-meeting brief
|
+-> Automatic follow-up scheduler (runs between meetings)
    |
    Check outstanding commitments + deadlines + user settings
    |
    Send reminders/status requests through a user-enabled channel
    |
    Record delivery + prevent duplicate reminders
    |
    Cancel or reschedule when task state changes

Historical question -> decision ledger + hybrid retrieval -> cited answer
```

The follow-up scheduler reads validated project state and runs independently of transcript ingestion while the local service is running. It checks the current owner, status, deadline, evidence availability, and user settings immediately before sending. Unresolved candidates and unaccepted suggestions do not trigger commitment reminders. Users can pause or disable follow-up; missing deadlines use an explicitly configured cadence rather than an invented due date. Delivery records persist across restarts, failed deliveries remain visible with bounded retries, and uncertain delivery outcomes require review before resending. Completion, dropping, corrections, and deletion invalidate affected pending reminders. The local MVP does not promise delivery while the device is asleep or the service is stopped.

The AI work comprises structured extraction, semantic task matching, evidence-grounded summarization, and retrieval-augmented answers. Application code validates schemas, source references, project boundaries, and permitted state transitions. Transcript content is untrusted data and cannot authorize tool execution or change system instructions.

Each task has a stable ID, project ID, owner ID, description, nullable due date, status, and original source segment. Each update records the task ID, previous and new values, evidence segment, meeting date, processing time, and whether a user or model proposed and accepted it. Suggestions and unresolved candidates are kept separately from accepted tasks. Accepted suggestions link to the resulting task without losing their original source. An update cannot reference a nonexistent segment or silently move a task into another project.

Processing is idempotent: re-uploading or retrying a meeting must not duplicate accepted tasks. Meetings are reconciled in event order; importing older meetings must not silently overwrite newer task state. Speaker and transcript corrections invalidate dependent outputs for review or recomputation. Search indexes and cached outputs follow source deletions.

### Preliminary implementation choices

| **Layer**   | **Proposed choice and purpose**                                                                                                   |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| Interface         | CLI for runtime control, meeting inspection, task correction, and ambiguity review                                                      |
| Service           | Python background worker with schema validation for ingestion, extraction, and task operations                                          |
| Speech            | Inspect the sponsor's existing pipeline first; use Whisper and pyannote.audio if reuse is unavailable or unsuitable                     |
| Persistence       | SQLite for the local MVP, local private audio storage, and timestamped transcript segments                                              |
| Retrieval         | SQLite decision ledger plus project-filtered lexical and dense retrieval over speaker-attributed turns; retain source IDs               |
| Model integration | One configured LLM behind a small adapter, with structured outputs and bounded retries; exact model selected after a quality/cost pilot |
| Verification      | Pytest for extraction/state behavior and end-to-end CLI checks for detection, calendar matching, review, correction, and citations      |
| Observability     | Record model/prompt versions, usage, processing failures, stage latency, and cost per hour of audio                                     |

No sponsor code is assumed available or licensed until inspected. Transcript imports allow development of the core follow-through workflow while audio integration proceeds. Prompt caching is an optional measured optimization after correctness is established.

## 7. Evaluation Plan

### Data and experimental design

Begin with a pilot of 6-8 short meetings using consenting team meetings and purpose-recorded scenarios. The expanded evaluation target is 18 meetings arranged into six independent three-meeting project sequences, split into three development, one validation, and two held-out test sequences. If only the pilot is feasible, report the actual sequence counts and a reduced evaluation design rather than claiming the full six-sequence split. Keep scenario variants and overlapping source material together to prevent leakage. These are pilot-scale targets, not a claim of statistical representativeness. Report counts and uncertainty, and expand the held-out set if feasible.

Use QMSum as a supplementary retrieval and summarization benchmark after checking its terms; it does not replace longitudinal task-state annotations.

Two team members independently annotate the held-out commitments, owners, deadlines, decisions, links between meetings, and state changes, then resolve disagreements before scoring. Include professor suggestions and their later acceptance or dismissal, completion, blocked work, partial completion, reassignment, changed deadlines, dropped tasks, duplicate mentions, similar tasks in different projects, uncertain speakers, negation, and tasks never mentioned again. Include answerable and unanswerable historical questions. Freeze prompts and thresholds before held-out evaluation.

Compare two conditions using the same transcripts, model, and extraction settings:

1. **Independent meeting extraction:** Produce each meeting's summary and task list without reconciling earlier tasks.
2. **Persistent reconciliation:** Use the same extraction plus existing task state and source-backed updates.

Score both against the expected current task list after each meeting, counting duplicates, stale open items, unsupported changes, and missing tasks. Separately compare a simple lexical task matcher with semantic reconciliation to test the value of the matching component. Evaluate on corrected transcripts and raw pipeline outputs to distinguish reasoning failures from speech and speaker errors.

### Component comparisons

Use the same input splits and configured model for each paired comparison. Report measured differences rather than assuming baseline weaknesses or performance gains.

| **Component** | **Baseline**                              | **Proposed pipeline and measurements**                                                                                                              |
| :------------------ | :---------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Extraction          | Unconstrained zero-shot extraction              | Schema-enforced records with confirmed speaker mapping; task F1, owner accuracy, and decision precision                                                   |
| Reconciliation      | Keyword/Jaccard matching                        | Contextual matching against persistent project state; linkage F1, state-transition accuracy, and false duplicate rate                                     |
| Summaries           | Single-pass summary                             | Generate, critique, and revise against a fixed rubric; blind human ratings of faithfulness, attribution, conciseness, actionability, and coverage         |
| Historical Q&A      | Dense-only retrieval over 500-token text chunks | Decision ledger plus lexical/dense retrieval over timestamped turns; faithfulness, context precision/recall, citation accuracy, and audio timestamp error |

Additional development targets from the Word draft are extraction F1 \>= 0.88, owner attribution \>= 95%, linkage F1 \>= 0.85, false duplicate rate \<= 5%, answer faithfulness \>= 0.95, context precision \>= 0.90, and audio anchor error \<= 10 seconds where source audio exists. These are experimental targets, not observed results or guarantees. Multi-month retrieval claims require an archive covering that period; the three-meeting demo alone cannot validate them.

### Metrics and provisional success criteria

These are proposed acceptance targets, not measured results. Calibrate them on development and validation data before freezing the test protocol.

| **Output**      | **Measurement**                                                                                                                                                                                                                      | **Proposed target**                                                                                                      |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| Extracted commitments | Precision and recall against adjudicated tasks; a match requires the correct owner and equivalent commitment                                                                                                                               | Precision\>= 90%, recall \>= 80%                                                                                               |
| Cross-meeting updates | Correct task link and requested field/status change among automatic updates                                                                                                                                                                | Precision\>= 95%; also report recall and automatic-update coverage                                                             |
| Current task list     | Correct owner, description, status, and supported due date after each meeting                                                                                                                                                              | Higher state accuracy than independent extraction; report absolute difference and raw counts                                   |
| False completion      | Unsupported done transitions divided by all automatic done transitions                                                                                                                                                                     | Zero observed in the held-out demo set, with sample size reported                                                              |
| Human review burden   | Fraction of candidate updates requiring review and review time                                                                                                                                                                             | Report alongside accuracy; no success claim from routing everything to review                                                  |
| Historical answers    | Correct answer and citations that support each substantive claim                                                                                                                                                                           | \>= 90% supported-answer rate; separately score abstention on unanswerable questions                                           |
| Summaries             | Human rubric for faithfulness, attribution, conciseness, actionability, and coverage                                                                                                                                                       | Mean\>= 4.6/5 overall; faithfulness 5/5, with no unsupported claims in the final demo                                          |
| Audio and speakers    | Word error rate on selected hand-transcribed segments; diarization error and owner-attribution accuracy                                                                                                                                    | Report by recording condition; diagnose impact on downstream task errors                                                       |
| Plans (stretch only)  | Confirmed final deadline respected; suggested dates labeled; no unaccepted step becomes a commitment                                                                                                                                       | All deterministic checks pass                                                                                                  |
| Automatic follow-up   | Controlled-clock tests with a fake delivery channel: correct recipient and schedule, no duplicate sends after restart, deadline/owner changes, cancellation after completion or deletion, disabled settings, and visible delivery failures | All deterministic checks pass; demonstrate one end-to-end delivery through the selected channel to a consenting test recipient |
| System behavior       | Folder detection, calendar matching, duplicate ingestion, correction, deletion, consent gating, project isolation, citation navigation                                                                                                     | All required end-to-end scenarios pass                                                                                         |
| Efficiency            | End-to-end and stage latency, tokens, cost per audio hour, and manual reconciliation time                                                                                                                                                  | Report hardware/model and median/range; set operational budget after pilot                                                     |

Summary rubric anchors: **1** = materially incorrect or unusable, **3** = mostly correct but requires substantive editing, **5** = faithful and immediately useful. Scores 2 and 4 represent intermediate quality. Reviewers score dimensions separately. An LLM judge may assist error triage but will not replace human ground truth for ownership, dates, completion, or citation support.

### Minimum end-to-end demonstration

The final demonstration will run a three-meeting sequence in which:

- Meeting 1 creates two owned tasks, a decision, and a professor suggestion.
- Meeting 2 completes one existing task, changes another task's deadline, and introduces blocked work.
- Meeting 3 leaves the remaining task open and includes an ambiguous reference requiring human review.

The demonstration will also include a scheduled follow-up to a consenting test recipient between meetings, rescheduling after a deadline change, cancellation after completion, and a retry/restart check for duplicate prevention. It will include a cited historical question, user correction, folder detection, calendar association, CLI inspection, duplicate-ingestion protection, and deletion of a meeting with removal of its associated searchable content.

## 8. Related Work and Product Positioning

The following references inform component selection and evaluation; they are not evidence that the complete proposed workflow already works.

| **Source**                                                        | **Relevance and boundary**                                                                                                                |
| :---------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| [<u>Whisper, Radford et al., 2022</u>](https://arxiv.org/abs/2212.04356) | Speech recognition foundation; assess our recordings rather than assuming accurate domain terminology or speaker attribution.                   |
| [<u>pyannote.audio</u>](https://github.com/pyannote/pyannote-audio)      | Speaker diarization tools; named attendee mapping remains a separate step.                                                                      |
| [<u>QMSum, Zhong et al., 2021</u>](https://arxiv.org/abs/2104.05938)     | Query-based meeting summarization benchmark for retrieval and summary experiments; does not establish our longitudinal task-state ground truth. |
| [<u>MeetingBank, Hu et al., 2023</u>](https://arxiv.org/abs/2305.17529)  | Public meeting summarization benchmark; municipal meetings differ from recurring advisor/student meetings.                                      |
| [<u>AMI Meeting Corpus</u>](https://groups.inf.ed.ac.uk/ami/corpus/)     | Candidate meeting audio and annotation source; inspect available annotations and permitted use before selecting a subset.                       |

Preliminary product review, checked September 8, 2026:

| **Product**                                                                                             | **Documented strength**                                          | **Implication for this proposal**                                                                           |
| :------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| [<u>Otter</u>](https://help.otter.ai/hc/en-us/articles/25983095114519-Action-Items-Overview)                   | Consolidates assigned action items across conversations.               | A cross-meeting task list alone is not a differentiator; evaluate evidence-backed updates from subsequent speech. |
| [<u>Granola</u>](https://docs.granola.ai/help-center/getting-more-from-your-notes/chatting-with-your-meetings) | Supports questions across meeting notes, action items, and follow-ups. | Historical meeting chat alone is not a differentiator; focus on explicit task state and corrections.              |
| [<u>Zoom AI Companion</u>](https://news.zoom.com/zoom-agentic-ai/)                                             | Describes task action, memory, and meeting action-item capture.        | Broad claims that existing assistants stop at summaries are not defensible.                                       |
| [<u>Google Meet notes</u>](https://support.google.com/meet/answer/14754931?hl=en)                              | Produces meeting notes, summaries, and suggested next steps.           | Test longitudinal reconciliation directly rather than inferring limitations from a notes feature description.     |

Our proposed distinction is a transparent, evaluated research-team workflow for matching later statements to prior commitments, resolving uncertainty, and inspecting task-change evidence. Product documentation does not establish which competitors support every detail of this workflow. A small hands-on comparison remains planned; we will not claim that no existing product tracks actions across meetings.

## 9. Data, Licensing, and Responsible Use

**Data Sources and Evaluation:** For development and evaluation, we will mainly use purpose-recorded scenarios and meetings from our own team or study groups where everyone has agreed to participate. These meetings will be designed to include the kinds of situations our system needs to handle, such as commitments, professor suggestions, decisions, task updates, blockers, changed deadlines, and ambiguous references to things discussed in previous meetings. We will not assume that real research lab meetings, sponsor recordings, or existing meeting archives are available for us to use. If we later use real research meetings, we will first confirm that we have participant consent and permission to process that data. We will also keep controlled/test scenarios separate from natural meetings when reporting our evaluation results.

**Consent and Participant Control:** Everyone in a meeting must agree to the recording and processing policy before their audio is processed. Participants should know what is being collected, what information the system will keep, whether any meeting content is being sent to an external AI provider, how long the data will be retained, and how they can request deletion. Consent requirements are not the same everywhere: some states require every participant's consent to record a conversation, while others only require one person's, so we will record which policy applies to a given meeting rather than assuming the least restrictive rule. Simply uploading a recording does not mean that everyone in that recording consented. Participants should also have a non-recorded option and be able to request that a meeting, or specific parts of a meeting where possible, are excluded from AI processing. Before using real research-group data, we will confirm any additional institutional requirements that apply.

**Privacy and Data Minimization:** Research meetings can include information that should not become part of a long-term AI memory, such as unpublished research (including patent-pending architectures), personnel discussions, credentials, grant information, or other confidential material. Our goal is therefore to store only what the system actually needs for its longitudinal-memory functions. Persistent memory should focus on supported decisions, commitments, task updates, professor suggestions, and the evidence needed to verify them rather than saving unrelated conversation indefinitely. For development and evaluation, we will avoid intentionally including sensitive information that is not necessary for testing the system. Real recordings, transcripts, embeddings, speaker mappings, and extracted project data will not be committed to Git or included in public demos.

**Storage, Retention, and Deletion:** The MVP will be local-first and single-user, with meeting data stored on access-controlled, encrypted local storage. We also recognize that deleting the original audio is not enough. A meeting can create a transcript, embeddings, search indexes, summaries, tasks, decisions, speaker mappings, and other derived data. If a meeting or portion of a meeting is deleted, the system should also remove the related searchable and cached artifacts. Rather than permanently erasing the source audio the moment deletion is requested, we will route it through the OS's native trash first, so it stays recoverable for a short window in case the deletion was accidental or a dispute requires the original evidence, before it is purged for good. If deleted evidence was the only support for an existing task or decision, that record should be flagged for review rather than continuing to appear as verified information. Retention periods will be decided and clearly communicated before we begin collecting evaluation data.

**Evidence, Attribution, and Human Review:** Because this system creates a memory that carries information across meetings, we do not want one incorrect AI inference to become a permanent part of that history. The system should preserve evidence for the tasks, decisions, and state changes it creates. A professor saying, "someone should try this" should not automatically become a commitment assigned to a student, and misattributing a task or decision to the wrong speaker is a failure mode we are treating as its own testable category (attribution hallucination) rather than assuming schema-enforced extraction rules it out. Similarly, silence about a task in the next meeting should not mean it was completed or abandoned, and partial progress should not automatically mean completion. When ownership, task matching, or state changes are ambiguous, the system should flag the item for human review instead of making the decision on its own. Users should also be able to correct speaker mappings, extracted records, and reconciliation decisions if the system gets something wrong.

**Grounded Summaries and Historical Q&A:** Summaries and historical answers should be grounded in actual meeting evidence rather than the model filling in missing information. Important claims should point back to the relevant meeting and transcript timestamp, with an audio reference when the original audio is still available. If the system does not have enough evidence to answer a question, it should say that rather than make its best guess. For example, discussing an experiment is not the same thing as explicitly committing to complete it. Our evaluation will include both answerable and intentionally unanswerable questions so we can test whether the system retrieves the right evidence and knows when it should not make a claim.

**Project Isolation and External Actions:** Information from one research project should not accidentally appear in another project's results. Retrieval and reconciliation will therefore be scoped to the selected project. We will also treat transcript content as untrusted input; something said during a meeting cannot override system instructions or authorize the system to take an external action. The model will not independently send messages, delete recordings, modify calendars, or take similar actions. Features such as reminders, calendar updates, or summary sharing will only happen through workflows that the user has explicitly enabled.

**External AI Services, Licensing, and Third-Party Data:** Before sending meeting content to an external AI or API provider, we will document what data leaves the local system, why it needs to be sent, and the provider's relevant retention and data-use policies. Participants should know when their meeting content may be processed externally, and we will avoid sending excluded or unnecessary portions of a meeting where possible. We will also document the source, version, license, access restrictions, and redistribution permissions for any sponsor code, public datasets, pretrained models, libraries, or other third-party assets we use. Something being publicly available does not automatically mean we have permission to redistribute it. Sponsor code will only be incorporated after we confirm that we are allowed to use it.

**Responsible Use and Non-Goals:** \[TBD\] is meant to help research teams remember and follow up on what was discussed across meetings. It is not meant to evaluate the people in those meetings. The system will not create productivity or performance scores, rank students or researchers, use speaking frequency or number of assigned tasks as a measure of contribution, infer sensitive personal characteristics, or monitor meetings without participant consent. It also will not treat something reported during a meeting as independent proof that the work happened in the real world. The system's job is to accurately represent and connect what was said in the meetings, while keeping the original evidence available for verification. Known limitations, including overlapping speech, technical jargon, uncertain speakers, and ambiguous references, will be evaluated and reported rather than hidden.

## 10. Team, Timeline, and Budget

### Proposed ownership

| **Member**  | **Primary responsibility**                | **First implementation checkpoint**                                       |
| :---------------- | :---------------------------------------------- | :------------------------------------------------------------------------------ |
| Will Liu          | Data contracts, extraction, and reconciliation  | Task schema, source references, update rules, and ambiguous-match handling      |
| Bryan Yang        | Runtime, CLI, storage, and pipeline integration | Transcript-to-task vertical slice with CLI corrections and timestamp inspection |
| Guadalupe Cantera | Evaluation, data preparation, and quality       | Consent/data protocol, sequence fixtures, annotation guide, and pilot metrics   |

All members review the proposal, consent practices, evaluation claims, and final demo. These proposed assignments need team confirmation.

### Relative course timeline

| **Period**                            | **Deliverable**                                                                                                                                |
| :------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| Weeks 1-2 / Milestone 1                     | Proposal, scope, preliminary product review, team roles, and rubric verification; confirm sponsor-code access and data permissions before collection |
| Weeks 3-5 / first implementation checkpoint | Consented sample sequence, transcript import, task extraction, persistence, CLI controls, folder watching, and calendar context                      |
| Weeks 6-8                                   | Cross-meeting reconciliation, review/undo, person/project inspection, and citation-based search                                                      |
| Weeks 9-10                                  | Automatic follow-up delivery, suggestion tracking, meeting brief, privacy/deletion checks, and validation pilot; freeze evaluation protocol          |
| Weeks 11-12                                 | Held-out evaluation, baseline comparison, failure analysis, and reliability fixes                                                                    |
| Weeks 13-14                                 | Reproduce clean setup, finalize results and limitations, and prepare report and demonstration                                                        |

Week numbers describe proposed project phases, not verified course dates. Confirm the official milestone schedule before assigning calendar deadlines.

## 11. Draft evaluation-harness checkpoint for Milestone 2

By the next milestone, aim to run a small, reproducible evaluation from timestamped transcripts to a saved score report. This checkpoint establishes the evaluation machinery; it does not require the full audio pipeline or demonstrate final model quality.

| Proposed owner    | Deliverable                                                                         | Completion check                                                                                                                                                                                                                                                                          |
| ----------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Guadalupe Cantera | One synthetic three-meeting development sequence and a short annotation guide       | Expected commitments, owners, source segments, and task states are labeled after each meeting and reviewed by a second team member. Include completion, a changed deadline, an unaccepted suggestion, an ambiguous reference, and a task that is not mentioned again.                     |
| Will Liu          | Transcript/task output contract and initial independent-meeting extraction baseline | Baseline outputs use the agreed schema and retain source IDs. Record the model, prompt version, and run settings. Define how semantically equivalent commitments are matched to annotations, with human adjudication where needed.                                                        |
| Bryan Yang        | Evaluation runner and offline scorer tests                                          | One documented command loads fixtures and saved predictions and produces a report. A correct prediction fixture receives the expected score; deliberately wrong owners, duplicate tasks, unsupported completion, and invalid citations are detected. CI exercises this without API calls. |

The first report should include task precision/recall, owner accuracy, duplicate counts, unsupported completion counts, and source-reference validity, with numerators and denominators. Once reconciliation is runnable, score the expected task state after each meeting and compare it with the independent-meeting baseline on the same sequence. Keep this sequence in development only; it must not become held-out evidence. Live model runs are separate from deterministic CI tests and record usage and latency. These assignments and the checkpoint are drafts for team confirmation.

### Planning budget

We expect the project to have relatively low infrastructure costs because we are not training or fine-tuning a large model. Development will use the team's existing laptops, local storage, GitHub, SQLite, and free or open-source development tools wherever possible. No additional hardware purchases are expected, and because the MVP is designed as a local-first application, we do not currently expect to need paid cloud hosting or a production database.

Our main expected cost is API/model usage for structured extraction, cross-meeting reconciliation, rubric-graded summarization, historical Q&A, and evaluation. Our evaluation plan currently targets a small number of purpose-recorded meeting sequences, with the exact count depending on whether teaching staff can point us to existing pre-recorded advisor/student sequences we could use instead (see Section 7); as a planning upper bound, we estimated cost assuming around 18 short meetings across six three-meeting sequences. Because the exact cost will depend on the model we select, transcript length, number of evaluation runs, and retries, we will first run a small pilot and measure the actual cost per meeting and evaluation run rather than assume a fixed cost in advance. We will also cache transcripts, embeddings, and other unchanged intermediate outputs so that repeated experiments do not unnecessarily repeat the same processing.

We propose an initial total project spending cap of \$75, broken down as follows:

- **Model/API usage - up to \$50:** Reserved for LLM calls used for extraction, reconciliation, summarization, retrieval-augmented Q&A, and evaluation. Working through our own pipeline at current API rates (roughly $1-$2 per million input tokens and $5-$10 per million output tokens for a capable model, or well under $1 per million tokens for a cheaper tier), our full 6 to 10-meeting evaluation matrix comes to well under $50, even accounting for development iteration and repeated evaluation runs.
- **Hardware - \$0 expected:** We will use hardware already owned by team members. Dedicated GPU hardware is not expected to be necessary because the primary contribution of this project is the longitudinal memory and reconciliation pipeline rather than training a new model.([Claude API Pricing 2026](https://www.cloudzero.com/blog/claude-pricing/); [OpenAI API Pricing 2026](https://www.cloudzero.com/blog/openai-pricing/))
- **Local storage/deployment - \$0 expected:** The MVP is designed as a local-first, single-user application using local storage and SQLite, so a paid production server, hosted database, or cloud deployment is not required for the core project. Speech-to-text and diarization also run locally through Whisper and pyannote.audio, both free for research use, so we do not expect to pay for a hosted transcription API either. ([pyannote/speaker-diarization-3.1 license](https://huggingface.co/pyannote/speaker-diarization-3.1), [Hugging Face](https://huggingface.co/pyannote/speaker-diarization-3.1))
- **Contingency - up to \$25:** Reserved for unexpected costs such as limited paid transcription, temporary cloud compute, or another service that becomes necessary during integration or final evaluation. This amount will only be used if the required functionality cannot reasonably be completed using our existing hardware or free/open-source resources.

Actual API and compute costs will be recorded throughout development. If projected spending begins to approach the \$75 cap, we will prioritize the core three-meeting longitudinal evaluation, reduce unnecessary repeated experiments, use lower-cost models when they meet our quality requirements, and reuse cached intermediate results before increasing the project budget. The final report will include the actual amount spent and, where applicable, measured cost per meeting or evaluation run.

## 12. Risks and Mitigations

| **Risk**                                                | **Response**                                                                                                                                           |
| :------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Incorrect speaker assignment gives a task to the wrong person | Confirm speaker mappings, preserve unknown identities, and evaluate owner attribution separately.                                                            |
| Similar tasks are incorrectly merged or completed             | Require project/owner/evidence consistency; review ambiguity and prioritize update precision.                                                                |
| Silence or partial progress is mistaken for completion        | Require explicit supported state changes; include negative and partial-completion fixtures.                                                                  |
| Summaries or cleanup invent meaning                           | Preserve raw segments, attach evidence, and manually score faithfulness.                                                                                     |
| Too little longitudinal data                                  | Purpose-record linked scenarios and clearly separate controlled results from natural-meeting results.                                                        |
| Audio integration delays the central contribution             | Start with timestamped transcript imports; reuse the sponsor pipeline for audio where available.                                                             |
| The proposal duplicates existing products                     | Compare documented capabilities honestly and emphasize measurable reconciliation behavior.                                                                   |
| Scope exceeds the available term                              | Prioritize the three-meeting task lifecycle; keep one automatic follow-up channel; defer additional channels, backward planning, slides, and native capture. |

## 13. Weekly Check-In

### Progress Made

This week, we finalized the revised project direction following feedback from our professor and TA and developed the initial project scope, architecture, evaluation plan, responsible-use plan, and team responsibilities. We also reviewed related meeting-assistant products to better define our project's contribution and began planning the evaluation harness and three-meeting test sequences.

### Top Blockers and Risks

Our main open questions are whether we will be permitted to reuse the sponsor's existing meeting pipeline, whether appropriate pre-recorded advisor/student meeting sequences are available, and whether our proposed pilot-scale evaluation dataset is sufficient for the claims we want to make. We also need to make sure that audio/transcription integration does not take development time away from the project's central contribution: cross-meeting reconciliation and persistent state.

### Planned Next Steps

Next, we will confirm sponsor-code and data access, select the first follow-up delivery channel and scheduling defaults, finalize team ownership, create the first labeled three-meeting development sequence, implement the transcript/task data contract and independent-meeting extraction baseline, and build a reproducible offline evaluation runner. This will give us an initial end-to-end evaluation path before implementing the full reconciliation pipeline.

Remaining questions for teaching staff: Is the proposed small sequence dataset sufficient for the intended claims? Is independent per-meeting extraction the right primary baseline? Should audio processing remain required, or can the sponsor pipeline serve as an upstream component? Are pre-recorded advisor/student meeting sequences with tasks and deadlines available?

## Teaching-staff discussion and next steps

During Week 3, the team met with the professor and TA twice to discuss the revised project direction, scope, and next steps. The team reports receiving approval to proceed with the meeting follow-through assistant. Based on the professor discussion, automatic follow-up on outstanding commitments is a required MVP feature, alongside persistent tracking and reconciliation. This records approval of the direction, not confirmation of every proposed metric, dataset choice, or integration detail.

Next steps are to finalize the proposal and pitch artifact, confirm task ownership, clarify access to the sponsor's meeting pipeline, and build the initial evaluation harness described in Section 11. The repository scaffold and local smoke checks are in place. The weekly check-in records progress, top blockers, and planned work and should be included in the submission PDF.
