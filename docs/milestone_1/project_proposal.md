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
- **Model integration:** Use Qwen2.5-Coder 7B Instruct as the first repeatable local coding model, served through Ollama's OpenAI-compatible endpoint. The application will call it through a provider-neutral adapter that records the model tag, runtime version, request parameters, exact messages, response, latency, and token counts for every run. Phase 2 will first prove one complete local run through this adapter before adding an optional hosted comparison model.
- **Evaluation:** In Phase 2, define a versioned JSON fixture schema containing the task, disposable repository revision, target paths, candidate context and metadata, expected governance decisions, active repository rules, and machine-checkable task outcomes. Pytest will validate the schema and deterministic policies, materialize each disposable repository, run matched governed and ungoverned conditions with the same model settings, execute task tests and static policy assertions, and write one trace and metric record per run. Playwright will exercise the user-visible path from loading a fixture through inspecting decisions and exact model input to launching both conditions and comparing their results. The first Phase 2 checkpoint is one end-to-end scenario whose UI results, saved trace, and Pytest outcome agree before the team expands the fixture suite.
- **Design framework:** The current dependency-free HTML  in mockup and Draw.io architecture remain the low-fidelity design sources; implementation styling will use CSS custom properties and a small project-owned component vocabulary before considering a larger UI library.
- **Distribution:** Reproducible local setup first, with container packaging as a release goal.

Final framework commitments will be made after a narrow end-to-end prototype validates the interaction and model path.

All choices are provisional. Milestone 1 establishes a credible implementation direction rather than locking the team into frameworks before the first vertical prototype.

### Rough compute and tooling budget

The project is designed to rely primarily on existing team hardware and free, open-source development tools. The team assumes each member has access to a modern development laptop with at least 16 GB of memory, enough to run the quantized local coding model that receives governed or ungoverned context and produces the code edit under evaluation. The laptop also needs approximately 25 GB of free storage for the downloaded model, Python and Node dependencies, Playwright's browser binary, team-authored fixtures, and recorded governance decisions and model outputs. No new hardware purchases are planned.

Qwen2.5-Coder 7B Instruct served through Ollama is the initial baseline selected in the model-integration plan above. The hardware envelope also leaves room to evaluate a larger quantized model if the team chooses to do so: Ollama lists the 4-bit Qwen2.5-Coder 14B artifact at roughly 9 GB, while OpenAI describes gpt-oss-20b as capable of running within 16 GB of memory. These are feasibility examples, not additional model commitments. Phase 2 will confirm actual memory, storage, latency, and stability on available team hardware. If the baseline cannot run reliably, the team will use limited hosted inference through the same provider-neutral adapter.

For the initial pilot, the team estimates approximately 36 primary task-model runs. This comes from six scenario classes, including five adversarial scenarios and one clean control, two primary conditions, and three repeated trials for each scenario-condition pair. Three trials are an initial planning estimate rather than a statistically derived requirement because the system does not yet have an effect-size or variance estimate. Pilot results will determine whether the final evaluation requires additional repetitions. Governance runs, failed setup attempts, and optional comparison-model runs will be reported separately rather than hidden inside the task-model total.

Most evaluation runs are expected to use the local model, keeping inference costs near zero. Hosted-model usage will be limited primarily to development needs and an optional stronger-model comparison. Based on provider pricing reviewed in September 2026, a 36-run pilot is expected to cost only a few dollars under ordinary prompt and response sizes, but actual cost will depend on measured token usage. The team will use a $20 total API spending cap unless additional spending is explicitly approved. The application is intended to run locally, so deployment cost is expected to remain $0 on a free hosting tier, with up to $10 reserved for a short-lived demonstration environment if needed.

| Budget item                                          | Provisional limit                                                                                   |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Open-source development tools and repository hosting | $0                                                                                                  |
| Local model execution                                | Existing team hardware; no new hardware purchase assumed                                            |
| Hosted model API usage                               | $20 total project cap unless the team approves a documented exception                               |
| Optional deployment                                  | $0 preferred using a free hosting tier; up to $10 total for a short-lived demonstration environment |
| Storage                                              | Local SQLite and repository fixtures; no paid database assumed                                      |

Pricing and hardware figures reflect research conducted in September 2026 and will be reverified before final Milestone 2 threshold calibration because API and hosting prices can change. Sources: [Claude Platform Pricing](https://platform.claude.com/docs/en/about-claude/pricing), [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing), [Qwen2.5-Coder 14B on Ollama](https://ollama.com/library/qwen2.5-coder:14b), and [Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/).

### Data and licensing plan

1. **Fixture sources and origin:** All project fixtures shall consist primarily of team-authored synthetic repositories, tasks, operational rules, synthetic documents, agent memories, and expected evaluation outcomes. Public or third-party examples may be incorporated only when their explicit licenses permit redistribution and modification and all upstream copyright, attribution, and license-notice obligations have been satisfied before adoption.
2. **Access, storage, and ownership:** All validated and approved fixtures must be stored directly within the project repository so every team member can independently review, inspect, and reproduce evaluation results. Each fixture commit must include formal provenance metadata recording the author and creation date or the corresponding upstream source.
3. **Permitted scope of use and disclaimers:** Fixtures and derived assets covered under this plan are authorized exclusively for course development, systematic evaluation, academic demonstrations, and publication in accordance with the repository's declared open or proprietary license. Synthetic results, test cases, and simulated user behaviors must not be marketed, represented, or construed as reflective of actual production organizations, commercial systems, or real individuals.
4. **Exclusion of private and proprietary data:** Employer codebases, proprietary enterprise documentation, customer data, internal communications, authentication credentials, student records, and personally identifiable information are strictly forbidden. Contributors must sanitize all artifacts and replace realistic names, domains, and identifiers with verified synthetic placeholders before committing files to the repository.
5. **Third-party tracking and inventory management:** Before freezing any benchmark or fixture release, the project team must compile and maintain a centralized third-party asset inventory. The registry must account for all external software dependencies, public datasets, model weights, third-party APIs, icons, fonts, and adapted reference materials, identifying the exact source URL, active license terms, and required attribution statements.
6. **Model terms and evaluation governance:** Every foundation or fine-tuned model evaluated within this initiative must be logged with complete compliance metadata. The record must detail the model name, exact version tag, provider or hosting vendor, governing license or terms of service, access date, and any known restrictions on commercial reuse, output redistribution, or derivative works.

### Ethics and safety plan

- **Privacy:** Development and evaluation will use synthetic, purpose-built, or licensed public repositories, coding tasks, and context fixtures, per the data and licensing plan above. Fixtures will not include employer or customer code, private communications, student records, personal information, or other proprietary data. Because the workbench records candidate context and model-input traces, only information necessary for the controlled experiment will be stored, and the evidence store will stay local to each team member's machine rather than shared or hosted.
- **Representativeness and bias:** The evaluation scenarios are designed to test specific context-governance failures: a superseded instruction that conflicts with current configuration, a rule retrieved for the wrong path scope, untrusted content attempting to become an authoritative instruction, a stale handoff memory naming an obsolete command, and duplicate guidance. These scenarios will not represent every repository, programming language, organization, or type of coding-agent failure. Results will therefore be reported by scenario and will not be generalized beyond the conditions tested.
- **Misuse:** The workbench is intended as a defensive tool for evaluating and debugging coding-agent context. It will not be presented as a general security system or a mechanism for determining whether arbitrary information is objectively true. Evaluation scenarios will not involve credential theft, persistence, exploitation, or attacks against third-party systems.
- **Harmful code output:** Model-generated code and commands will be treated as untrusted until evaluated. Generated changes will run only inside disposable evaluation repositories with a restricted toolset: file edits and test execution inside the evaluation repository, no network access, no arbitrary package installation, and no shell command outside an explicit allow-list. Generated changes will be checked using the scenario's automated tests and policy checks, and the coding runner will not be connected to production repositories or systems.
- **Credential exposure:** API keys, access tokens, passwords, and other secrets will be kept out of context fixtures, model prompts, stored traces, and committed repository files. Credentials required to access a model will be provided through local configuration or environment variables, not committed files, and will not be intentionally exposed to the coding model unless a task strictly requires them. Because the exact model-input preview shows the compiled context directly, redaction will happen before context compilation rather than only at display time, so a secret cannot be hidden from the trace view while still reaching that preview.
- **Governance safeguards:** Governance decisions will rely on explicit information available to the system, such as scope, provenance, version, trust metadata, declared precedence, and controlled scenario ground truth, not on judging whether arbitrary content is true. When deterministic rules cannot safely resolve a high-risk conflict, the context will be quarantined rather than automatically accepted or rejected. Each governance decision will include a visible reason code, and users will be able to inspect the exact context ultimately supplied to the model; that trace will record what was delivered to the model, not what the model privately reasoned about it.
- **Release safeguards:** Before the final demonstration, review committed fixtures and generated artifacts for accidentally exposed credentials or private information, verify applicable licenses, and run the project's automated scenario, policy, and integration checks. Known limitations of the governance rules and evaluation scenarios will also be documented rather than presenting the system as a complete solution to coding-agent safety.

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

The team assigns one primary owner to each workstream while retaining shared review responsibility for architecture, evaluation claims, safety decisions, and submission artifacts.

| Team member       | Primary workstream                | Responsibilities                                                                                                                     |
| ----------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Will Liu          | Architecture and governance       | System architecture, candidate contracts, deterministic policies, precedence rules, reason codes, and assigned proposal requirements |
| Bryan Yang        | Application and model integration | Repository setup, workbench UI, context inspection, model adapter, task runner, side-by-side execution, and pitch-deck draft         |
| Guadalupe Cantera | Evaluation, fixtures, and quality | Scenario ideas, synthetic fixtures, ground truth, automated checks, evaluation review, QA/QC, and assigned proposal requirements     |

### Next-milestone ownership

| Milestone 2 task                                                       | Primary owner     | Review or support   |
| ---------------------------------------------------------------------- | ----------------- | ------------------- |
| Freeze the architecture, candidate schema, and governance reason codes | Will Liu          | Bryan and Guadalupe |
| Build the first UI-to-model vertical slice and local-model adapter     | Bryan Yang        | Will                |
| Define the initial fixtures, expected outcomes, and evaluation rubric  | Guadalupe Cantera | Will and Bryan      |
| Implement policy, schema, task-outcome, and trace-consistency tests    | Guadalupe Cantera | Bryan               |
| Maintain repository setup, continuous integration, and developer setup | Bryan Yang        | Will                |
| Review pilot evidence and approve final thresholds                     | Guadalupe Cantera | Will and Bryan      |
| Maintain milestone documentation and prepare the checkpoint update     | Bryan Yang        | Will and Guadalupe  |

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
- Complete the preliminary technology, budget, data, licensing, ethics, and safety sections.
- Complete the required pitch artifact and final PDF.

### Next steps

1. Verify the Milestone 1 checklist against the official course rubric.
2. Review and approve this proposal as the Milestone 1 source of truth.
3. Confirm the preliminary technology choices with the assigned workstream owners.
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
- [X] Assign Bryan, Will, and Guadalupe as owners for the proposed workstreams and next-milestone tasks. Completed in Roles and Timeline.
- [X] Name the preliminary front-end, back-end, storage, model-integration, evaluation, and design-framework choices, even if they remain provisional. Owner: Bryan. Completed in Preliminary implementation choices.
- [X] State a rough compute and tooling budget, including local hardware assumptions, expected evaluation volume, API spending limit, and deployment cost assumptions. Owner: Guadalupe. Completed in Rough compute and tooling budget.
- [X] Add a dedicated data and licensing plan covering fixture sources, access, ownership, permitted use, private-data exclusions, and third-party license tracking. Owner: Will. Completed in Data and licensing plan.
- [X] Add a dedicated ethics and safety plan covering privacy, representativeness or bias, misuse, harmful code output, credential exposure, and concrete safeguards. Owner: Guadalupe. Completed in Ethics and safety plan.
- [X] Add an explicit early timeline checkpoint to confirm fixture access, ownership, permitted use, private-data exclusions, and license-inventory responsibilities before evaluation fixtures are frozen. Owner: Bryan researches; group reviews. Completed in the Full-course timeline.

### Submission artifacts

- [X] Draft a pitch deck with six slides or fewer. Owner: Bryan. Completed in `docs/milestone_1/pitch_deck.md`.
- [ ] Export the pitch deck, visually verify the final artifact, and import it into Google Slides. Owner: group.
- [ ] Assemble the required components into a single PDF and verify the final export against Canvas instructions. Owner: group.
