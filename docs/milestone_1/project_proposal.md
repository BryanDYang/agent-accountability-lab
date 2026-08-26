# Milestone 1 Project Proposal and Scope

## Agent Context Governance for Reliable Coding Agents

**Course:** CIS-5980
**Track:** AI Engineering
**Team:** Bryan Yang, Will Liu, & Guadalupe Cantera
**Status:** Working submission draft
**Repository:** [https://github.com/BryanDYang/agent-accountability-lab](https://github.com/BryanDYang/agent-accountability-lab)

## 1. Project Explanation and Motivation

Coding agents assemble context from repository instruction files, company documentation, retrieved files, issue text, tool output, and memories left by previous agents. These sources can become stale, conflict with one another, apply only to a different directory or repository, or contain untrusted instructions. Retrieval systems usually optimize for relevance, but relevant information is not necessarily current, applicable, or safe. When invalid context reaches the model, the agent can edit the wrong file, follow an obsolete command, violate repository policy, or waste tokens on duplicate guidance. Developers then have little evidence showing which source affected the task or how to prevent the same failure from recurring.

We propose a provider-neutral governance layer between context retrieval and model inference. It will record provenance and scope for each candidate, apply deterministic rules for validity, supersession, authority, trust, and duplication, and assemble the smallest approved context bundle for the task. A local investigation interface will show why candidates were admitted, rejected, or quarantined and will support correction and replay of failed tasks. The capstone will compare relevance-only retrieval, prompt-only guidance, and runtime enforcement on controlled coding tasks with known ground truth. Success will be measured through task completion, invalid-context admission, rule violations, replay correction, regressions, latency, and token use.

## 2. Project Charter

### Problem statement

Coding agents lack a dependable mechanism for deciding whether retrieved instructions and memories should be allowed into model context. Existing prompts can tell a model to prefer current or trusted information, but they do not enforce admission, remove superseded context, preserve a decision trace, or verify a correction through replay.

### Target users and context

The primary users are engineers and AI platform owners responsible for coding-agent reliability across one or more repositories. In the target workflow, a developer asks an agent to modify a repository. Before the model call, the proposed layer evaluates candidate instructions, documentation, retrieved files, and prior memories against the active repository, directory, file, and task scope.

### Value proposition

Give coding agents the smallest trustworthy context needed for a task, explain why each source was included or excluded, and measure the resulting reliability, token, and latency impact.

Success should feel like ordinary software debugging: an engineer can identify the context behind a bad change, correct or supersede the source once, find other exposed tasks, and replay affected cases to verify the fix.

### End deliverable

The final deliverable will be a locally deployable developer toolkit with:

- A Python SDK that accepts candidate context and returns an approved context bundle with reason-coded decisions
- SQLite persistence for candidates, versions, tasks, decisions, outputs, corrections, and replay records
- Deterministic governance for scope, validity, supersession, authority, trust, conflicts, and duplication
- A provider-neutral interface with one working coding-agent or controlled coding-task integration
- A lightweight investigation and replay interface
- Synthetic repository fixtures containing seeded context failures and machine-checkable outcomes
- A reproducible evaluation harness comparing three context-handling conditions
- Containerized local setup, tests, documentation, a final report, and a live demonstration

### User workflow

1. A developer starts a coding task against a known repository revision.
2. The agent integration retrieves candidate context.
3. The governance layer records provenance, scope, validity, authority, trust, and version relationships.
4. Deterministic policies admit, reject, quarantine, deduplicate, or prioritize each candidate.
5. The coding agent receives only the approved context bundle.
6. The system links the bundle to the model configuration, code change, tool activity, test outcome, latency, and token counts.
7. An engineer inspects a failure, corrects or supersedes a source, and replays affected tasks.

## 3. Objectives, Methods, and Success Metrics

### Technical objectives

1. Prevent invalid context from reaching a coding agent when the invalidity is established by explicit metadata or controlled scenario ground truth.
2. Preserve a complete trace from candidate source through governance decision, approved bundle, agent output, repository change, and evaluation outcome.
3. Make corrections testable by replaying the same task and comparing the original and corrected results.
4. Reduce unnecessary context without hiding the reliability cost of governance.
5. Demonstrate a provider-neutral design with stable, versioned contracts.

### Experimental method

Each controlled task will use the same repository revision, user request, candidate set, tools, and model configuration across three conditions:

1. **Relevance-only retrieval:** All retrieved candidates enter model context.
2. **Prompt-only governance:** All candidates enter context with instructions telling the model to prefer current, applicable, and trusted information.
3. **Runtime enforcement:** Invalid or duplicate candidates are rejected or quarantined before model inference.

The initial scenario suite will include:

- A superseded root instruction that conflicts with current repository configuration
- A directory-scoped rule retrieved for the wrong service or language
- Untrusted repository or issue content attempting to become an authoritative instruction
- A stale handoff memory describing an obsolete architecture or test command
- Duplicate guidance that increases token use without adding information

Each scenario will define expected governance decisions, the allowed context set, the expected code or tool outcome, and automated checks before experiments run. Repository tests, lint rules, static assertions, and explicit policy checks will score outcomes. Live-model trials will be repeated under fixed settings where stochastic behavior matters; deterministic or recorded responses will validate storage, policy, trace, and replay behavior.

### Success metrics

The proposed notation, equations, measurement policies, thresholds, and open decisions are documented for group review in [Milestone 1 Success Metrics: Group Review Draft](success_metrics_math.md). The table below remains preliminary until that review is complete.

| Metric                         | Definition                                                                                  | Preliminary success target                                                                           |
| ------------------------------ | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Invalid-context admission rate | Invalid candidates included in the model bundle divided by all invalid candidates retrieved | At least 80% lower than relevance-only retrieval                                                     |
| Repository-rule violation rate | Tasks whose output violates the active scenario rule                                        | At least 50% lower than relevance-only retrieval                                                     |
| Task-success rate              | Tasks passing scenario tests and required policy checks                                     | Improve over relevance-only retrieval without losing more than 5 percentage points on clean controls |
| Correction success rate        | Seeded failures resolved after source correction and replay                                 | 100% across the required scenario classes                                                            |
| Regression rate                | Previously correct clean-control tasks made incorrect after correction                      | No more than 5%                                                                                      |
| False-rejection rate           | Valid candidates incorrectly rejected                                                       | No more than 5% in controlled fixtures                                                               |
| Human-review rate              | Tasks requiring quarantine or operator review                                               | Reported separately; not used to hide failures                                                       |
| Trace completeness             | Required provenance, decision, bundle, model, revision, and outcome fields recorded         | 100% for evaluated tasks                                                                             |
| Governance latency             | Time added before the model call                                                            | p95 below 100 ms for deterministic checks on the evaluation machine                                  |
| Net context tokens             | Approved-context tokens plus any governance-model tokens minus baseline context tokens      | Median no greater than baseline, with all components reported                                        |
| Incident diagnosis time        | Time required to identify the invalid source in a seeded failure                            | Median below 3 minutes using the investigation interface                                             |
| Decision clarity               | Evaluator correctly identifies why a candidate was admitted, rejected, or quarantined       | At least 90% accuracy on a short scenario review task                                                |

Numeric targets are preliminary and will be revisited after the first pilot, but any change will be documented before the final experiment suite is run.

## 4. Feasibility, Constraints, Ethics, and Safety

### Technology stack and preliminary design framework

- **Core and backend:** Python 3.11+, Pydantic or dataclasses, SQLite, and JSONL evidence export
- **Service boundary:** FastAPI only where it simplifies the integration or user interface
- **User interface:** Streamlit or a small web interface for trace inspection and replay comparison
- **Agent integration:** Provider-neutral adapter with one required model-provider implementation
- **Evaluation:** Pytest, Ruff, mypy, Pandas, and Matplotlib
- **Packaging:** Docker for the release candidate and one-command local setup
- **Interface design:** A compact inspection-first layout that prioritizes task history, candidate decisions, reason codes, original-versus-replay comparison, and accessible status labels

### Data and licensing constraints

The project will use synthetic or purpose-built repositories, tasks, instruction files, memories, and expected outcomes. No private company code, customer records, credentials, or personal information will be included. Public dependencies, models, and any reused repository content will be recorded with their licenses and terms before publication.

Preliminary licensing audit:

| Resource                                    | Expected license or terms                                    | Constraint and action                                                         |
| ------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Team-authored synthetic repository fixtures | Team-owned and released under the repository's MIT license   | Avoid copying private or restrictively licensed code into fixtures            |
| Public repository fixtures, if used         | MIT or Apache 2.0 only unless separately reviewed            | Preserve notices and attribution; record revision and license                 |
| First hosted model API, to be selected      | Provider terms of use and data-processing terms              | Verify logging, retention, evaluation, and publication permissions before use |
| Local fallback model, if required           | Prefer Apache 2.0 or another commercially permissive license | Record model card, version, license, and redistribution restrictions          |

### Compute budget and tooling

Development and deterministic evaluation will run on team laptops and GitHub Actions. SQLite and local fixtures avoid hosted database cost. Before repeated live-model experiments, the team will run a pilot to estimate tokens and cost per case. The preliminary API budget cap is **$50 total for the team**, with cached or recorded outputs used only where they do not invalidate the comparison. If projected cost exceeds the cap, secondary repetitions will use a smaller or local model while one provider remains the required end-to-end integration.

### Principal risks and mitigations

| Risk                                                              | Mitigation                                                                                          | Fallback                                                             |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Natural-language conflicts become open-ended truth judgments      | Use explicit metadata, declared supersession, controlled ground truth, and deterministic predicates | Limit claims to conflicts that the system can verify mechanically    |
| Coding outcomes are difficult to score                            | Design tasks with tests, lint, static assertions, and explicit rule checks                          | Use a documented human rubric only for residual qualitative outcomes |
| Governance saves context tokens but spends more on classification | Prefer deterministic checks and account separately for every governance token                       | Restrict model-assisted classification to quarantined cases          |
| Model stochasticity obscures policy effects                       | Hold inputs and configurations constant and repeat selected trials                                  | Use scripted or recorded responses for system-correctness tests      |
| Integration work consumes the schedule                            | Support one controlled runner and at most one real agent integration                                | Demonstrate neutrality through stable adapter contracts              |
| Ambiguous source precedence causes unsafe decisions               | Define a small explicit precedence policy and expose unresolved conflicts                           | Quarantine ambiguous high-risk cases                                 |

### Ethics and safety plan

| Harm or misuse scenario                                           | Guardrail                                                                                                                         | Test                                                                                                                                  |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Prompt injection in repository, issue, or retrieved content       | Mark retrieved content untrusted by default and prevent it from gaining instruction authority without explicit policy             | Run a red-team fixture set containing direct, indirect, encoded, and cross-file instruction attempts; report invalid-admission rate   |
| Cross-repository or cross-directory leakage                       | Require explicit scope checks before admission and fail closed on missing high-risk scope                                         | Run paired fixtures across repositories, services, and directories; assert that no out-of-scope candidate enters the bundle           |
| Incorrect code or destructive tool action caused by stale context | Reject expired or superseded sources, restrict demo tools to disposable repositories, and require tests before accepting outcomes | Seed stale commands and policies; verify rejection, run the task in an isolated fixture, and record rule violations and test outcomes |

- **Privacy:** Use synthetic or public content, scan fixtures and traces for secrets, minimize logged prompt content, and retain evaluated artifacts only for the course and reproducibility needs.
- **Fairness and coverage:** The principal disparity risk is uneven performance across programming languages, repository structures, and instruction-writing styles rather than demographic groups. The evaluation will report results separately for at least two language or project structures and will not claim generality beyond tested groups.
- **Transparency:** Record repository revision, model, prompt, policy, schema, candidates, decisions, and configuration for every evaluated task.
- **Human oversight:** Quarantine unresolved high-risk conflicts and measure the resulting review burden.
- **Limitations:** State that the MVP enforces supplied metadata and controlled policies; it does not establish objective truth or authenticate every source.
- **Balanced reporting:** Report false rejections, regressions, quarantines, latency, and token cost alongside improvements.

## 5. Scope, Roles, and Timeline

### Included in scope

- Versioned candidate, decision, context-bundle, task, outcome, correction, and replay contracts
- Deterministic context-governance engine with stable reason codes
- Synthetic coding repositories and at least five seeded incident classes
- Relevance-only, prompt-only, and runtime-enforcement conditions
- One agent integration or controlled coding-task runner
- Trace inspection, correction, blast-radius lookup, and replay comparison
- Automated scenario, schema, policy, integration, and replay tests
- Reliability, latency, token, review-rate, and regression analysis
- Local or containerized deployment and public documentation

### Explicitly out of scope

- Automatic truth verification for arbitrary natural-language content
- A general enterprise agent control plane
- Support for every coding agent, model provider, repository host, or programming language
- Learned policy engines, fine-tuning, or custom model training
- Production multi-tenancy, billing, enterprise identity, or marketplace distribution
- Human approval for every candidate or coding task
- Claims about the model's private internal reasoning

### Team roles and responsibilities

The following ownership is proposed for planning purposes and must be confirmed by both team members before submission.

| Team member | Primary ownership                                                                       | Supporting responsibilities                                          |
| ----------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Bryan Yang  | Product scope, governance policy, evaluation design, metrics, and documentation         | Data contracts, experiments, repository quality, and final report    |
| Will Liu    | Coding-agent integration, repository fixtures, task runner, and investigation interface | SDK implementation, integration tests, demo flow, and pitch artifact |

Both members will review architecture decisions, pull requests, experiment results, responsible-AI claims, and the final presentation.

### Full-course timeline

| Period      | Checkpoint and output                                                                                                                               |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Weeks 1-2   | Finalize proposal, use case, team roles, scope, risks, repository requirements, and pitch artifact                                                  |
| Weeks 3-5   | Freeze data contracts and five scenario fixtures; implement relevance-only and prompt-only baselines; produce the first end-to-end failure trace    |
| Weeks 6-8   | Implement deterministic governance, reason codes, approved bundles, corrections, and evidence storage                                               |
| Weeks 9-10  | Add blast-radius lookup, replay, investigation interface, and the working coding-agent integration                                                  |
| Weeks 11-12 | Run repeated evaluations; analyze reliability, regressions, latency, tokens, cost, and failure cases; complete container packaging                  |
| Weeks 13-14 | Freeze the release, reproduce results from clean setup, complete documentation and final report, record the demo, and prepare the live presentation |

## 6. GitHub Repository

**Repository URL:** [https://github.com/BryanDYang/agent-accountability-lab](https://github.com/BryanDYang/agent-accountability-lab)

| Required item       | Current status                                                        |
| ------------------- | --------------------------------------------------------------------- |
| README              | Present; must be aligned with the final coding-agent direction        |
| Issue labels        | Must be verified or created before submission                         |
| Code of conduct     | Present                                                               |
| Contributing guide  | Present                                                               |
| Basic CI smoke test | Present through GitHub Actions; final passing status must be verified |
| License             | Present, MIT                                                          |

Repository work will use feature branches, pull-request review, automated lint and tests, versioned fixtures, and reproducible commands. Secrets and generated experiment artifacts will not be committed.

## 7. Selected AI Engineering Focus Areas

### Data

- Build a small dataset from labeled examples curated as synthetic repository fixtures

### Model and system

- Retrieval augmented generation
- Tool use or agentic orchestration

### Application and deployment

- Lightweight user interface
- Local deployment only for the MVP
- Containerized deployment

### Evaluation and responsible AI

- Custom test suite beyond the baseline harness
- Robustness tests for edge cases
- Safety and hallucination checks where applicable
- Latency and cost profiling

## 8. Weekly Check-In and Blockers

### Progress made

- Created the repository scaffold, contribution and conduct documents, MIT license, and GitHub Actions smoke test
- Compared candidate agent use cases and selected coding-agent context governance as the working direction
- Defined the target user, product boundary, preliminary architecture, controlled failure classes, baselines, and evaluation metrics
- Drafted a provider-neutral contract for candidate context, governance decisions, approved bundles, and replay
- Identified token efficiency as a measured outcome rather than an unsupported product claim

### Top blockers and risks

- Team ownership must be confirmed before submission.
- Source precedence among company, repository, directory, file, and task instructions must be frozen before expected fixture outcomes can be finalized.
- The first coding-agent integration and model provider must be selected.
- Existing repository documentation still contains material from an earlier project direction and must be reconciled.
- GitHub issue labels and the current CI result must be verified.

### Planned next steps

1. Confirm roles, integration choice, model provider, and precedence policy.
2. Reconcile README and architecture documents with the coding-agent direction.
3. Implement one narrow fixture and run the three conditions end to end.
4. Use the pilot to confirm metric thresholds, latency measurement, and API cost.
5. Freeze the initial scenario definitions and expected outcomes.
6. Complete and review the six-slide pitch deck.

## 9. Group Contribution Plan for the Next Milestone

| Task                                               | Proposed owner | Dependency or risk                              |
| -------------------------------------------------- | -------------- | ----------------------------------------------- |
| Finalize schemas and SDK boundary                  | Bryan Yang     | Must agree on integration contract              |
| Build repository fixtures and task runner          | Will Liu       | Scenarios need machine-checkable outcomes       |
| Specify governance precedence and reason codes     | Bryan Yang     | Ambiguous conflicts require quarantine behavior |
| Implement first agent integration                  | Will Liu       | Provider and agent choice not yet final         |
| Implement baseline evaluation and token accounting | Bryan Yang     | Pilot needed to set final thresholds            |
| Build initial trace and replay interface           | Will Liu       | Depends on stable storage schema                |
| Review tests, documentation, and demo flow         | Both           | Earlier project-direction text must be removed  |

## 10. Pitch Artifact

**Selected option:** Pitch deck with six slides or fewer
**Working artifact:** To be created. The file `contexts/milestone 1/CIS-5980_Phase1.pptx` is professor-provided course material and is not the team pitch.

The final deck should contain:

1. Problem and firsthand motivation
2. Target user and failure scenario
3. Proposed governance layer and workflow
4. Ambitious but bounded MVP
5. Evaluation design, success targets, and token/latency accounting
6. Timeline, team ownership, risks, and requested teaching-staff feedback

## 11. Requested Teaching-Staff Feedback and Next Steps

The team requests feedback on:

- Whether coding-agent context governance is sufficiently differentiated and appropriately scoped for two people
- Whether the three-condition comparison supports the proposed reliability claims
- Whether the preliminary success thresholds are meaningful and achievable
- Whether deterministic metadata-driven governance is an acceptable boundary for the capstone
- Whether one real integration plus controlled repository fixtures provides enough implementation depth

After receiving feedback, the team will record requested changes, owners, and due dates here before beginning the next milestone.

## 12. Submission Readiness Checklist

- [ ] Confirm the proposed team roles with Bryan Yang and Will Liu
- [ ] Confirm the coding-agent integration and model provider
- [ ] Replace preliminary metric targets if the pilot supports better thresholds
- [ ] Verify GitHub issue labels and passing CI
- [ ] Align README and repository documentation with this proposal
- [ ] Update the six-slide pitch deck to match this proposal
- [ ] Record teaching-staff feedback and next steps when available
- [ ] Export the report and pitch artifact as one PDF according to the Canvas submission instructions
