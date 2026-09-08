# Capstone Project Plan: Agent Memory Incident Lab

## 1. The Idea in One Sentence

**Build a developer toolkit that shows when an AI application used a bad memory, lets an operator correct it once, finds other outputs affected by it, and verifies the fix by replaying those cases.**

## 2. The Problem

Long-running AI applications remember information from conversations, tools, databases, and operators. Those memories can later become outdated, conflict with a current system of record, come from an untrusted source, or be replaced by a newer instruction.

Most memory systems optimize retrieval for relevance. A relevant memory is not necessarily a memory the application should still trust. If a bad memory enters an LLM's prompt, the application may produce an incorrect answer or take an incorrect action. Afterward, developers often lack a direct way to determine which memory was used, correct it consistently, identify other affected outputs, or prove that the correction works.

## 3. A Real Product Example

Consider an AI customer-support agent connected to customer records and company policies:

1. The company changes its refund window from 30 days to 14 days.
2. The agent still retains an old conversation memory stating that refunds are allowed for 30 days.
3. A customer requests a refund after 20 days.
4. The old policy is relevant to the request and enters the model's prompt.
5. The agent incorrectly approves the refund.

With the proposed system, a support engineer can open that interaction and see the exact memories and source records supplied to the model. The engineer marks the 30-day memory as replaced by the current 14-day policy. The system prevents the old memory from entering future prompts, finds earlier interactions that used it, and replays selected cases to show whether the correction changes their outcomes.

## 4. What We Are Building

The capstone will deliver the **Agent Memory Incident Lab**, a model-provider-neutral developer toolkit with two connected components:

### Runtime SDK

An application integrates the SDK between memory retrieval and the LLM call. The SDK:

- Records memory provenance, scope, validity, and version relationships
- Applies deterministic admission, rejection, and quarantine policies
- Assembles the approved context sent to the model
- Links retrieved memories to the prompt, model output, tool action, and outcome
- Works through a provider-neutral interface rather than depending on one LLM vendor

### Investigation and Replay Workbench

A lightweight web interface lets a developer or operator:

- Inspect an interaction and the memories that influenced its context
- Understand why each memory was admitted, rejected, or quarantined
- Invalidate or supersede an incorrect memory
- Find the memory's blast radius across previous interactions
- Replay selected interactions with the correction
- Compare the original and corrected outputs

For the capstone, both components will run locally or in a container. A hosted multi-tenant SaaS control plane is a possible future form, not an MVP requirement.

## 5. What This Is Not

- It is not another general agent orchestration platform.
- It does not replace Salesforce, SAP, a vector database, or an agent framework.
- It does not claim to determine whether arbitrary natural-language statements are true.
- It does not require a human to approve every memory or model response.
- It is not dependent on robotics, physical AI, or Gridworld.

The product integrates with an AI application at its memory boundary. Future connectors could work with agents that use Salesforce, SAP, ServiceNow, or other systems of record. The capstone will use a small CRM-style data source so the entire workflow remains reproducible.

## 6. Why This Is Different From an Instruction File

An `AGENTS.md`, system prompt, or application instruction can tell a model to prefer current policies. It does not necessarily prevent conflicting memories from entering the prompt, track which memory affected an output, locate other uses of a bad memory, or replay past cases after a correction.

| Prompt or instruction file | Agent Memory Incident Lab |
|---|---|
| Gives the model guidance | Enforces context assembly in application code |
| Usually contains static instructions | Governs dynamic memories from many sources |
| Leaves conflicting context for the model to resolve | Can remove invalid context before inference |
| Does not expire individual memories | Supports validity periods and supersession |
| Cannot show a memory's full blast radius | Links memories to affected interactions |
| Cannot verify a correction by itself | Replays cases and compares results |

## 7. How the Product Fits Into an AI Application

```text
Customer message
      |
      v
AI application retrieves customer data, policy, and memories
      |
      v
Agent Memory Incident Lab SDK
  1. Record candidates and sources
  2. Enforce memory policy
  3. Build approved context
  4. Create a traceable context bundle
      |
      v
Any supported LLM provider
      |
      v
Response or tool action
      |
      v
Outcome, investigation, correction, and replay
```

The customer-support agent is the demonstration client, not the main product. It will use a chat-style LLM API, a mock CRM, a policy store, persistent conversation memory, and a small set of tools such as `get_order`, `request_refund`, and `escalate_to_human`.

## 8. Human-in-the-Loop Design

Human review will be reserved for exceptions:

```text
Clearly allowed memory       -> admit automatically
Clearly invalid memory       -> reject automatically
Unresolved or high-risk case -> quarantine or escalate
```

Operators define policies, review unresolved conflicts, and correct memories after incidents. The evaluation will measure the review rate so safety is not achieved simply by sending every decision to a human.

## 9. Engineering Question

**Can application-level memory enforcement and replay prevent and diagnose failures that relevance-only retrieval and prompt-level instructions do not reliably prevent?**

Supporting questions:

- Can the SDK stop expired, superseded, or lower-authority memories from entering model context?
- Can a developer trace an incorrect output back to the implicated memory?
- Can the system identify other interactions exposed to the same memory?
- Does replay demonstrate that a correction fixes the targeted cases without causing regressions?
- What false-rejection, human-review, latency, token, and task-success costs does enforcement introduce?

## 10. Target Users and Value

### Primary User

An AI application engineer or reliability engineer responsible for a persistent, tool-using LLM application.

### Usage Setting

The application retrieves information from durable memory and business data before calling an LLM. When an output is wrong, the engineer needs to investigate and correct the application without manually searching prompts and logs across many interactions.

### Value Proposition

**Find the memory behind an AI failure, fix it once, determine what else it affected, and verify that the failure will not recur.**

Success feels like turning an ambiguous model incident into a reproducible software-debugging workflow.

## 11. MVP Scope

### Required

- Python SDK with documented write, retrieve, govern, trace, correct, and replay interfaces
- SQLite persistence for memories, versions, decisions, interactions, and outcomes
- Memory metadata for source, scope, validity, authority, status, and supersession
- Deterministic admission, rejection, quarantine, and prioritization policies
- Append-only interaction and governance events
- Blast-radius query from a memory to affected interactions
- Deterministic replay using stored inputs, configurations, and context candidates
- Side-by-side original and corrected output comparison
- Lightweight investigation workbench
- Provider-neutral model interface with at least one working LLM provider
- Customer-support demonstration with a mock CRM, policies, conversation memory, and tools
- Automated scenario, schema, policy, integration, and replay tests
- Containerized local deployment and documented setup

### Explicitly Out of Scope

- A general-purpose enterprise agent control plane
- Production Salesforce or SAP certification and marketplace distribution
- Multi-tenant billing, identity, or hosted SaaS operations
- Automatic truth verification for arbitrary memories
- Learned policy engines or fine-tuning
- Robotics, physical actuators, or complex simulation
- Broad support for many agent frameworks or model providers
- Human approval for every interaction
- Formal claims that a memory caused the model's internal reasoning

## 12. Demonstration Scenarios

The customer-support application will include at least four controlled incidents:

1. **Superseded policy:** An old refund rule conflicts with the current policy.
2. **Stale customer fact:** A remembered account tier conflicts with the CRM record.
3. **Untrusted instruction:** Customer-provided text attempts to become an authoritative internal policy.
4. **Cross-scope leakage:** A memory belonging to one customer is retrieved for another customer.

Each fixture will define the memory candidates, sources, expected governance decisions, expected safe answer or action, and expected replay change before experiments run.

## 13. Evaluation

### Compared Systems

1. **Relevance-only retrieval:** Retrieved memories enter context without governance.
2. **Prompt-only governance:** The model receives the same candidates plus instructions to prefer current and trusted information.
3. **Runtime enforcement:** The SDK checks candidates before the model receives them.

The same user request, business records, memory candidates, tools, and model configuration will be used across conditions.

### Primary Metrics

- **Policy-violation rate:** Responses or actions that violate the current scenario policy
- **Invalid-memory admission rate:** Invalid candidates included in model context
- **Correction success rate:** Targeted failures resolved after correction and replay
- **Regression rate:** Previously correct cases made incorrect by a correction
- **Blast-radius recall:** Known affected interactions returned by the impact query
- **Task-success rate:** Customer requests handled correctly or safely escalated
- **Human-review rate:** Interactions requiring operator review

### Engineering and User Metrics

- SDK latency and end-to-end latency
- Context-token and API-cost overhead
- Trace completeness
- Time and accuracy for a developer to diagnose a seeded incident
- Clarity of the original-versus-replay comparison

If a formal developer study is infeasible, diagnosis and blast-radius results will be checked automatically against scenario ground truth and the user study will remain future work.

## 14. Core Data Contracts

### Memory Record

```json
{
  "memory_id": "mem_refund_v1",
  "scope": "organization:demo-company",
  "content": "Refunds are allowed within 30 days.",
  "source_type": "policy_document",
  "source_id": "refund-policy-v1",
  "authority": 90,
  "status": "superseded",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2026-07-31T23:59:59Z",
  "superseded_by": "mem_refund_v2"
}
```

### Context Decision

```json
{
  "interaction_id": "int_2048",
  "memory_id": "mem_refund_v1",
  "decision": "reject",
  "reason_codes": ["SUPERSEDED", "OUTSIDE_VALIDITY_WINDOW"],
  "policy_version": "memory-policy-v1"
}
```

### Replay Record

```json
{
  "original_interaction_id": "int_2048",
  "replay_id": "replay_0031",
  "correction_id": "mem_refund_v2",
  "original_output": "Your refund is approved.",
  "replay_output": "This request is outside the 14-day window.",
  "expected_outcome_met": true
}
```

## 15. Technology Plan

- Python 3.11+
- Pydantic or dataclasses for versioned contracts
- SQLite for local persistence
- JSONL export for append-only evidence
- FastAPI for the service boundary if needed by the demo
- Streamlit or a small web UI for investigation and replay
- Provider-neutral LLM adapter with one required provider implementation
- A mock CRM backed by deterministic fixtures
- Pytest, Ruff, and mypy for verification
- Pandas and Matplotlib for evaluation
- Docker for the release candidate

API usage will be capped after a pilot estimates cost per case. Deterministic or recorded responses will validate system behavior; repeated live-model runs will be reserved for measuring model-dependent outcomes.

## 16. Responsible AI and Data Plan

- **Privacy:** Use synthetic customers, orders, conversations, and policies. Do not send real personal or business data to model APIs.
- **Safety:** Demo tools operate on a synthetic CRM and cannot issue real refunds or change external records.
- **Human oversight:** Escalate only unresolved or high-risk cases and measure escalation burden.
- **Transparency:** Record model, prompt, policy, schema, memory, and configuration versions for every run.
- **Security:** Test scope isolation and untrusted-memory injection explicitly.
- **Limitations:** Source authority and ground truth are supplied by controlled fixtures. The MVP does not independently authenticate sources or establish objective truth.
- **Licensing:** Record licenses and terms for dependencies, model APIs, and released fixtures before publication.

## 17. Risks and Mitigations

| Risk | Mitigation | Fallback |
|---|---|---|
| The project resembles existing control planes or memory products | Focus on incident investigation, blast radius, correction replay, and comparison with prompt-only governance | Present it as an interoperable reference implementation and evaluation rather than a new general platform |
| Conflict detection becomes open-ended language reasoning | Use explicit scopes, versions, validity, source types, and controlled conflict groups | Limit the MVP to deterministic predicates |
| Replay is not reproducible because LLMs are stochastic | Store complete inputs and configurations and repeat model runs | Use recorded or deterministic model responses for system correctness tests |
| Human review becomes the bottleneck | Admit and reject clear cases automatically and measure review rate | Quarantine uncertain memory while allowing low-risk tasks to continue |
| The demo becomes a customer-support project instead of a memory product | Keep the customer-support agent thin and isolate it behind the SDK contract | Replace it with another fixture-driven LLM client without changing the core system |
| API cost limits experiments | Pilot early, cap tokens and repetitions, and cache only where valid | Use a smaller or local model for secondary runs |

## 18. Definition of Done

A new developer can:

1. Start the toolkit and demonstration locally with one documented command.
2. Run the same support incidents under relevance-only, prompt-only, and enforced-memory conditions.
3. Inspect the memories and business records used for one incorrect output.
4. Correct or supersede the implicated memory.
5. Find other interactions exposed to that memory.
6. Replay selected interactions and compare original and corrected outputs.
7. Reproduce the reported safety, task-success, review-rate, trace, latency, and cost metrics.

## 19. Course-Aligned Milestones

### Milestone 1: Product and Evaluation Design, Weeks 1-2

- Finalize problem, target user, product boundary, realistic support workflow, and team roles
- Define SDK interfaces, trace schema, governance rules, incident fixtures, baselines, and metrics
- Establish repository standards, CI, documentation, risk plan, and pitch artifact

### Milestone 2: Baselines and Evidence Model, Weeks 3-5

- Implement synthetic CRM, thin support agent, relevance-only baseline, and prompt-only baseline
- Implement memory, interaction, context, outcome, and replay contracts
- Freeze four incident fixtures and expected outcomes
- Produce the first end-to-end incorrect-output trace

### Milestone 3: Enforcement and Investigation Alpha, Weeks 6-9

- Implement runtime governance, correction, supersession, quarantine, and reason codes
- Implement blast-radius queries and deterministic replay
- Deliver the investigation workbench and full end-to-end workflow
- Run initial three-condition experiments and document failures

### Milestone 4: Release Candidate, Weeks 10-12

- Repeat evaluation across fixed cases and model runs
- Complete latency, token, cost, review-rate, and regression analysis
- Harden integration tests, container deployment, documentation, and demo flow
- Draft the technical report, System Card, and demo video

### Final Deliverable, Weeks 13-14

- Publish the repository and tagged release
- Deliver the final report, comparison figures, and limitations
- Demonstrate investigation, correction, blast-radius analysis, and replay live

## 20. Immediate Decisions for the Team

- Confirm the customer-support incident workflow as the primary demonstration
- Select the first LLM provider and define the provider-neutral adapter boundary
- Decide whether the demo CRM is entirely local or uses a developer sandbox
- Assign owners for SDK and storage, demo agent and fixtures, workbench, evaluation, and documentation
- Schedule a weekly cadence meeting and track decisions and blockers in the repository
