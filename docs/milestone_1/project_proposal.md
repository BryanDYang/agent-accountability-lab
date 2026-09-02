# Milestone 1 Project Proposal and Scope

## Visual Context Governance for Reliable Coding Agents

**Course:** CIS-5980

**Track:** AI Engineering

**Team:** Bryan Yang, Will Liu, and Guadalupe Cantera

**Status:** Working submission draft

**Repository:** [agent-accountability-lab](https://github.com/BryanDYang/agent-accountability-lab)

## 1. Project Explanation and Motivation

Coding agents assemble model context from user tasks, target files, repository instructions, company documentation, retrieved files, tool output, and memories from earlier work. These sources can be stale, duplicated, untrusted, mutually inconsistent, or applicable only to a different repository or directory. Retrieval systems usually optimize for relevance, but relevant information is not necessarily current, applicable, or safe. Developers also have limited visibility into this process: they may see the user request and final answer without seeing which context candidates were considered, why a source was removed, how conflicts were handled, or the exact context ultimately sent to the model. That makes context-related failures difficult to explain and governance benefits difficult to demonstrate.

We propose a visual context-governance workbench for coding agents. A user can construct a coding task, add candidate context through drag and drop or controlled fixtures, observe deterministic governance decisions, inspect the exact compiled model input, and compare the same task with and without governance. The application will report context and output tokens, latency, policy violations, task outcomes, and false rejections so token reduction is not mistaken for reliability improvement. This plan combines a working application, deterministic governance policies, controlled coding scenarios, and paired evaluation runs to demonstrate whether the system improves reliability without unacceptable costs.

As an AI Engineering project, the proposal uses the following engineering validation question to connect the system design to measurable success criteria; it is not presented as a separate Research-Driven track requirement:

> Can visible, application-level context governance prevent invalid context from reaching a coding model and improve controlled coding-task outcomes without unacceptable loss of valid context, latency, or token efficiency?

## 2. Project Charter

### Problem statement

Coding agents lack a dependable and observable mechanism for deciding which retrieved instructions, documents, and memories should enter model context. Prompt instructions can ask a model to prefer current or trusted information, but they do not enforce admission before inference or provide a complete record of what was considered and supplied.

### Target users

The primary users are engineers and AI platform owners responsible for coding-agent reliability. They need to understand and control the context supplied to a model before it edits a repository or recommends an action.

### Value proposition

Show developers exactly what context was considered, what governance did to it, what reached the coding model, and how governance changed task quality, token use, and latency.

### End deliverable

The final deliverable will be a locally deployable visual workbench with:

- Task input, target-file selection, model selection, and a configurable token budget
- Drag-and-drop candidate context and reproducible scenario fixtures
- Candidate metadata for provenance, type, scope, authority, trust, validity, and version
- Deterministic admit, reject, quarantine, deduplication, and priority decisions with reason codes
- An ordered preview of the exact governed context and complete model input
- Side-by-side execution of governed and ungoverned versions of the same coding task
- Model output, proposed code changes, automated task checks, and policy-violation results
- Separate input-token, output-token, governance-token, latency, and total-usage reporting
- A provider-neutral model adapter with at least one repeatable local or open-source model
- A reproducible evaluation harness using controlled coding tasks with known ground truth

### User workflow

1. The user enters a coding task and selects the target files or path scope.
2. The user drags in documents, rules, memories, or a prepared scenario fixture.
3. The application extracts content and displays candidate metadata and token counts.
4. The governance pipeline evaluates scope, validity, supersession, trust, conflicts, and duplication.
5. Every candidate remains visible with an admit, reject, quarantine, or deduplicate decision and reason code.
6. The application compiles the approved context within the configured token budget.
7. The user inspects the exact prompt and context that will be sent to the model.
8. The application runs matched governed and ungoverned conditions.
9. The user compares model output, repository changes, tests, violations, tokens, and latency.

## 3. System Architecture

The governance layer is positioned between raw context collection and model inference. The coding agent receives an approved context bundle and does not read the unfiltered candidate pool directly.

```text
User / IDE / Task
        |
        | Task intent, target files, model, token budget
        v
+------------------------------------------------------------------+
| Governance Orchestration Layer                                   |
|                                                                  |
|  1. Ingestion and Extraction                                     |
|     - Document extractor                                         |
|     - Repository rules scanner                                   |
|     - Memory or retrieval adapter                                |
|                         |                                        |
|                         v                                        |
|  2. Deterministic Pre-filter and Hierarchy Policy                |
|     - Path and repository scope                                  |
|     - Validity and supersession                                  |
|     - Authority and trust                                        |
|     - Deduplication and token-budget checks                       |
|                         |                                        |
|                         v                                        |
|  3. Conflict Resolver and Context Compiler                       |
|     - Quarantine unresolved conflicts                            |
|     - Order admitted candidates                                  |
|     - Compile the approved context bundle                        |
+------------------------------------------------------------------+
        |
        | Approved governed context plus decision trace
        v
+------------------------------------------------------------------+
| Coding Model / Agent                                             |
| - Receives only the compiled input for its assigned condition    |
| - Produces output, proposed edits, and tool activity              |
+------------------------------------------------------------------+
        |
        v
Outcome checks, token accounting, latency, and comparison
```

### Component responsibilities

| Component                | Responsibility                                                          | Visible evidence                                                      |
| ------------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Ingestion and extraction | Normalize manually added or retrieved sources into candidate records    | Source, content, version, scope, trust, and raw token count           |
| Deterministic pre-filter | Apply mechanically verifiable policies                                  | Decision, reason code, policy version, and tokens admitted or removed |
| Conflict resolver        | Apply declared precedence and quarantine unresolved high-risk conflicts | Conflicting claims, applied precedence, or quarantine reason          |
| Context compiler         | Order admitted candidates and enforce the context budget                | Exact approved bundle and compiled token count                        |
| Model adapter            | Invoke the selected model through a stable interface                    | Model, parameters, exact request, response, and provider usage        |
| Evaluation runner        | Score matched task executions                                           | Tests, policy checks, latency, token use, and paired differences      |

The first milestone will prioritize deterministic governance. Model-assisted conflict classification is optional and, if used, will be a separately measured branch with its own model identity, input, output, latency, and token cost. The system will not claim to determine the objective truth of arbitrary natural-language statements.

## 4. Application and Interface Design

The interface mirrors the architecture so users can inspect the full path from candidate context to task outcome.

```text
+--------------------------------------------------------------------------+
| Task | Target files | Model | Token budget | Scenario                    |
+----------------------+----------------------+----------------------------+
| Candidate Context    | Governance Trace     | Exact Model Input          |
|                      |                      |                            |
| Drag files here      | ADMIT                | System instructions        |
| Repository rules     | REJECT               | User task                  |
| Documentation        | QUARANTINE           | Approved context           |
| Retrieved memories   | DEDUPLICATE          | Token breakdown            |
| Candidate metadata   | Reason codes         | Ordered payload            |
+----------------------+----------------------+----------------------------+
| Run without governance             | Run with governance              |
+------------------------------------+-------------------------------------+
| Ungoverned output                  | Governed output                   |
| Proposed edits                     | Proposed edits                    |
| Tests and violations               | Tests and violations              |
| Input and output tokens            | Input and output tokens           |
| Latency                            | Governance and total latency      |
+------------------------------------+-------------------------------------+
```

The UI exposes application inputs and outputs, not the model's private reasoning. Provider-reported token usage will be labeled as exact for that request. Tokenizer calculations used before a request will be labeled as estimates.

## 5. Objectives, Experimental Method, and Metrics

### Technical objectives

1. Prevent invalid context from entering model input when invalidity is established by explicit metadata or controlled ground truth.
2. Preserve a trace from every candidate through its governance decision, compiled input, model output, and scored outcome.
3. Make governance behavior understandable through visible reason-coded decisions and exact input inspection.
4. Measure context reduction without hiding false rejection or task-performance costs.
5. Demonstrate paired governed and ungoverned executions through a provider-neutral model interface.

### Compared conditions

Each controlled task will use the same repository revision, request, candidate set, tools, model, parameters, and trial seed when supported.

1. **No governance:** Every retrieved candidate is placed into model context.
2. **Governance enabled:** Deterministic policies filter, deduplicate, scope, order, and reason-code candidates before inference.
3. **Prompt-only governance:** All candidates enter context with instructions to prefer current, applicable, and trusted information. This is an experimental baseline and does not need to dominate the live demonstration.

The two primary modes in the workbench will be no governance and governance enabled.

### Initial scenarios

- A superseded instruction conflicts with current repository configuration.
- A directory-scoped rule is retrieved for the wrong target path.
- Untrusted repository or issue content attempts to become an authoritative instruction.
- A stale handoff memory names an obsolete architecture or test command.
- Duplicate guidance consumes tokens without adding information.
- A clean control contains only valid, applicable context.

Each scenario will define candidate labels, expected governance decisions, allowed context, expected coding or tool outcome, and machine-checkable tests before model trials begin.

### Success metrics

Detailed formulas, statistical methods, and threshold calibration are deferred to the [Milestone 2 Evaluation Plan](../milestone_2/evaluation_plan.md). For Milestone 1, the metric identities and purposes below define the proposed evaluation direction.

| Metric                         | What it establishes                                                                      |
| ------------------------------ | ---------------------------------------------------------------------------------------- |
| Invalid-context admission rate | Whether governance prevents known-invalid candidates from reaching the model             |
| False-rejection rate           | Whether governance incorrectly removes valid candidates                                  |
| Task-success rate              | Whether the coding task passes its required tests and policy checks                      |
| Repository-rule violation rate | Whether model output violates the active scenario rule                                   |
| Input context tokens           | How much context each condition supplies to the task model                               |
| Output tokens                  | Whether output length or behavior changes materially                                     |
| Governance-model tokens        | Any tokens consumed by optional model-assisted governance                                |
| Governance and total latency   | The preprocessing cost and full user-visible runtime                                     |
| Decision clarity               | Whether an evaluator can correctly explain a governance decision from the UI             |
| Trace completeness             | Whether all required candidate, decision, input, model, and outcome evidence is recorded |

Token reduction alone will not count as success. It must be interpreted alongside task success, policy violations, and false rejection. Numeric targets remain provisional until a pilot establishes reasonable effect sizes and variance.

### Model strategy

- Use one inexpensive local or open-source model for repeatable demonstrations and most experimental runs.
- Use one stronger coding model, potentially Codex, for a limited external-validity comparison if access and course constraints permit.
- Compare governance conditions within the same model. Results across different models will be reported separately and will not be attributed to governance.
- Record the exact model identifier, configuration, tokenizer or usage source, and software version for every evaluated run.

## 6. Feasibility, Constraints, Ethics, and Safety

### Preliminary implementation choices

- **Front end:** React and TypeScript with Vite for a local visual workbench; semantic HTML and accessible interactions remain requirements regardless of framework.
- **Back end:** Python 3.12 with FastAPI for task setup, deterministic governance, model invocation, and evaluation endpoints.
- **Storage:** SQLite for local tasks, candidates, decisions, exact model requests, and outcomes; content hashes link immutable evidence records without requiring production infrastructure.
- **Model integration:** A thin provider-neutral adapter with an OpenAI-compatible request contract; the first local or open-source model and runtime will be selected in Milestone 2. <- too fuzzy
- **Evaluation:** Pytest for scenario, policy, schema, and metric checks; Playwright for the narrow end-to-end workbench flow; controlled JSON fixtures define expected decisions and outcomes. <- word it more detail how we'll address this in phase 2
- **Design framework:** The current dependency-free HTML  in mockup and Draw.io architecture remain the low-fidelity design sources; implementation styling will use CSS custom properties and a small project-owned component vocabulary before considering a larger UI library.
- **Distribution:** Reproducible local setup first, with container packaging as a release goal.

Final framework commitments will be made after a narrow end-to-end prototype validates the interaction and model path.

All choices are provisional. Milestone 1 establishes a credible implementation direction rather than locking the team into frameworks before the first vertical prototype.

### Rough compute and tooling budget

The initial plan assumes each team member can use a modern development laptop. The minimum local-model target is a machine with 16 GB of memory and approximately 20 GB of free storage for a quantized model, dependencies, fixtures, and run artifacts. If available hardware cannot run the selected model reliably, the team will use a bounded hosted-model path through the same adapter rather than changing the experiment design.

The first evaluation estimate is 60 task-model runs: five adversarial scenario classes plus one clean control, two primary conditions, and five repeated trials per scenario-condition pair. Pilot results may change the repetition count before the final evaluation. Governance runs, failed setup attempts, and optional comparison-model runs will be reported separately rather than hidden inside the task-model total.

| Budget item                                          |                                                                Provisional limit |
| ---------------------------------------------------- | -------------------------------------------------------------------------------: |
| Open-source development tools and repository hosting |                                                                               $0 |
| Local model execution                                |                         Existing team hardware; no new hardware purchase assumed |
| Hosted model API usage                               |            $50 total project cap unless the team approves a documented exception |
| Optional deployment                                  | $0 preferred; no more than $20 total for a short-lived demonstration environment |
| Storage                                              |                   Local SQLite and repository fixtures; no paid database assumed |

### Data and licensing plan

- **Fixture sources:** Use team-authored synthetic repositories, tasks, rules, documents, memories, and expected outcomes. Public examples may be adapted only when their licenses permit redistribution and attribution requirements are satisfied.
- **Access and ownership:** Store approved fixtures in the project repository so every team member can inspect and reproduce them. Record the author or upstream source for every fixture.
- **Permitted use:** Use fixtures only for course development, evaluation, demonstration, and publication under the repository's declared license. Do not imply that synthetic results represent production organizations or users.
- **Private-data exclusions:** Do not use employer code, customer data, private chats, credentials, proprietary documentation, student records, or other personal information. Replace realistic identifiers with synthetic values before committing artifacts.
- **Third-party tracking:** Maintain a source and license inventory for dependencies, model weights or APIs, public datasets, icons, fonts, and adapted fixture material before the first fixture set is frozen.
- **Model terms:** Record model name, version, provider, license or terms of use, access date, and redistribution restrictions for every evaluated model.

### Ethics and safety plan

- **Privacy:** Use synthetic tasks and disposable repositories. Inspect committed fixtures for secrets and personal information before release.
- **Representativeness and bias:** The controlled scenario suite will cover specific context failures, not the full range of repositories, languages, organizations, or developers. Results will be reported per scenario and will not be generalized beyond the tested conditions.
- **Misuse:** The workbench is intended for defensive evaluation and debugging. It will not include credential harvesting, persistence, exploitation, or deployment against third-party repositories.
- **Harmful code output:** Run generated edits and commands only in disposable evaluation repositories with restricted tools. Do not connect the coding runner to production systems or real credentials.
- **Credential exposure:** Exclude secrets from fixtures, redact sensitive values from visible traces, and prevent model tools from receiving ambient credentials that are unnecessary for the task.
- **Governance limits:** Do not claim that the system determines objective truth or reveals private model reasoning. Quarantine unresolved high-risk conflicts and distinguish delivered instructions from observed agent compliance.
- **Release safeguards:** Review fixture licenses, scan published artifacts, document known limitations, and require all automated tests and policy checks to pass before the demonstration release.

### Constraints and boundaries

- Use synthetic or purpose-built repositories and context fixtures.
- Do not include private code, customer data, credentials, or personal information.
- Record model, dataset, dependency, and public fixture licenses before publication.
- Do not claim that rejected context caused a model's private reasoning.
- Do not claim that the system establishes objective truth.
- Quarantine unresolved high-risk conflicts rather than silently choosing a source.
- Keep coding tools restricted to disposable evaluation repositories.

### Principal risks and mitigations

| Risk                                                                   | Mitigation                                                                                                                  |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Natural-language conflict resolution becomes open-ended truth judgment | Limit required decisions to explicit metadata, declared supersession, controlled ground truth, and deterministic predicates |
| Token savings remove necessary information                             | Measure false rejection, clean-control performance, and task success alongside tokens                                       |
| Model stochasticity obscures governance effects                        | Use paired inputs, fixed settings, repeated trials, and per-scenario reporting                                              |
| Model-assisted governance hides its own cost                           | Report its model, tokens, latency, and output separately                                                                    |
| The UI becomes a general prompt builder                                | Keep every interaction tied to governance decisions and controlled outcome comparison                                       |
| Integration work overwhelms the project                                | Support one controlled coding runner and a narrow model adapter before adding integrations                                  |

## 7. MVP Scope

### Included

- Visual task setup with target-file scope and token budget
- Drag-and-drop candidate context and prepared fixtures
- Structured candidate metadata and token estimates
- Deterministic governance with stable reason codes
- Visible candidate decisions and conflict quarantine
- Exact approved-context and model-input preview
- Governed and ungoverned execution using the same model configuration
- Side-by-side outputs, proposed edits, tests, violations, tokens, and latency
- One local or open-source model integration
- At least five adversarial scenario classes plus clean controls
- Automated scenario, policy, schema, integration, and metric tests
- Reproducible local setup, documentation, final report, and live demonstration

### Stretch goals

- Prompt-only governance as an interactive third mode
- A stronger hosted coding-model comparison
- Automatic context retrieval based on the task prompt
- Post-incident source correction and deterministic replay
- Blast-radius analysis across stored tasks
- Model-assisted classification for quarantined conflicts

### Explicitly out of scope

- Automatic truth verification for arbitrary natural-language content
- Custom model training or fine-tuning
- A general enterprise agent control plane
- Support for every model provider, coding agent, repository host, or language
- Production multi-tenancy, billing, identity, or marketplace distribution
- Human approval for every candidate or coding task
- Claims about model consciousness, hidden reasoning, or causal attribution from prompt traces alone

## 8. Roles and Timeline

Detailed ownership must be confirmed by all three team members. Proposed workstreams are:

| Workstream                  | Primary responsibilities                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------ |
| Governance and evaluation   | Candidate contracts, deterministic policies, reason codes, metrics, and experimental controls    |
| Application and integration | Workbench UI, context inspection, model adapter, task runner, and side-by-side execution         |
| Fixtures and communication  | Synthetic repositories, scenario ground truth, automated checks, documentation, and presentation |

### Full-course timeline

| Period        | Checkpoint and output                                                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| End of Week 1 | Confirm fixture access, ownership, permitted use, private-data exclusions, and license-inventory responsibilities before approving any evaluation source |
| Weeks 1-2     | Finalize the workbench proposal, architecture, roles, evaluation claims, and pitch artifact                                                              |
| Weeks 3-5     | Prototype task input, candidate loading, exact model-input preview, and one ungoverned coding run                                                        |
| Weeks 6-8     | Implement deterministic governance, reason codes, token accounting, and the governed run                                                                 |
| Weeks 9-10    | Complete side-by-side comparison, automated checks, clean controls, and scenario fixtures                                                                |
| Weeks 11-12   | Run paired evaluations and analyze reliability, false rejection, latency, tokens, and failures                                                           |
| Weeks 13-14   | Freeze the release, reproduce from a clean setup, complete the report, and prepare the demonstration                                                     |

## 9. Repository Status and Next Steps

The repository is intentionally planning-focused. It currently contains the active proposal, metric appendix, historical planning archive, course reference materials, and project governance documents. Earlier implementation scaffolding was removed because it represented a superseded project direction.

### Current blockers

- Verify the final submission package against the official Canvas instructions and grading rubric.
- Confirm team roles and ownership.
- Complete the preliminary technology, budget, data, licensing, ethics, and safety sections.
- Complete the required pitch artifact and final PDF.

### Next steps

1. Verify the Milestone 1 checklist against the official course rubric.
2. Review and approve this proposal as the Milestone 1 source of truth.
3. Confirm team roles and preliminary technology choices.
4. Complete the budget, data, licensing, ethics, safety, and timeline sections.
5. Create the required pitch artifact.
6. Assemble and verify the final PDF for submission.

Project-readiness decisions, repository setup, implementation, pilot runs, final metric thresholds, and optional comparison-model work are tracked in the [Milestone 2 TODO](../milestone_2/TODO.md).

## 10. Requested Teaching-Staff Feedback

The team requests feedback on:

- Whether a visual coding-agent context-governance workbench is sufficiently differentiated and appropriately scoped
- Whether paired governed and ungoverned executions support the proposed reliability claims
- Whether prompt-only governance should remain a required experimental condition
- Whether deterministic metadata-driven governance is an acceptable boundary for the MVP
- Whether one open-source model plus a limited stronger-model comparison provides adequate implementation depth
- Whether the proposed task, safety, token, latency, and false-rejection metrics are sufficient

## 11. Milestone 1 Submission Checklist

The following items are the proposed submission checklist. The team must verify them against the official Canvas instructions and grading rubric before treating the list as authoritative. 

### Proposal and planning -> convert the milestone 1 deliverable draft to google doc

- [X] Consolidate the project explanation and motivation into the two-paragraph format named in the grading rubric.
- [X] Add a weekly check-in with progress made, top blockers or risks, and planned next steps. -> @weekly_journal.md
- [X] Assign Bryan, Will, and Guadalupe as owners for the proposed workstreams and next-milestone tasks. -> General milestone by milestone via task -> Will: arch + checklist items Guadalupe: ideas + qa/qc + checklist items Bryan: repo setup + checklist items
- [ ] Name the preliminary front-end, back-end, storage, model-integration, evaluation, and design-framework choices, even if they remain provisional. <- bryan
- [ ] State a rough compute and tooling budget, including local hardware assumptions, expected evaluation volume, API spending limit, and deployment cost assumptions. <- Guadalupe
- [ ] Add a dedicated data and licensing plan covering fixture sources, access, ownership, permitted use, private-data exclusions, and third-party license tracking. <- Will
- [ ] Add a dedicated ethics and safety plan covering privacy, representativeness or bias, misuse, harmful code output, credential exposure, and concrete safeguards.  <- Guadalupe
- [ ] Add an explicit early timeline checkpoint for data or fixture access and licensing review. <- MIT (research Bryan)

### Submission artifacts

- [ ] Draft a pitch deck with six slides or fewer, or a three-to-five-minute concept video. <- Bryan draft and put it in the google doc
- [ ] Export the pitch deck or concept video and visually verify the final artifact. <- group
- [ ] Assemble the required components into a single PDF and verify the final export against Canvas instructions. <- group
