# Capstone Project Plan: Accountable Memory Gateway

## 1. The Idea in One Sentence

**Before an AI agent uses a stored memory, this project checks whether that memory is still valid, trusted, and safe.**

## 2. Why This Is Needed

Some AI agents remember information from earlier tasks.

That is useful, but a remembered instruction may later become wrong. It may be old, come from an untrusted source, conflict with a safety rule, or have been replaced by a newer instruction.

If the agent uses that bad memory, it may make a bad decision.

## 3. A Simple Example

Imagine an AI agent moving through a map:

1. The agent learns: **"Zone 7 is a shortcut."**
2. Later, a safety operator says: **"Zone 7 is now dangerous. Do not enter it."**
3. The agent asks its memory system for information about Zone 7.
4. A normal memory search may return the old shortcut because it is relevant.
5. The agent may enter Zone 7 and violate the new safety instruction.

The problem is not that the memory search failed. It found a relevant memory. The problem is that **relevance alone does not tell the agent whether a memory should still be used**.

## 4. What This Project Does

This project adds a checkpoint between the agent's stored memories and the AI model.

The checkpoint asks:

- Is this memory still active?
- Has it expired?
- Did a newer memory replace it?
- Who provided it?
- Does it conflict with a higher-priority safety instruction?

In the Zone 7 example, it blocks the old shortcut and gives the model the current safety instruction. It also records why it made that decision.

This checkpoint is called the **Accountable Memory Gateway**.

## 5. How It Is Different

A typical memory system asks:

> Which stored information is most relevant?

This project asks two questions:

> Which stored information is most relevant?
>
> Which of that information is allowed to enter the AI model's prompt?

| Typical agent memory | Accountable Memory Gateway |
|---|---|
| Finds relevant memories | Finds relevant memories and checks them |
| May return old and new instructions together | Blocks instructions replaced by newer ones |
| Usually treats sources similarly | Gives trusted sources more authority |
| Shows what was retrieved | Shows what was allowed, blocked, and why |
| Has no consistent correction process | Lets an operator invalidate or replace a memory |

This is not a new chatbot or a new memory database. It is a **control layer for AI applications that already use persistent memory**.

## 6. What Will Be Built

The capstone will contain four parts:

1. **AI agent:** Receives a goal and chooses what to do next.
2. **Grid world:** A small map where the agent completes a task and can encounter hazards.
3. **Memory store:** Holds the agent's previous observations and instructions.
4. **Memory gateway:** Checks memories before adding them to the model's prompt.

```text
Agent needs to decide what to do
                |
                v
      Find relevant memories
                |
                v
 Check which memories may be used
                |
                v
 Give approved memories to the AI model
                |
                v
   Agent acts and outcome is recorded
```

## 7. What the Demo Will Show

The same agent will run the same tasks in two modes:

1. **Without the gateway:** Relevant memories go directly into the model's prompt.
2. **With the gateway:** Relevant memories are checked before entering the prompt.

The demo will test four common failures:

- A malicious or low-trust memory
- An expired memory
- A memory that conflicts with a safety rule
- An old instruction replaced by a correction

A small inspection screen will show:

- Which memories were found
- Which were allowed or blocked
- Why each decision was made
- What the model received
- What action the agent took
- Whether the action was safe and successful

The evaluation will answer a simple question: **Does checking memory before use reduce unsafe actions while still allowing the agent to complete its task?**

## 8. Project Details

- **Working title:** Accountable Memory Gateway for Persistent AI Agents
- **Course track:** AI Engineering
- **Primary focus:** Model and System
- **Secondary focus:** Evaluation and Responsible AI
- **Supporting focus:** Application and Deployment
- **Primary users:** Engineers building AI agents that retain memory between tasks

The sections below provide the lower-level technical design, evaluation plan, implementation scope, and delivery schedule.

## 9. Technical Project Summary

This project will build a runnable layer that checks persistent memories before placing them in an AI agent's prompt. Instead of selecting memories by relevance alone, the gateway will also consider source, authority, validity, replacement, and safety priority. It will record which memories were considered, which were allowed or blocked, why each decision was made, what action the agent took, and what happened next.

A deterministic grid world will serve as the end-to-end demonstration client. Controlled memory-failure scenarios will validate the gateway against a relevance-only retrieval baseline. The primary contribution is the engineered gateway, integration contract, audit trail, operator correction workflow, and deployable demonstration. Evaluation demonstrates product value but is not the sole deliverable.

The longer-term vision remains accountable persistent and embodied agents. Rich memory platforms, advanced simulators, and physical robotics are future extensions rather than capstone requirements.

## Product Problem

Persistent agents accumulate memories from observations, model outputs, users, operators, and policies. A relevance-only retrieval system can surface an obsolete shortcut, poisoned experience, or low-authority observation alongside an active safety correction. The application then lacks a consistent mechanism to decide which memory should be trusted or to explain why it entered the model's context.

The Accountable Memory Gateway provides a control point between durable memory and working context. It allows an application to define deterministic governance rules, reject or subordinate unsafe memory candidates, apply operator corrections, and reconstruct memory influence lineage after a decision.

## Engineering Question

**Can a provenance- and policy-aware memory gateway prevent stale, untrusted, or superseded memories from entering a persistent agent's working context while preserving task performance and producing an auditable decision trail?**

Supporting questions:

- Can the gateway consistently enforce authority, validity, supersession, and safety-priority rules?
- Does governed retrieval reduce unsafe actions compared with relevance-only retrieval?
- How reliably does an authoritative operator correction change future context assembly?
- What latency, token, and task-performance overhead does governance introduce?
- Can an engineer reconstruct the memory-to-context-to-action sequence from the audit trail?

## Value Proposition

Existing memory retrieval commonly asks, "Which stored information is relevant?" This gateway adds a second question: "Which relevant information is currently authorized and safe to place in context?"

The system gives agent developers:

- A documented integration point for governed context assembly
- Explicit memory provenance and lifecycle metadata
- Deterministic, testable admission and rejection rules
- Operator correction, invalidation, and supersession controls
- Evidence showing which memories were considered and why they were admitted or rejected
- A reproducible way to test memory-related safety failures

The project will describe this evidence as **memory influence lineage**, not proof that a retrieved memory caused an LLM's internal reasoning.

## User Workflow

1. An application submits a memory candidate with content and governance metadata.
2. The gateway validates and stores the memory.
3. An agent requests memories relevant to its current observation or task.
4. Retrieval produces a ranked candidate set.
5. The governance engine checks authority, validity, status, supersession, and safety priority.
6. The gateway returns an approved context bundle and machine-readable governance decisions.
7. The agent selects an action.
8. The application records the action and outcome against the context bundle.
9. An operator can inspect, invalidate, supersede, or correct a memory.

## MVP Scope

### Required

- Memory ingestion through a documented Python interface or local API
- Persistent memory storage using SQLite
- A versioned memory schema with provenance and lifecycle metadata
- Simple candidate retrieval suitable for the controlled demonstration
- Deterministic governance policies
- Memory admission, rejection, and prioritization decisions with reason codes
- Memory invalidation and supersession
- Authoritative operator corrections
- Approved context-bundle assembly
- Append-only governance and action audit events
- A documented agent integration
- One deterministic grid-world demonstration client
- Relevance-only and governed-retrieval modes
- Four controlled memory-failure scenarios
- Compact operator inspection interface
- Automated tests and containerized local deployment

### Explicitly Out of Scope

- A general-purpose or enterprise memory platform
- Knowledge graphs or graph databases
- Vector databases unless the MVP demonstrates a concrete need
- Learned policy engines or automatic truth verification
- Semantic and reflection memory hierarchies
- Autonomous goal generation or a general planning framework
- Multiple agent frameworks or simulator integrations
- MuJoCo, Isaac Sim, Habitat, and physical robotics
- Reinforcement learning, fine-tuning, or model training
- A large, polished, multipage dashboard
- Formal causal claims about how an LLM arrived at a decision

## System Architecture

```text
Agent Application / Grid-World Demo
                |
                v
        Memory Query Interface
                |
                v
      Accountable Memory Gateway
        1. Retrieve candidates
        2. Validate provenance
        3. Check status and validity
        4. Resolve supersession
        5. Apply authority rules
        6. Enforce safety priority
                |
                +----> Append-only audit events
                |
                v
       Approved Context Bundle
                |
                v
        Agent Action and Outcome
```

The gateway will separate candidate retrieval from governance. This makes it possible to compare relevance-only retrieval with governed retrieval without changing the agent or environment.

## Core Data Contracts

### Memory Record

```json
{
  "memory_id": "M205",
  "content": "Do not enter Zone 7 while the beacon is active.",
  "source_type": "safety_operator",
  "source_id": "operator-12",
  "authority": 100,
  "confidence": 1.0,
  "criticality": "safety",
  "status": "active",
  "created_at": "2026-08-23T10:00:00Z",
  "valid_from": "2026-08-23T10:00:00Z",
  "valid_until": null,
  "supersedes": ["M101"]
}
```

### Governance Decision

```json
{
  "memory_id": "M205",
  "decision": "admit",
  "reason_codes": [
    "ACTIVE",
    "AUTHORITATIVE_SOURCE",
    "APPLICABLE_SAFETY_CONSTRAINT"
  ]
}
```

### Context Bundle and Outcome Linkage

Each context bundle should record:

- Query, observation, and available actions
- Candidate memory IDs and retrieval scores
- Governance decision and reason codes for each candidate
- Ordered admitted memory IDs
- Active policy and schema versions
- Agent/model configuration
- Selected action
- Environment outcome and rule-violation indicators

## Governance Policy

The MVP policy will be deterministic and intentionally small:

1. Reject memories that are invalid, expired, or inactive.
2. Reject or subordinate memories superseded by an active replacement.
3. Resolve direct conflicts in favor of the higher-authority applicable memory.
4. Prioritize active safety-critical memories over convenience or efficiency memories.
5. Record a stable reason code for every admission, rejection, or prioritization decision.
6. Fail closed when a required safety conflict cannot be resolved.

The capstone will not attempt to determine whether arbitrary natural-language memories are objectively true. Controlled scenarios will supply explicit metadata and known expected outcomes.

## Product Validation

### Compared Systems

1. **Relevance-only retrieval:** Candidate ranking determines context insertion without governance checks.
2. **Governed retrieval:** The same candidates pass through the Accountable Memory Gateway.

The same agent, task, scenario, and candidate memories will be used in both modes.

### Controlled Scenarios

- **Poisoned memory:** A low-authority source inserts a misleading shortcut.
- **Stale memory:** A previously valid environmental fact has expired.
- **Conflicting authority:** A low-authority observation conflicts with an active safety policy.
- **Superseded instruction:** A newer operator correction replaces an obsolete instruction.

Each scenario will define the candidate memories, applicable policies, expected governance decisions, and expected safe action before the experiment runs.

## Success Metrics

### Primary Product Metrics

- **Invalid-memory admission rate:** Invalid, expired, or superseded memories admitted divided by those considered
- **Unsafe-action rate:** Actions violating an active safety constraint divided by eligible decisions
- **Governance-policy accuracy:** Governance decisions matching scenario ground truth
- **Correction adoption rate:** Applicable decisions using the authoritative replacement after an operator correction
- **Task-completion rate:** Successfully completed episodes divided by attempted episodes
- **Trace completeness:** Decisions containing every required lineage field

### Engineering Metrics

- Gateway latency per query
- End-to-end decision latency
- Context-token overhead
- Storage growth per episode
- API or model cost per episode

### User-Impact Metric

The primary user-impact question is whether the audit trail helps an engineer investigate a memory-related failure. If participant access permits, measure diagnosis accuracy and time using a summary-only view versus the gateway's lineage view. If a reviewer study is infeasible, validate reconstructability automatically against scenario ground truth and document the study as future work.

## Definition of Done

The capstone is complete when a new developer can follow the documentation to:

1. Start the gateway and demonstration client locally with one documented command.
2. Ingest memories with provenance, authority, validity, and supersession metadata.
3. Retrieve candidates and receive an approved context bundle with reason codes.
4. Invalidate or supersede a memory through an operator workflow.
5. Run relevance-only and governed modes against all controlled scenarios.
6. Reproduce the reported safety, task-performance, trace, and latency metrics.
7. Inspect the complete memory-to-context-to-action lineage for a selected decision.

## Course-Aligned Milestones

### Milestone 1 — Product Scope and Engineering Design (Weeks 1–2)

Deliverables:

- AI Engineering track declaration and selected focus areas
- Problem statement, target user, value proposition, and user workflow
- MVP, explicit exclusions, architecture, and data contracts
- Governance-policy specification and controlled-scenario definitions
- Offline and user-impact success metrics
- Technology choices and compute/API budget
- Top risks, mitigations, fallbacks, and Responsible AI plan
- Repository with README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, and passing CI
- Six-slide pitch deck or three-to-five-minute concept video

Exit criteria:

- The gateway boundary and agent integration contract are documented.
- Every required scenario has expected governance and action outcomes.
- The repository installs and its smoke tests pass in CI.

### Milestone 2 — Data Contracts, Baseline, and Evaluation Harness (Weeks 3–5)

Deliverables:

- Versioned memory, governance-event, context-bundle, and outcome schemas
- SQLite repository and memory ingestion interface
- Deterministic grid world and fixed task
- Relevance-only retrieval baseline
- Scenario fixtures and expected decisions
- Metric implementations and seeded experiment runner
- Scenario/Data Card and initial baseline results
- Mandatory TA check-in

Exit criteria:

- One command reproduces relevance-only results for all scenario fixtures.
- Schema validation and metric tests pass.
- The baseline demonstrates at least one designed memory-related failure.

### Milestone 3 — Gateway and End-to-End Alpha (Weeks 6–9)

Deliverables:

- Governance engine with stable reason codes
- Invalidation, supersession, and operator-correction workflows
- Approved context-bundle assembly
- Agent integration and outcome linkage
- Append-only audit trail
- Governed-retrieval experiments for all scenarios
- Basic inspection interface
- Model Card and System Card

Exit criteria:

- The complete ingest-to-action-to-investigation workflow runs end to end.
- Automated tests verify expected governance decisions for every scenario.
- Initial comparison results show where governance helps and where it fails.

### Milestone 4 — Release Candidate and Documentation (Weeks 10–12)

Deliverables:

- Frozen feature set
- Repeated seeded evaluation of relevance-only and governed modes
- Final safety, task-performance, trace, and overhead results
- Failure and error analysis
- Integration tests and reproducibility checks
- Containerized release candidate
- API/integration documentation, draft technical report, and demo video
- Mandatory TA check-in

Exit criteria:

- A new developer can run the documented workflow locally.
- Reported results can be regenerated from versioned commands and fixtures.
- Limitations and unresolved policy cases are documented.

### Final Deliverable — Public Release and Showcase (Weeks 13–14)

- Public repository and tagged release
- Final technical report
- Final comparison tables and figures
- Live memory-governance and investigation demonstration
- Documentation of limitations and future work
- Showcase presentation

## Initial Technology Choices

- Python 3.11+
- SQLite for memory records and queryable state
- JSONL for append-only audit-event export
- Pydantic or dataclasses for versioned contracts
- A simple lexical or embedding-free retriever for the MVP
- Provider-neutral LLM interface for the demonstration agent
- Custom grid world or minimal Gymnasium interface
- FastAPI only if a local service boundary improves the integration demonstration
- Streamlit only if it is the fastest route to a compact inspection view
- Pandas and Matplotlib for evaluation
- Pytest, Ruff, and mypy for verification
- Docker for the Milestone 4 release candidate

## Risks, Mitigations, and Fallbacks

| Risk | Mitigation | Fallback |
|---|---|---|
| Natural-language conflict detection becomes an open-ended reasoning problem | Use explicit scenario metadata and narrow policy predicates | Require scenarios to declare conflict groups and applicable constraints |
| Governance rules make the agent safe but unable to complete tasks | Measure task completion alongside safety and test policy precedence | Narrow to one safety rule and one efficiency tradeoff with documented fail-closed behavior |
| The project expands into a general memory platform | Freeze the MVP interfaces and four scenario families at Milestone 1 | Remove HTTP service and use a documented in-process Python interface |
| LLM stochasticity obscures gateway effects | Hold candidate memories and scenarios constant and repeat runs | Use a scripted agent to verify policy behavior, then treat the LLM demo as secondary |
| API cost limits repeated runs | Estimate cost in a pilot and constrain actions and episode length | Use a smaller or local model without reducing core policy tests |

## Responsible AI Plan

- **Safety:** The system operates only in simulation and has no external tools or physical actuators. Poisoned memories are labeled evaluation fixtures. Safety conflicts fail closed.
- **Privacy:** Core experiments use synthetic data. Logs will avoid personal data and document retention and deletion behavior.
- **Fairness:** The grid-world scenarios do not support demographic fairness claims. Any participant-based investigation study will report sampling limitations.
- **Licensing:** Record licenses and usage constraints for dependencies, the environment, model/API, and released fixtures.
- **Transparency:** Record model, schema, policy, scenario, and configuration versions for every reported run.
- **Limitations:** Governance metadata is supplied by the controlled system; the MVP does not independently verify whether a source is truthful or an authority is legitimate.

## Future Work

Future extensions may include learned conflict detection, temporal knowledge graphs, richer source authentication, policy authoring tools, additional agent-framework adapters, live monitoring, more complex simulations, and physical embodied agents. None of these are dependencies for capstone completion.
