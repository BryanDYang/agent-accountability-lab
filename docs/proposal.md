# Project Proposal

> **Status:** Draft — Milestone 1

## Working Title

**Trajectory-Level Detection of Memory-Induced Behavioral Drift in Persistent AI Agents**

## Track Declaration

**Research-Driven**, with an emphasis on Evaluation and Responsible AI and a supporting Model and System implementation.

## Problem Statement

Persistent AI agents can change behavior as stored experiences accumulate and retrieval patterns evolve. Aggregate performance metrics can reveal that behavior changed without showing when the change began, which memories influenced it, or whether the change resulted from normal variation or a specific fault.

This project will create a controlled evaluation framework that injects known memory-related drift into an agent, records structured trajectory evidence, detects behavioral changes, and evaluates whether the likely cause can be diagnosed.

## Primary Readers

- Agent-platform and AI infrastructure engineers
- Engineers responsible for observability, evaluation, or safety
- Researchers studying persistent and memory-augmented agents

## Value Proposition

The project turns an ambiguous agent-monitoring problem into a reproducible experiment with known intervention types, known start times, inspectable evidence, and quantitative detection and attribution metrics.

## Research Question

**Can structured trajectory evidence detect and diagnose deliberately induced, memory-driven behavioral drift in a persistent AI agent?**

Supporting questions:

- How accurately can induced drift be distinguished from normal behavioral variation?
- How quickly can drift be detected after an intervention?
- Can memory retrieval evidence identify the likely cause?
- What performance, latency, and token-cost tradeoffs result from memory and monitoring?

## MVP

- One deterministic grid world and fixed task
- One reactive baseline
- One LLM agent with persistent episodic memory
- Structured decision traces with memory provenance
- Memory-poisoning and retrieval-bias interventions
- At least one drift detector
- Reproducible experiments and quantitative results
- Compact replay and investigation interface

Semantic/reflection memory, autonomous goal generation, complex planning, robotics simulators, physical robotics, and a polished multipage dashboard are out of scope.

## Success Metrics

### Offline Metrics

- Drift-detection precision, recall, and F1
- Detection delay
- Root-cause attribution accuracy
- Rule-violation rate
- Task-completion rate

### Reader-Impact Metrics

Given normal and drifted trajectories, measure how accurately and quickly an evaluator can identify the responsible intervention. If a formal reviewer study is infeasible, attribution against intervention ground truth will be the fallback.

### Engineering Metrics

- Trace completeness
- Decision latency
- Token usage and estimated API cost

## Initial Technology and Compute Budget

- Python 3.11+
- Custom grid world or minimal Gymnasium interface
- Provider-neutral LLM interface
- JSONL initially, with SQLite as an optional replacement
- Pandas, Matplotlib, and Pytest
- Streamlit only for a minimal inspection view
- Docker during release hardening

Before Milestone 2, the project will estimate cost per episode and set maximum episode count, token usage, and total API spend. A smaller or local model will be used if repeated experiments would exceed that budget.

## Principal Risks

| Risk | Mitigation | Fallback |
|---|---|---|
| Stochastic LLM behavior masks drift | Constrained actions, repeated seeded runs, aligned episode windows | Validate with a scripted memory-enabled policy first |
| Detector confuses normal task progress with drift | Known intervention ground truth and fixed scenarios | Restrict detection to rule violations and action-distribution changes |
| API cost limits statistical repetitions | Estimate before large runs, cap episodes, cache where valid | Use a smaller/local model and remove secondary conditions |

## Responsible AI

- **Safety:** The agent operates only in a simulation and has no external tools or physical actuators. Poisoned memories are labeled test fixtures.
- **Privacy:** Only synthetic environment data is required; no personal data should appear in prompts or logs.
- **Fairness:** Demographic fairness is not directly tested by the synthetic environment. Any reviewer study will report sampling limitations.
- **Licensing:** Model/API, environment, dependency, and fixture licenses will be recorded before Milestone 2.
- **Transparency:** Every reported run records configuration, model version, seed, intervention, and schema version. Generated explanations are treated as annotations rather than faithful internal reasoning.

See [`../capstone_project_plan.md`](../capstone_project_plan.md) for milestones, experimental conditions, and the definition of done.
