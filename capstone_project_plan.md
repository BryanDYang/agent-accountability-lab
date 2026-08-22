# Capstone Project Plan: Accountable Agents

## Working Title

**Trajectory-Level Detection of Memory-Induced Behavioral Drift in Persistent AI Agents**

## Track and Focus

- **Course track:** Research-Driven
- **Primary focus:** Evaluation and Responsible AI
- **Supporting focus:** Model and System
- **Primary readers:** Engineers and researchers responsible for evaluating, monitoring, or operating persistent AI agents

## Project Summary

This project will build an evaluation framework for detecting and diagnosing deliberately induced behavioral drift in a persistent, memory-augmented AI agent.

A deterministic grid world will serve as a controlled experimental testbed. The project will compare normal and drifted agent trajectories under fixed seeds, known intervention times, and known intervention causes. The central contribution is the trajectory schema, controlled-drift protocol, detection evaluation, and investigation workflow—not the simulator or a general-purpose agent architecture.

The broader research direction remains accountable embodied agents. More complex simulation and physical robotics are explicitly future work.

## Research Question

**Can structured trajectory evidence detect and diagnose deliberately induced, memory-driven behavioral drift in a persistent AI agent?**

Supporting questions:

- How accurately can a detector distinguish normal behavioral variation from an induced change?
- How quickly after an intervention can the change be detected?
- Can recorded memory retrievals help identify the likely cause of the drift?
- What task-performance, latency, and token-cost tradeoffs result from persistent memory and monitoring?

## Value Proposition

Persistent agents can change behavior as their stored experiences and retrieval patterns evolve. Aggregate success metrics may show that performance changed without showing when the change began or what evidence influenced it. This project provides a reproducible way to inject known memory-related faults, observe complete decision trajectories, measure drift detection, and investigate likely causes.

## Scope

### Required

- One deterministic custom grid world
- One fixed task with at least one explicit behavioral or safety rule
- One reactive, non-memory baseline
- One LLM agent with persistent episodic memory
- JSONL or SQLite trajectory storage
- Complete references from decisions to retrieved memory records
- Two controlled drift interventions: memory poisoning and retrieval bias
- One statistical drift detector; a second method is optional
- Seeded, repeatable experiment commands
- Quantitative evaluation and failure analysis
- A compact replay and trace-inspection interface

### Out of Scope

- MuJoCo, Isaac Sim, Habitat, or physical robotics
- Multiple simulation environments
- Semantic and reflection memory hierarchies
- Autonomous goal generation or competing-goal management
- A general-purpose planning framework
- Vector databases unless retrieval scale demonstrates a need
- Five-way agent architecture comparisons
- Reinforcement learning or model training
- A large or polished multipage dashboard
- Claims that generated explanations reveal the model's internal reasoning

## Experimental System

```text
Deterministic Grid World
        |
        v
Agent: reactive baseline or LLM + episodic memory
        |
        v
Structured Decision/Event Trace
        |
        +--> Drift Detector
        +--> Metrics and Evaluation
        +--> Replay and Investigation View
```

For every decision, the trace should capture observable evidence:

- Environment and episode identifiers
- Seed, step, timestamp, and experimental condition
- Agent observation and available actions
- Retrieved memory IDs and retrieval scores
- Selected action and applicable task or policy constraint
- Environment outcome, reward, and rule violations

Generated explanations may be stored as annotations, but they will not be treated as proof of the model's true reasoning.

## Experimental Conditions

1. Reactive baseline without persistent memory
2. Memory-enabled agent without an intervention
3. Memory-enabled agent with memory poisoning
4. Memory-enabled agent with retrieval bias

### Controlled Drift Interventions

**Memory poisoning:** At a defined episode, insert misleading experience records that suggest an unsafe or ineffective shortcut succeeds.

**Retrieval bias:** At a defined episode, alter retrieval weighting so misleading, outdated, or recent memories become disproportionately likely to influence decisions.

Every intervention has a known type and start time, providing ground truth for detection and attribution.

## Evaluation

### Primary Metrics

- Drift-detection precision, recall, and F1
- Detection delay after the intervention
- Root-cause attribution accuracy
- Rule-violation rate
- Task-completion rate

### Secondary Engineering Metrics

- Percentage of actions with complete trace evidence
- Average latency per decision
- Input and output tokens per episode
- Estimated API cost per episode

### Reader-Impact Evaluation

Given a sample of normal and drifted runs, measure an evaluator's accuracy identifying the responsible intervention, time to diagnosis, and confidence. If a formal reviewer study is infeasible, root-cause attribution against intervention ground truth will be the documented fallback.

## Course-Aligned Milestones

### Milestone 1 — Proposal, Scope, and Experimental Design (Weeks 1–2)

Deliverables:

- Track declaration, problem statement, primary readers, and value proposition
- Fixed MVP and explicit exclusions
- Grid-world, agent, trajectory, and intervention specifications
- Offline and reader-impact metrics
- Initial architecture and 14-week timeline
- Tech stack and compute/API budget
- Risks, mitigations, and fallbacks
- Licensing, safety, fairness, and privacy plan
- Repository with README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, and CI smoke test
- Six-slide pitch deck or three-to-five-minute concept video

Exit criteria:

- Each experimental condition, intervention, and metric is defined before core implementation begins.
- The repository installs and its smoke tests pass in CI.

### Milestone 2 — Evaluation Harness and Baselines (Weeks 3–5)

Deliverables:

- Deterministic grid world and fixed task
- Reactive baseline
- Versioned trajectory/event schema
- Seeded experiment runner
- Drift-injection protocol with known intervention time and cause
- Metric implementations and initial baseline results
- Scenario/Data Card describing generated data and limitations
- Mandatory TA check-in

Exit criteria:

- Repeated baseline runs are reproducible from one command.
- The evaluation pipeline scores a synthetic or scripted drift fixture correctly.

### Milestone 3 — End-to-End Alpha (Weeks 6–9)

Deliverables:

- LLM agent with persistent episodic memory
- Memory poisoning and retrieval-bias interventions
- Complete decision traces with memory provenance
- At least one working drift detector
- Root-cause attribution method
- Basic replay and investigation interface
- Initial repeated experiments
- Model Card and System Card

Exit criteria:

- One command executes normal and drifted conditions and produces traces, metrics, and an inspectable run.
- At least one induced drift scenario is detected above the declared baseline threshold.

### Milestone 4 — Release Candidate and Documentation (Weeks 10–12)

Deliverables:

- Frozen feature set and repeated seeded experiments for both interventions
- Final primary and secondary metrics
- Failure and error analysis
- Tests for schema validity, intervention timing, and metric correctness
- Reproducible/containerized release candidate
- Draft technical report, documentation, and short demo video
- Mandatory TA check-in

Exit criteria:

- Results can be regenerated from documented commands.
- Known limitations and failed cases are documented.
- No required analysis depends on manual inspection alone.

### Final Deliverable — Report and Showcase (Weeks 13–14)

- Final technical report
- Public reproducible repository
- Final tables and figures
- Replay/investigation demonstration
- Live presentation
- Documented limitations and future work

## Definition of Done

The capstone is complete when a documented command can:

1. Run seeded normal and drifted experimental conditions.
2. Introduce a named intervention at a known episode.
3. Save complete trajectory evidence with memory references.
4. Detect and timestamp the resulting behavioral change.
5. Attribute the likely cause using recorded evidence.
6. Produce quantitative metrics and a replayable investigation report.

## Initial Tech Stack

- Python 3.11+
- Custom grid world or a minimal Gymnasium interface
- OpenAI, Anthropic, or a local model behind a small provider interface
- JSONL initially; SQLite if querying becomes cumbersome
- Pandas and Matplotlib for analysis
- Pytest for unit and integration tests
- Streamlit only if it remains the fastest route to the compact inspection view
- Docker as a Milestone 4 packaging task

## Risks, Mitigations, and Fallbacks

| Risk | Mitigation | Fallback |
|---|---|---|
| LLM stochasticity obscures induced drift | Fixed seeds where supported, constrained actions, repeated runs, and a deterministic baseline | Use a scripted memory-enabled policy to validate the harness before evaluating the LLM agent |
| Drift detector cannot separate task progress from drift | Compare aligned episode windows and use known intervention ground truth | Limit the detector to rule violations and action-distribution changes in one fixed scenario |
| API cost or latency prevents sufficient repetitions | Cache outputs where valid, cap episode length, and estimate cost before large runs | Use a smaller or local model and reduce secondary conditions, not repetitions of the primary experiment |

## Responsible AI Plan

- **Safety:** The project studies simulated failures only and will not connect the agent to external tools or physical actuators. Intervention code and unsafe shortcuts will be labeled as evaluation fixtures.
- **Privacy:** Experiments use synthetic environment data. Prompts, traces, and responses will be retained only for reproducibility and will not contain personal data.
- **Fairness:** Human demographic fairness is not directly implicated by the synthetic grid world. If reviewers participate, report sampling limitations and avoid claims that generalize beyond that group.
- **Licensing:** Record licenses and usage constraints for the environment library, model/API, and released evaluation fixtures before Milestone 2.
- **Accountability:** Record model versions, configurations, seeds, interventions, and trace-schema versions for every reported run.

## Future Work

After the capstone, the framework could expand to richer memory architectures, additional drift causes, MiniGrid or robotics simulators, human-in-the-loop intervention, and eventually physical embodied agents. These extensions are not dependencies for capstone completion.
