# Architecture

> **Status:** Draft – Phase 1

## High-Level Overview

```
Simulation Environment
        ↓
Observation Interface
        ↓
Agent Brain
  ├── LLM Reasoning
  ├── Memory Retrieval
  ├── Goal Selection
  └── Planning
        ↓
Action Executor
        ↓
Environment Update
        ↓
Accountability Logger
        ↓
Evaluation + Visualization Dashboard
```

## Module Map

| Module | Path | Responsibility |
|---|---|---|
| Environments | `src/accountable_agents/envs/` | Grid-world, adapters |
| Agents | `src/accountable_agents/agents/` | Base, LLM, memory agents |
| Memory | `src/accountable_agents/memory/` | Episodic, semantic, retrieval |
| Planning | `src/accountable_agents/planning/` | Goal management, planner |
| Accountability | `src/accountable_agents/accountability/` | Logger, traces, explanations |
| Evaluation | `src/accountable_agents/evaluation/` | Metrics, drift detection |
| Dashboard | `src/accountable_agents/dashboard/` | Streamlit app |

## Environment Interface

```python
class Environment:
    def reset(self) -> dict: ...
    def observe(self) -> dict: ...
    def step(self, action: str) -> tuple[dict, float, bool, dict]: ...
    def render(self) -> None: ...
```

## Agent Interface

```python
observation = env.observe()
action, trace = agent.act(observation)
next_state, reward, done, info = env.step(action)
logger.record(observation, action, trace, next_state)
```
