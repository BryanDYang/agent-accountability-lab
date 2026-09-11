# Milestone 1 Project Proposal

## [TBD]

**Course:** CIS-5980

**Track:** AI Engineering

**Team:** Will Liu, Guadalupe Cantera, and Bryan Yang

**Repository:** [github.com/BryanDYang/ai-capstone](https://github.com/BryanDYang/ai-capstone)

**Status:** Milestone 1 proposal incorporating team submission-draft input

**Updated:** September 11, 2026

## 1. Project Explanation and Motivation

Weekly research meetings produce student commitments, professor suggestions, decisions, and deadlines that are difficult to maintain across weeks. Researchers report what they tried and what they plan to do next; the professor may recommend an experiment, alternative approach, or paper. Summaries capture what was said, but teams still have to connect those updates to earlier commitments and determine whether a suggestion was ever tried. The sponsor, CCB, already has a pipeline that records, transcribes, identifies speakers, cleans transcripts, and files meeting titles and summaries. This project builds the follow-through layer on top of those meeting artifacts.

We propose [TBD], a local background service with a CLI control interface and native OS integrations for advisors and research teams. Once configured, it detects new meeting artifacts, associates them with calendar context, extracts decisions and owned commitments, and reconciles later statements with persistent project memory. Professor suggestions remain separate until a researcher accepts them as commitments. Users can inspect evidence, correct records, review ambiguous matches, read rubric-graded summaries, and ask historical questions with meeting and timestamp citations. The central engineering contribution is an evaluated workflow for maintaining commitments and suggestions across meetings, with traceable changes and explicit uncertainty.

**Engineering question:** Can an assistant reliably maintain commitments across a sequence of meetings while reducing manual reconciliation and avoiding unsupported task updates?

## 2. Users and Example Workflow

The primary users are a PhD advisor and the researchers or students who meet with them weekly. A secondary development setting is our own consenting project team or study group.

1. Participants agree to recording, processing, and retention before the configured pipeline processes meeting artifacts.
2. After a weekly research sync, [TBD] detects a new artifact in a configured local folder and matches it to the project, calendar event, attendees, date, and timezone. Uncertain matches require review.
3. The upstream pipeline supplies a timestamped transcript. Users can confirm speaker names and correct recognition or extraction errors.
4. [TBD] records the decision to standardize on ViT-B/16, Will's commitment to rerun the baseline by Friday, and the advisor's commitment to send two papers. A recommendation to try mixed precision stays on a separate suggestion list until accepted.
5. At the next meeting, “The rerun finished early on the cluster” updates the matching task to done when the owner, project, and evidence support the match. The original commitment and new evidence remain linked.
6. The advisor's unsent papers remain open and roll into the next meeting brief. A stated new deadline updates the existing record; silence never marks an item done or dropped.
7. The CLI exposes runtime status, configuration, meeting history, evidence, and review controls. Proposed commands include `labsync status`, `labsync config`, `labsync history`, and `labsync inspect <meeting-id>`.
8. A question such as “What did we decide about the baseline last month, and why?” returns a dated decision, rationale, speaker attribution, and timestamp citation, or states that the available evidence is insufficient.

Calendar integration is required for meeting context. Native reminder synchronization is a planned integration; automatic emails, scheduled nudges, and broader calendar writes are cuttable. External writes require explicit configuration and a user-authorized workflow.

## 3. Terms and Observable Outputs

| Term                   | Definition and output                                                                                                                                                   |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Transcription          | Converts speech into timestamped text; it does not establish speaker identity.                                                                                          |
| Transcript cleanup     | Edits recognition errors, punctuation, and filler without changing meaning; it produces a separate cleaned version linked to the original segments.                     |
| Diarization            | Separates stretches of audio by voice; it produces speaker labels, not names.                                                                                           |
| Speaker identification | Maps speaker labels to attendee names with user confirmation; an attendee list alone does not establish who spoke.                                                      |
| Action item            | A named person's commitment to a specific task, with an optional due date, status, and source timestamp; an unowned suggestion remains a candidate for clarification.   |
| Suggestion             | A professor recommendation tracked with its source and intended researcher when explicit; it stays separate from commitments until accepted.                            |
| Decision               | A statement settling a question, stored with its source; a later reversal is a linked new decision rather than an overwrite.                                            |
| Reconciliation         | Matches a later statement to an existing commitment and proposes or records an evidenced change; similar wording alone is insufficient.                                 |
| Summary                | A concise account of discussion, decisions, and commitments evaluated for faithfulness, coverage, and usefulness.                                                       |
| Suggested plan         | Proposed steps working backward from a confirmed deadline; its invented intermediate dates are not meeting commitments.                                                 |
| Consent                | Recorded agreement by every participant to the stated recording and processing policy before audio processing; an upload alone is not evidence of everyone's agreement. |

## 4. Scope and Deliverable

### Required MVP

- Run a local background service that watches a configured meeting-artifact folder, with a CLI for configuration, status, history, inspection, and review.
- Integrate calendar context to associate meetings with projects, attendees, dates, and timezones.
- Import timestamped transcripts from the sponsor pipeline or manual imports; confirm or correct speaker mappings.
- Generate structured decisions, commitments, and a concise summary with source references.
- Maintain open, in-progress, blocked, done, and dropped tasks across meeting sequences, including owner and deadline changes. Carry-forward is a history event, not evidence of completion.
- Track professor suggestions separately, including whether they are accepted, tried, or explicitly dismissed, with evidence for changes.
- Present ambiguous matches for review and provide correction and undo with change history.
- Provide CLI inspection by meeting, person, and project, plus a pre-meeting brief of outstanding tasks and suggestions.
- Answer historical questions using retrieved evidence with transcript timestamps and audio links when retained audio is available.
- Demonstrate consent gating, selective exclusion, deletion, and project-scoped retrieval.
- Deliver a local application, reproducible evaluation fixtures, measured results, and setup documentation.

### Stretch goals

Sophisticated diarization, voice-profile enrollment, backward planning, dedicated Zoom/iPhone capture, slide-aware summaries, native reminder synchronization, and automatic scheduled notifications. Reuse the sponsor capture pipeline where permitted; implementing a new speech pipeline is secondary to the persistent-state workflow. Manual speaker confirmation is sufficient for the MVP.

### Boundaries

The project will not train a speech model, infer productivity scores, monitor people without consent, deploy a production multi-tenant service, or claim to establish real-world task completion beyond what participants report. Initial evaluation covers English-language small-group meetings; broader language and setting claims require additional evidence.

## 5. Architecture and AI Engineering

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
       Persistent history + CLI inspection + next-meeting brief
                         |
       Optional authorized native reminder synchronization

Historical question -> decision ledger + hybrid retrieval -> cited answer
```

The AI work comprises structured extraction, semantic task matching, evidence-grounded summarization, and retrieval-augmented answers. Application code validates schemas, source references, project boundaries, and permitted state transitions. Transcript content is untrusted data and cannot authorize tool execution or change system instructions.

Each task has a stable ID, project ID, owner ID, description, nullable due date, status, and original source segment. Each update records the task ID, previous and new values, evidence segment, meeting date, processing time, and whether a user or model proposed and accepted it. Suggestions and unresolved candidates are kept separately from accepted tasks. Accepted suggestions link to the resulting task without losing their original source. An update cannot reference a nonexistent segment or silently move a task into another project.

Processing is idempotent: re-uploading or retrying a meeting must not duplicate accepted tasks. Meetings are reconciled in event order; importing older meetings must not silently overwrite newer task state. Speaker and transcript corrections invalidate dependent outputs for review or recomputation. Search indexes and cached outputs follow source deletions.

### Preliminary implementation choices

| Layer             | Proposed choice and purpose                                                                                                             |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Interface         | CLI for runtime control, meeting inspection, task correction, and ambiguity review                                                      |
| Service           | Python background worker with schema validation for ingestion, extraction, and task operations                                          |
| Speech            | Inspect the sponsor's existing pipeline first; use Whisper and pyannote.audio if reuse is unavailable or unsuitable                     |
| Persistence       | SQLite for the local MVP, local private audio storage, and timestamped transcript segments                                              |
| Retrieval         | SQLite decision ledger plus project-filtered lexical and dense retrieval over speaker-attributed turns; retain source IDs               |
| Model integration | One configured LLM behind a small adapter, with structured outputs and bounded retries; exact model selected after a quality/cost pilot |
| Verification      | Pytest for extraction/state behavior and end-to-end CLI checks for detection, calendar matching, review, correction, and citations      |
| Observability     | Record model/prompt versions, usage, processing failures, stage latency, and cost per hour of audio                                     |

No sponsor code is assumed available or licensed until inspected. Transcript imports allow development of the core follow-through workflow while audio integration proceeds. Prompt caching is an optional measured optimization after correctness is established.

## 6. Evaluation Plan

### Data and experimental design

Start with a pilot of 6-8 short meetings from consenting team meetings and purpose-recorded scenarios, including at least two complete three-meeting project sequences. Use this pilot to refine the annotation guide, estimate costs, and confirm data availability; it is not the full held-out evaluation. Ask teaching staff whether existing pre-recorded advisor/student sequences are available with appropriate permissions.

The expanded evaluation plan, subject to data availability and the $75 budget, is 18 short meetings across six independent three-meeting sequences: three development, one validation, and two held-out test sequences. Keep whole sequences, scenario variants, and overlapping source material together to prevent leakage. Do not reuse pilot material used for tuning as held-out test data. If the expanded set is infeasible, finalize and document a smaller sequence-level split before testing and narrow the claims accordingly. These are pilot-scale targets, not a claim of statistical representativeness; report actual counts and uncertainty.

Use QMSum as a supplementary retrieval and summarization benchmark after checking its terms; it does not replace longitudinal task-state annotations.

Two team members independently annotate the held-out commitments, owners, deadlines, decisions, links between meetings, and state changes, then resolve disagreements before scoring. Include professor suggestions and their later acceptance or dismissal, completion, blocked work, partial completion, reassignment, changed deadlines, dropped tasks, duplicate mentions, similar tasks in different projects, uncertain speakers, negation, and tasks never mentioned again. Score attribution hallucination separately, including tasks or decisions assigned to the wrong speaker despite valid output schemas. Include answerable and unanswerable historical questions. Freeze prompts and thresholds before held-out evaluation.

Compare two conditions using the same transcripts, model, and extraction settings:

1. **Independent meeting extraction:** Produce each meeting's summary and task list without reconciling earlier tasks.
2. **Persistent reconciliation:** Use the same extraction plus existing task state and source-backed updates.

Score both against the expected current task list after each meeting, counting duplicates, stale open items, unsupported changes, and missing tasks. Separately compare a simple lexical task matcher with semantic reconciliation to test the value of the matching component. Evaluate on corrected transcripts and raw pipeline outputs to distinguish reasoning failures from speech and speaker errors.

### Component comparisons

Use the same input splits and configured model for each paired comparison. Report measured differences rather than assuming baseline weaknesses or performance gains.

| Component      | Baseline                                        | Proposed pipeline and measurements                                                                                                                        |
| -------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Extraction     | Unconstrained zero-shot extraction              | Schema-enforced records with confirmed speaker mapping; task F1, owner accuracy, and decision precision                                                   |
| Reconciliation | Keyword/Jaccard matching                        | Contextual matching against persistent project state; linkage F1, state-transition accuracy, and false duplicate rate                                     |
| Summaries      | Single-pass summary                             | Generate, critique, and revise against a fixed rubric; blind human ratings of faithfulness, attribution, conciseness, actionability, and coverage         |
| Historical Q&A | Dense-only retrieval over 500-token text chunks | Decision ledger plus lexical/dense retrieval over timestamped turns; faithfulness, context precision/recall, citation accuracy, and audio timestamp error |

Additional development targets from the Word draft are extraction F1 >= 0.88, owner attribution >= 95%, linkage F1 >= 0.85, false duplicate rate <= 5%, answer faithfulness >= 0.95, context precision >= 0.90, and audio anchor error <= 10 seconds where source audio exists. These are experimental targets, not observed results or guarantees. Multi-month retrieval claims require an archive covering that period; the three-meeting demo alone cannot validate them.

### Metrics and provisional success criteria

These are proposed acceptance targets, not measured results. Calibrate them on development and validation data before freezing the test protocol.

| Output                | Measurement                                                                                                                            | Proposed target                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Extracted commitments | Precision and recall against adjudicated tasks; a match requires the correct owner and equivalent commitment                           | Precision >= 90%, recall >= 80%                                                              |
| Cross-meeting updates | Correct task link and requested field/status change among automatic updates                                                            | Precision >= 95%; also report recall and automatic-update coverage                           |
| Current task list     | Correct owner, description, status, and supported due date after each meeting                                                          | Higher state accuracy than independent extraction; report absolute difference and raw counts |
| False completion      | Unsupported done transitions divided by all automatic done transitions                                                                 | Zero observed in the held-out demo set, with sample size reported                            |
| Human review burden   | Fraction of candidate updates requiring review and review time                                                                         | Report alongside accuracy; no success claim from routing everything to review                |
| Historical answers    | Correct answer and citations that support each substantive claim                                                                       | >= 90% supported-answer rate; separately score abstention on unanswerable questions          |
| Summaries             | Human rubric for faithfulness, attribution, conciseness, actionability, and coverage                                                   | Mean >= 4.6/5 overall; faithfulness 5/5, with no unsupported claims in the final demo        |
| Audio and speakers    | Word error rate on selected hand-transcribed segments; diarization error and owner-attribution accuracy                                | Report by recording condition; diagnose impact on downstream task errors                     |
| Plans (stretch only)  | Confirmed final deadline respected; suggested dates labeled; no unaccepted step becomes a commitment                                   | All deterministic checks pass                                                                |
| System behavior       | Folder detection, calendar matching, duplicate ingestion, correction, deletion, consent gating, project isolation, citation navigation | All required end-to-end scenarios pass                                                       |
| Efficiency            | End-to-end and stage latency, tokens, cost per audio hour, and manual reconciliation time                                              | Report hardware/model and median/range; set operational budget after pilot                   |

Summary rubric anchors: **1** = materially incorrect or unusable, **3** = mostly correct but requires substantive editing, **5** = faithful and immediately useful. Scores 2 and 4 represent intermediate quality. Reviewers score dimensions separately. An LLM judge may assist error triage but will not replace human ground truth for ownership, dates, completion, or citation support.

### Minimum end-to-end demonstration

Run a three-meeting sequence in which the first meeting creates two owned tasks and a decision, the second completes one task and changes the other's deadline, and the third leaves the remaining task open. Include a professor suggestion that is later accepted or dismissed, a blocked task, an ambiguous mention that requests review, a cited historical question, and a correction. Demonstrate folder detection, calendar association, and CLI inspection. Re-import an artifact to demonstrate no duplication, then delete a meeting to demonstrate removal of associated searchable content and explicit handling of dependent task evidence.

## 7. Related Work and Product Positioning

The following references inform component selection and evaluation; they are not evidence that the complete proposed workflow already works.

| Source                                                           | Relevance and boundary                                                                                                                          |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| [Whisper, Radford et al., 2022](https://arxiv.org/abs/2212.04356) | Speech recognition foundation; assess our recordings rather than assuming accurate domain terminology or speaker attribution.                   |
| [pyannote.audio](https://github.com/pyannote/pyannote-audio)      | Speaker diarization tools; named attendee mapping remains a separate step.                                                                      |
| [QMSum, Zhong et al., 2021](https://arxiv.org/abs/2104.05938)     | Query-based meeting summarization benchmark for retrieval and summary experiments; does not establish our longitudinal task-state ground truth. |
| [MeetingBank, Hu et al., 2023](https://arxiv.org/abs/2305.17529)  | Public meeting summarization benchmark; municipal meetings differ from recurring advisor/student meetings.                                      |
| [AMI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/corpus/)     | Candidate meeting audio and annotation source; inspect available annotations and permitted use before selecting a subset.                       |

Preliminary product review, checked September 8, 2026:

| Product                                                                                                | Documented strength                                                    | Implication for this proposal                                                                                     |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [Otter](https://help.otter.ai/hc/en-us/articles/25983095114519-Action-Items-Overview)                   | Consolidates assigned action items across conversations.               | A cross-meeting task list alone is not a differentiator; evaluate evidence-backed updates from subsequent speech. |
| [Granola](https://docs.granola.ai/help-center/getting-more-from-your-notes/chatting-with-your-meetings) | Supports questions across meeting notes, action items, and follow-ups. | Historical meeting chat alone is not a differentiator; focus on explicit task state and corrections.              |
| [Zoom AI Companion](https://news.zoom.com/zoom-agentic-ai/)                                             | Describes task action, memory, and meeting action-item capture.        | Broad claims that existing assistants stop at summaries are not defensible.                                       |
| [Google Meet notes](https://support.google.com/meet/answer/14754931?hl=en)                              | Produces meeting notes, summaries, and suggested next steps.           | Test longitudinal reconciliation directly rather than inferring limitations from a notes feature description.     |

Our proposed distinction is a transparent, evaluated research-team workflow for matching later statements to prior commitments, resolving uncertainty, and inspecting task-change evidence. Product documentation does not establish which competitors support every detail of this workflow. A small hands-on comparison remains planned; we will not claim that no existing product tracks actions across meetings.

## 8. Data, Licensing, and Responsible Use

**Data Sources and Evaluation:** For development and evaluation, we will mainly use purpose-recorded scenarios and meetings from our own team or study groups where everyone has agreed to participate. These meetings will be designed to include the kinds of situations our system needs to handle, such as commitments, professor suggestions, decisions, task updates, blockers, changed deadlines, and ambiguous references to things discussed in previous meetings. We will not assume that real research lab meetings, sponsor recordings, or existing meeting archives are available for us to use. If we later use real research meetings, we will first confirm that we have participant consent and permission to process that data. We will also keep controlled/test scenarios separate from natural meetings when reporting our evaluation results.

**Consent and Participant Control:** Everyone in a meeting must agree to the recording and processing policy before recording begins and before uploaded audio is processed. Participants should know what is being collected, what information the system will keep, whether any meeting content is being sent to an external AI provider, how long the data will be retained, and how they can request deletion. We will document the applicable recording and processing requirements for each meeting while retaining every participant's explicit agreement as our project policy. This policy is not a claim of jurisdiction-specific legal sufficiency. Simply uploading a recording does not mean that everyone in that recording consented. Participants should also have a non-recorded option and be able to request that a meeting, or specific parts of a meeting where possible, are excluded from AI processing. Before using real research-group data, we will confirm any additional institutional requirements that apply.

**Privacy and Data Minimization:** Research meetings can include information that should not become part of a long-term AI memory, such as unpublished research (including patent-pending architectures), personnel discussions, credentials, grant information, or other confidential material. Our goal is therefore to store only what the system actually needs for its longitudinal-memory functions. Persistent memory should focus on supported decisions, commitments, task updates, professor suggestions, and the evidence needed to verify them rather than saving unrelated conversation indefinitely. For development and evaluation, we will avoid intentionally including sensitive information that is not necessary for testing the system. Real recordings, transcripts, embeddings, speaker mappings, and extracted project data will not be committed to Git or included in public demos.

**Storage, Retention, and Deletion:** The MVP will be local-first and single-user, with meeting data stored on access-controlled, encrypted local storage. We also recognize that deleting the original audio is not enough. A meeting can create a transcript, embeddings, search indexes, summaries, tasks, decisions, speaker mappings, and other derived data. If a meeting or portion of a meeting is deleted, the system should also remove the related searchable and cached artifacts. Rather than permanently erasing the source audio the moment deletion is requested, we will route it through the OS's native trash first, so it stays recoverable for a short window in case the deletion was accidental or a dispute requires the original evidence, before it is purged for good. The recovery window and purge procedure must be defined and communicated before collection; moving audio to trash is not permanent deletion. Trashed audio must be excluded from ingestion and retrieval during that window. If deleted evidence was the only support for an existing task or decision, that record should be flagged for review rather than continuing to appear as verified information. Retention periods will be decided and clearly communicated before we begin collecting evaluation data.

**Evidence, Attribution, and Human Review:** Because this system creates a memory that carries information across meetings, we do not want one incorrect AI inference to become a permanent part of that history. The system should preserve evidence for the tasks, decisions, and state changes it creates. A professor saying, "someone should try this" should not automatically become a commitment assigned to a student, and misattributing a task or decision to the wrong speaker is a failure mode we are treating as its own testable category (attribution hallucination) rather than assuming schema-enforced extraction rules it out. Similarly, silence about a task in the next meeting should not mean it was completed or abandoned, and partial progress should not automatically mean completion. When ownership, task matching, or state changes are ambiguous, the system should flag the item for human review instead of making the decision on its own. Users should also be able to correct speaker mappings, extracted records, and reconciliation decisions if the system gets something wrong.

**Grounded Summaries and Historical Q&A:** Summaries and historical answers should be grounded in actual meeting evidence rather than the model filling in missing information. Important claims should point back to the relevant meeting and transcript timestamp, with an audio reference when the original audio is still available. If the system does not have enough evidence to answer a question, it should say that rather than make its best guess. For example, discussing an experiment is not the same thing as explicitly committing to complete it. Our evaluation will include both answerable and intentionally unanswerable questions so we can test whether the system retrieves the right evidence and knows when it should not make a claim.

**Project Isolation and External Actions:** Information from one research project should not accidentally appear in another project's results. Retrieval and reconciliation will therefore be scoped to the selected project. We will also treat transcript content as untrusted input; something said during a meeting cannot override system instructions or authorize the system to take an external action. The model will not independently send messages, delete recordings, modify calendars, or take similar actions. Features such as reminders, calendar updates, or summary sharing will only happen through workflows that the user has explicitly enabled.

**External AI Services, Licensing, and Third-Party Data:** Before sending meeting content to an external AI or API provider, we will document what data leaves the local system, why it needs to be sent, and the provider's relevant retention and data-use policies. Participants should know when their meeting content may be processed externally, and we will avoid sending excluded or unnecessary portions of a meeting where possible. We will also document the source, version, license, access restrictions, and redistribution permissions for any sponsor code, public datasets, pretrained models, libraries, or other third-party assets we use. Something being publicly available does not automatically mean we have permission to redistribute it. Sponsor code will only be incorporated after we confirm that we are allowed to use it.

**Responsible Use and Non-Goals:** [TBD] is meant to help research teams remember and follow up on what was discussed across meetings. It is not meant to evaluate the people in those meetings. The system will not create productivity or performance scores, rank students or researchers, use speaking frequency or number of assigned tasks as a measure of contribution, infer sensitive personal characteristics, or monitor meetings without participant consent. It also will not treat something reported during a meeting as independent proof that the work happened in the real world. The system's job is to accurately represent and connect what was said in the meetings, while keeping the original evidence available for verification. Known limitations, including overlapping speech, technical jargon, uncertain speakers, and ambiguous references, will be evaluated and reported rather than hidden.

## 9. Team, Timeline, and Budget

### Proposed ownership

| Member            | Primary responsibility                          | First implementation checkpoint                                                 |
| ----------------- | ----------------------------------------------- | ------------------------------------------------------------------------------- |
| Will Liu          | Data contracts, extraction, and reconciliation  | Task schema, source references, update rules, and ambiguous-match handling      |
| Bryan Yang        | Runtime, CLI, storage, and pipeline integration | Transcript-to-task vertical slice with CLI corrections and timestamp inspection |
| Guadalupe Cantera | Evaluation, data preparation, and quality       | Consent/data protocol, sequence fixtures, annotation guide, and pilot metrics   |

All members review the proposal, consent practices, evaluation claims, and final demo. These proposed assignments need team confirmation.

### Relative course timeline

| Period                                      | Deliverable                                                                                                                                          |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Weeks 1-2 / Milestone 1                     | Proposal, scope, preliminary product review, team roles, and rubric verification; confirm sponsor-code access and data permissions before collection |
| Weeks 3-5 / first implementation checkpoint | Initial evaluation harness and extraction baseline, synthetic development sequence, consented samples when available, transcript import, persistence, and initial CLI/calendar integration |
| Weeks 6-8                                   | Cross-meeting reconciliation, review/undo, person/project inspection, and citation-based search                                                      |
| Weeks 9-10                                  | Suggestion tracking, meeting brief, privacy/deletion checks, and validation pilot; freeze evaluation protocol                                        |
| Weeks 11-12                                 | Held-out evaluation, baseline comparison, failure analysis, and reliability fixes                                                                    |
| Weeks 13-14                                 | Reproduce clean setup, finalize results and limitations, and prepare report and demonstration                                                        |

Week numbers describe proposed project phases, not verified course dates. Confirm the official milestone schedule before assigning calendar deadlines.

### Draft evaluation-harness checkpoint for Milestone 2

By the next milestone, aim to run a small, reproducible evaluation from timestamped transcripts to a saved score report. This checkpoint establishes the evaluation machinery; it does not require the full audio pipeline or demonstrate final model quality.

| Proposed owner | Deliverable | Completion check |
| --- | --- | --- |
| Guadalupe Cantera | One synthetic three-meeting development sequence and a short annotation guide | Expected commitments, owners, source segments, and task states are labeled after each meeting and reviewed by a second team member. Include completion, a changed deadline, an unaccepted suggestion, an ambiguous reference, and a task that is not mentioned again. |
| Will Liu | Transcript/task output contract and initial independent-meeting extraction baseline | Baseline outputs use the agreed schema and retain source IDs. Record the model, prompt version, and run settings. Define how semantically equivalent commitments are matched to annotations, with human adjudication where needed. |
| Bryan Yang | Evaluation runner and offline scorer tests | One documented command loads fixtures and saved predictions and produces a report. A correct prediction fixture receives the expected score; deliberately wrong owners, duplicate tasks, unsupported completion, and invalid citations are detected. CI exercises this without API calls. |

The first report should include task precision/recall, owner accuracy, duplicate counts, unsupported completion counts, and source-reference validity, with numerators and denominators. Once reconciliation is runnable, score the expected task state after each meeting and compare it with the independent-meeting baseline on the same sequence. Keep this sequence in development only; it must not become held-out evidence. Live model runs are separate from deterministic CI tests and record usage and latency. These assignments and the checkpoint are drafts for team confirmation.

### Planning budget

Development will use existing team laptops, local storage, GitHub, SQLite, and free or open-source development tools where suitable. We do not plan to train or fine-tune a large model, buy dedicated GPU hardware, or provision a paid production server or database for the local, single-user MVP.

Propose an initial **$75 total project spending cap**:

| Category | Proposed allocation and purpose |
| --- | --- |
| Model/API usage | Up to $50 for extraction, reconciliation, rubric-graded summarization, historical Q&A, and evaluation |
| Hardware | $0 expected; use hardware already owned by the team |
| Local storage/deployment | $0 incremental spending expected; use local storage and SQLite, with the sponsor pipeline or local Whisper/pyannote.audio subject to access, license, and hardware checks |
| Contingency | Up to $25 for limited paid transcription, temporary compute, or another necessary integration/evaluation service when existing resources are insufficient |

These are proposed allocations, not approved spending or verified vendor quotes. No paid resource has been provisioned. The budgeting scenario allows for up to 18 short meetings across six three-meeting sequences, while the initial pilot targets 6-8 meetings as described in Section 6. Actual affordability depends on the selected model, transcript lengths, evaluation conditions, repeated runs, and retries. Validate the full evaluation matrix against the $50 API allocation using pilot measurements.

Run a small pilot first and measure actual cost per meeting, per audio hour, and per evaluation run. Verify the selected provider's current rates and the exact model/library terms before use. Cache unchanged transcripts, embeddings, and other intermediate outputs, with invalidation after corrections or deletion. Record API charges and any paid compute separately from estimated local compute costs.

If projected spending approaches $75, prioritize the core three-meeting longitudinal evaluation, reduce unnecessary repeated experiments, use lower-cost models only when they meet quality requirements, and reuse valid cached outputs before proposing a budget increase. The final report will include actual spending and measured unit costs.

## 10. Risks and Mitigations

| Risk                                                          | Response                                                                                                         |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Incorrect speaker assignment gives a task to the wrong person | Confirm speaker mappings, preserve unknown identities, and evaluate owner attribution separately.                |
| Similar tasks are incorrectly merged or completed             | Require project/owner/evidence consistency; review ambiguity and prioritize update precision.                    |
| Silence or partial progress is mistaken for completion        | Require explicit supported state changes; include negative and partial-completion fixtures.                      |
| Summaries or cleanup invent meaning                           | Preserve raw segments, attach evidence, and manually score faithfulness.                                         |
| Too little longitudinal data                                  | Purpose-record linked scenarios and clearly separate controlled results from natural-meeting results.            |
| Audio integration delays the central contribution             | Start with timestamped transcript imports; reuse the sponsor pipeline for audio where available.                 |
| The proposal duplicates existing products                     | Compare documented capabilities honestly and emphasize measurable reconciliation behavior.                       |
| Scope exceeds the available term                              | Prioritize the three-meeting task lifecycle; defer notifications, backward planning, slides, and native capture. |

## 11. Teaching-Staff Feedback and Next Steps

During Week 3, the team met with the professor and TA twice to discuss the revised project direction, scope, and next steps. The team reports receiving approval to proceed with the meeting follow-through assistant. This records approval of the direction, not confirmation of every proposed metric, dataset choice, or integration detail.

Next steps are to finalize the proposal and pitch artifact, confirm task ownership, clarify access to the sponsor's meeting pipeline, and build the initial evaluation harness described in Section 9. The repository scaffold and local smoke checks are in place. The [weekly check-in](../weekly_journal.md#week-3) records progress, top blockers, and planned work and should be included in the submission PDF.

Remaining questions for teaching staff: Is the proposed small sequence dataset sufficient for the intended claims? Is independent per-meeting extraction the right primary baseline? Should audio processing remain required, or can the sponsor pipeline serve as an upstream component? Are pre-recorded advisor/student meeting sequences with tasks and deadlines available?
