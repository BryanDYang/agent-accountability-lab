# Milestone 1 Project Proposal

## [TBD]

**Course:** CIS-5980

**Track:** AI Engineering

**Team:** Will Liu, Guadalupe Cantera, and Bryan Yang

**Repository:** [github.com/BryanDYang/ai-capstone](https://github.com/BryanDYang/ai-capstone)

**Status:** Working proposal for the new project direction

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

Target 18 short meetings arranged into six independent three-meeting project sequences, using consenting team meetings and purpose-recorded scenarios. Split whole sequences into three development, one validation, and two held-out test sequences. Keep scenario variants and overlapping source material together to prevent leakage. These are pilot-scale targets, not a claim of statistical representativeness. Report counts and uncertainty, and expand the held-out set if feasible.

Use QMSum as a supplementary retrieval and summarization benchmark after checking its terms; it does not replace longitudinal task-state annotations.

Two team members independently annotate the held-out commitments, owners, deadlines, decisions, links between meetings, and state changes, then resolve disagreements before scoring. Include professor suggestions and their later acceptance or dismissal, completion, blocked work, partial completion, reassignment, changed deadlines, dropped tasks, duplicate mentions, similar tasks in different projects, uncertain speakers, negation, and tasks never mentioned again. Include answerable and unanswerable historical questions. Freeze prompts and thresholds before held-out evaluation.

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

**Collection and consent:** Use our own consenting team or study-group meetings and purpose-recorded scenarios. For this project, require every participant's explicit agreement before recording and before processing uploaded audio, including disclosure of any external model provider. Offer a non-recorded alternative and deletion requests without penalty. This is our product policy, not a statement of jurisdiction-specific legal sufficiency; confirm institutional requirements before collecting research-group data.

**Privacy:** Exclude student evaluations, health discussions, unpublished sensitive research, employer information, and other confidential material from development recordings. Give users a chance to exclude segments before external LLM processing. Automatic sensitive-content detection is assistive and cannot guarantee detection. Keep real recordings, transcripts, embeddings, and consent records outside Git and public demonstrations. Use fictional names and purpose-recorded examples for distributable artifacts.

**Storage and deletion:** Default to local use on encrypted storage with restricted access. Proposed retention is raw audio for 30 days and retained transcripts/tasks until the participant requests deletion or the project ends, subject to participant agreement. Deletion removes associated indexes and cached outputs; unsupported surviving tasks are flagged for review. Do not retain deleted sensitive text merely to preserve an audit trail. Document provider retention and backup limitations before any upload to an external service.

**Access:** Keep the first release single-user and local. Shared access is deferred until authorization is implemented. Within that release, all retrieval and task matching must enforce project boundaries. Summary sharing is an explicit user action.

**Licensing:** Before using the sponsor's code, public datasets, model weights, or libraries, record the exact source, version, license or terms, access requirements, and redistribution permissions. Public availability alone does not imply permission to redistribute. Keep third-party assets separate from the repository's own license, and publish dataset references or preparation instructions when redistribution is not permitted.

**Reliability and misuse:** Show uncertainty, source evidence, and corrections. Do not treat inferred task status as verified real-world performance or use the tool for student ranking. Test overlapping speech, accents, jargon, and pronoun ambiguity; report coverage limits. Generated plans remain suggestions. Model outputs cannot send messages, delete source material, or alter external calendars without a user-directed workflow.

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
| Weeks 3-5 / first implementation checkpoint | Consented sample sequence, transcript import, task extraction, persistence, CLI controls, folder watching, and calendar context                      |
| Weeks 6-8                                   | Cross-meeting reconciliation, review/undo, person/project inspection, and citation-based search                                                      |
| Weeks 9-10                                  | Suggestion tracking, meeting brief, privacy/deletion checks, and validation pilot; freeze evaluation protocol                                        |
| Weeks 11-12                                 | Held-out evaluation, baseline comparison, failure analysis, and reliability fixes                                                                    |
| Weeks 13-14                                 | Reproduce clean setup, finalize results and limitations, and prepare report and demonstration                                                        |

Week numbers describe proposed project phases, not verified course dates. Confirm the official milestone schedule before assigning calendar deadlines.

### Planning budget

Assume existing team laptops, no required hardware purchase, and local deployment. Propose a **$150 total project spending cap**: up to $100 for model/transcription usage, $30 for optional compute or demo hosting, and $20 contingency. These are allocations, not vendor price quotes or approved spending. No paid resource has been provisioned.

Run a small pilot first, measure cost per audio hour and per reconciliation/question run, and calculate the affordable evaluation volume including retries and repeated runs. Start with the proposed 18 short recordings and at most three repeated model runs per evaluation condition where affordable. Cache unchanged transcripts and reduce secondary experiments before reducing the core held-out comparison. Record actual charges separately from estimated local compute cost.

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

## 11. Milestone 1 Readiness and Requested Feedback

### Draft completed

- [X] Two-paragraph explanation and motivation
- [X] Defined terms, user story, scope, and architecture
- [X] Measurable AI outputs, baselines, annotation plan, and provisional targets
- [X] Preliminary related work and sourced product positioning
- [X] Data, consent, licensing, ethics, and deletion plan
- [X] Proposed ownership, timeline, budget, and risks

### Before submission

- [ ] Verify official Canvas rubric, required length, deadline, and submission format.
- [ ] Confirm team roles and review the new direction with teaching staff.
- [ ] Confirm access and permitted reuse of the sponsor's code, or commit to the independent pipeline.
- [ ] Confirm recording participants and institutional data requirements before collection.
- [ ] Finalize the pitch artifact (a deck of six slides or fewer, or a 3-5 minute concept video) and assemble the required single PDF submission.

Requested teaching-staff feedback: Is longitudinal commitment reconciliation an appropriate central contribution? Is the proposed small sequence dataset sufficient for the intended claims? Is independent per-meeting extraction the right primary baseline? Should audio processing remain required, or can the sponsor pipeline serve as an upstream component? Are pre-recorded advisor/student meeting sequences with tasks and deadlines available?
