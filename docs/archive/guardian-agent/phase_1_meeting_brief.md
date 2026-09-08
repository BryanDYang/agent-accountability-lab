# Phase 1 faculty meeting brief

**Purpose:** Rehearse an eight-minute pitch and leave the 30-minute meeting with proposal decisions.
**Basis:** The professor's meeting announcement supplied by Bryan and the repository's current proposal. This is preparation, not a record of faculty approval or a substitute for the Canvas rubric.
**Pre-read:** [Project proposal](project_proposal.md), already shared with the professor according to Bryan. Confirm the shared copy matches the version the team will discuss.

## Before the meeting

- Attend as the full team: Bryan, Will, and Guadalupe.
- Agree on the three questions below and the proposed cuts before joining.
- Open the shared proposal, [pitch draft](pitch_deck.md), and [UI mockup](../mockup/index.html). Label the mockup as a concept, not a working model integration or measured result.
- Assign a note-taker and timekeeper. Suggested speaking split: Bryan covers problem and product; Will covers governance and scope; Guadalupe covers evaluation.
- Rehearse once with a timer. Stop the pitch at eight minutes even if some detail is left out.

## Use the 30 minutes

| Time | Activity | Intended result |
|---|---|---|
| 0:00-8:00 | Pitch, with at most one minute of mockup walkthrough | Shared understanding of problem, audience, build, track, and success |
| 8:00-23:00 | Three questions, roughly five minutes each | Decisions on scope, evidence, and Week 5 expectations |
| 23:00-28:00 | Confirm cuts and proposal changes | Explicit minimum deliverable and revisions |
| 28:00-30:00 | Read back decisions, owners, and deadlines | Agreed actions before Friday submission |

## Eight-minute talk track

### 0:00-1:30: Problem and audience

“We are building Guardian Agent, a visual context-governance workbench for coding agents, on the AI Engineering track. Our users are engineers and AI platform owners responsible for coding-agent reliability.

“A coding agent may receive a current repository rule alongside an obsolete instruction, a rule for another directory, or an untrusted document. Relevance alone does not establish whether that context should guide the task. Developers also need a way to inspect what was supplied and connect it to the resulting edits and tests.”

### 1:30-3:00: One concrete example

“Imagine a task to update a function under `src/service/`. The candidate context includes the current service rule, a superseded version of that rule, and an instruction that applies only under `legacy/`. Our fixtures explicitly record versions and scope.

“Without governance, the model receives all three candidates. With governance, deterministic checks exclude the superseded and out-of-scope instructions. The interface shows each decision and its reason, the exact model input, and the outputs and checks for both conditions. We will test whether that change actually improves the coding outcome. We do not yet have measured results.”

Show the candidate list, decision trace, exact input, and comparison area in the mockup. Do not spend this minute on every UI control.

### 3:00-4:30: What we will build and the boundary

“The deliverable is a local workbench, deterministic governance policies, one coding-model integration, and a reproducible evaluation harness. The first implementation uses controlled fixtures with declared provenance, scope, trust, and version metadata. Unresolved conflicts can be quarantined with a visible reason.

“We are not attempting to establish the truth of arbitrary documents. The engineering contribution is the complete, inspectable path from context admission to model input and tested task outcomes. Our current first-model choice is Qwen2.5-Coder 7B Instruct through Ollama; local execution still needs validation.”

### 4:30-6:30: Evaluation and success

“Our headline outcome is task-success rate: the fraction of coding tasks passing all required tests and policy checks. We will also report repository-rule violations, invalid-context admission, valid-context rejection and quarantine, and token and latency costs. Clean controls test whether filtering harms tasks where the context was already valid.

“We will compare no governance, prompt-only governance, and deterministic governance using the same task, repository revision, candidates, model settings, and available tools. Prompt-only can run in the harness without requiring a third interactive UI mode.

“The data plan is team-authored synthetic repositories and fixtures with ground truth and executable checks specified before trials. This avoids relying on private data access, but limits generalization. The current 36-run estimate is a small two-condition pilot, not 36 independent tasks or evidence of broad reliability. Including prompt-only makes that 54 runs under the same six-fixture, three-repeat assumption. Final task counts and thresholds need pilot evidence and faculty feedback.”

Filtering explicitly invalid inputs demonstrates that the policy works; it does not by itself demonstrate better model outcomes. Keep these claims separate. Freeze tuning choices and thresholds before held-out final evaluation.

### 6:30-8:00: Scope, schedule, and transition

“We would protect one complete fixture-to-model-to-test path before expanding the UI or model support. Our full proposal targets five adversarial scenario classes plus clean controls. If that breadth is too large, our proposed fallback is stale or superseded context, wrong-directory scope, and clean controls, with more independent tasks within those categories.

“We noticed our draft timeline delays governed execution beyond the Week 5 evaluation milestone. We propose moving a minimal governed runner, the baselines, metrics, and first error analysis into Weeks 3-5, then expanding the suite and polishing the workbench. We would like your guidance on three decisions.”

## Three questions to spend the discussion on

| Ask the professor | Team's recommended starting position | Decision to capture |
|---|---|---|
| Is a deterministic, metadata-based context workbench sufficiently substantial for the AI Engineering track, and what is the smallest acceptable scenario scope? | One local model and a complete evidence path; retain the full scenario target if feasible, with the narrower fallback above | Accepted contribution, required scenario breadth, and explicit cuts |
| Are controlled synthetic coding tasks with executable tests and policy checks an adequate evaluation foundation, and should prompt-only be a required baseline? | Include prompt-only in the harness; distinguish admission correctness from downstream task improvement; reserve independent held-out tasks | Required baselines, primary outcome, ground-truth expectations, and limits on claims |
| For Week 5, is a minimal runner covering all three conditions, justified metrics, a small fixture pilot, and initial error analysis sufficient while the UI is still basic? | Bring evaluation forward; calibrate final experiment size after the pilot | Concrete Milestone 2 acceptance criteria and any minimum dataset expectations |

## Know what we would cut

These are recommendations to discuss, not changes already approved for the proposal.

| Protect in the minimum version | Cut or defer first |
|---|---|
| One model and one controlled coding runner | Stronger-model comparison and additional providers |
| Prepared fixtures with explicit metadata | Automatic retrieval, broad document extraction, and drag-and-drop polish |
| Deterministic scope and supersession checks with reason codes | Model-assisted conflict classification |
| Exact model-input inspection and linked outcome records | Source correction, replay, and blast-radius analysis |
| Paired execution, prompt-only harness baseline, task tests, policy checks, and clean controls | Third interactive comparison mode and formal human-usability study |
| Independent tasks and honest reporting of failure cases | Scenario breadth if the professor accepts a narrower scope |

Do not cut clean controls, valid-context preservation checks, or outcome evaluation to make the UI look more complete.

## Proposed Week 5 delivery plan

| By | Deliverable | Existing workstream owner |
|---|---|---|
| Week 3 | Versioned fixture contract, ground-truth labels kept separate from runtime inputs, one disposable coding task, model invocation, and saved exact request/response | Will: contract; Guadalupe: fixture/checks; Bryan: runner/model |
| Week 4 | Minimal deterministic governance plus no-governance and prompt-only baselines; matched execution; automated task and policy scoring | Will: governance; Bryan: condition runner; Guadalupe: scoring |
| Week 5 | Runnable documented harness, small adversarial and clean pilot, justified metrics, per-condition report, and initial error analysis | Guadalupe: analysis; Bryan: reproducibility; Will: policy-error review |

For the initial error analysis, inspect actual failures and classify them as fixture/label problems, wrong admission or rejection, unresolved conflict, model failure despite valid context, or runner/check failures. Include examples linked to the exact input, output, and failed check. Report setup failures separately from completed trials. Watch the evaluation lectures and four-part error-analysis demo series before finalizing this protocol.

Later weeks can expand independent tasks and scenario coverage, complete the comparison UI, and run the frozen final evaluation. A polished UI is not a prerequisite for collecting early evidence.

## Proposal reconciliation before Friday

- **Timeline:** Replace the current Weeks 3-5 ungoverned-only checkpoint with the agreed runnable evaluation milestone. Keep later weeks for expansion and final evaluation.
- **Model status:** The proposal already names Qwen2.5-Coder 7B Instruct through Ollama. The pitch, journal, and TODO still describe selection as open. Distinguish a provisional selection from validated integration.
- **Baseline identity:** The proposal specifies all supplied candidates as the no-governance baseline; the evaluation appendix calls it relevance-only retrieval. Use one definition and hold candidate collection fixed.
- **Pilot size:** Clarify unique fixtures versus repeated model runs. Budget 54 task-model runs if all three conditions use six fixtures and three repeats; this does not settle final sample size.
- **Ground truth:** Runtime policies may use declared metadata, but must not read oracle labels or expected decisions from evaluation fixtures. Avoid a test that merely feeds the answer to the filter.
- **Success statement:** Lead with task success and rule violations, supported by admission correctness and preservation checks. Keep numerical targets provisional until calibrated, then freeze before final testing.
- **Status cleanup:** Some proposal blockers still say to complete sections already present. Update completion status and verify exports and submission requirements against Canvas.

## Live decision and action log

Suggested note-taker: choose someone before the meeting. Leave faculty decisions blank until stated.

| Decision topic | Professor's guidance / agreed change | Owner | Due |
|---|---|---|---|
| AI Engineering contribution and MVP boundary | Pending | Will | Before Friday submission |
| Data, baselines, primary outcome, and claim limits | Pending | Guadalupe | Before Friday submission |
| Week 5 deliverable and revised timeline | Pending | Bryan | Before Friday submission |
| Other proposal revisions | Pending | Assign in meeting | Before Friday submission |

Close by reading back: “Our understanding is that we will keep ___, defer ___, evaluate against ___, and deliver ___ by Week 5. Before Friday, ___ will update ___.” Record corrections, then update the shared proposal and repository copy consistently.
