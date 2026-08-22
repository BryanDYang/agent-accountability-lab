# Evaluation Plan

> **Status:** Draft – Phase 1

## Agent Variants Under Test

| Variant | Memory | Accountability | Notes |
|---|---|---|---|
| Baseline | None | None | Rule-based reactive |
| LLM Only | None | None | LLM chooses actions |
| LLM + Memory | Episodic + Semantic | None | |
| LLM + Memory + Reflection | All | None | |
| LLM + Memory + Accountability | All | Full | Primary research target |

## Evaluation Dimensions

| Dimension | Metric |
|---|---|
| Task completion | % of goals reached per episode |
| Consistency | Action entropy over time |
| Explainability | Human rating of decision traces (1–5) |
| Auditability | % of actions with full trace |
| Drift detection | Drift score at 100/500/1000 steps |
| Latency / cost | Avg. seconds and tokens per step |

## Experiment Protocol

1. Reset environment with fixed seed.
2. Run agent for N steps (N = 200 / 500 / 1000).
3. Save JSONL log to `experiments/results/<variant>/`.
4. Compute metrics offline.
5. Repeat 5 times per variant; report mean ± std.
