# Capstone Project Plan: Accountable Embodied Agents

## Working Title

**Digital Twin Environment for Evaluating Accountability, Memory, and Behavioral Drift in Autonomous AI Agents**

## Core Idea

This project explores how long-lived autonomous AI agents can remain explainable, auditable, and accountable as they accumulate memories, pursue goals, and adapt behavior over time. The initial implementation will use a simulated environment instead of physical robotics so that the project can be built and evaluated within a 14-week capstone timeline. The longer-term direction is to extend the same agent architecture to embodied robotics, where agents may operate continuously for days or weeks rather than short isolated sessions.

## Why Simulation First

The simulation environment is not the main novelty by itself. It is the controlled testbed for studying agent behavior. Starting with simulation allows fast iteration, repeatable experiments, and easier debugging before connecting the architecture to physical hardware.

The project can begin with a simple grid-world or MiniGrid-style environment before moving to more complex simulation tools such as MuJoCo, Habitat, Isaac Sim, or a robotics platform later.

## Project Objective

Build a working software system where an autonomous agent can:

- Observe a simulated environment
- Maintain short-term and long-term memory
- Select and prioritize goals
- Plan and execute actions
- Record why it took each action
- Generate decision traces and explanations
- Detect changes in behavior over time

## Key Research Question

Can long-lived autonomous agents remain accountable as their memory, goals, and behavior evolve over time?

Supporting questions:

- Can an external observer reconstruct why the agent took a specific action?
- Which memories influenced the agent's decisions?
- Does the agent's behavior drift over long runs?
- Can drift be detected before it causes undesirable outcomes?
- Does accountability improve transparency without significantly reducing task performance?

## Proposed Architecture

```text
Simulation Environment
        ↓
Observation Interface
        ↓
Agent Brain
  - LLM Reasoning
  - Memory Retrieval
  - Goal Selection
  - Planning
        ↓
Action Executor
        ↓
Environment Update
        ↓
Accountability Logger
        ↓
Evaluation + Visualization Dashboard
```

## Milestone-Based Development Plan

### Milestone 0: Repository and Project Skeleton

Goal: Establish a clean engineering foundation.

Deliverables:

- GitHub repository
- Python project structure
- README
- Basic simulation runner
- Configuration files
- Experiment logging folder

Success criteria:

- Project runs locally with one command
- Simple environment can reset and step forward

---

### Milestone 1: Minimal Simulation Environment

Goal: Create the simplest possible testbed.

Environment options:

- Custom Python grid world
- MiniGrid
- Gymnasium environment

Initial entities:

- Agent
- Food/resource
- Charging station
- Obstacles
- Goal location

Success criteria:

- Agent can observe the environment
- Environment accepts actions
- State changes are logged

---

### Milestone 2: Basic LLM Agent Loop

Goal: Add a simple autonomous agent.

Core loop:

```python
observation = env.observe()
decision = agent.think(observation)
action = agent.choose_action(decision)
env.step(action)
```

Success criteria:

- Agent can complete a simple task
- Agent actions are valid
- Basic reasoning output is captured

---

### Milestone 3: Persistent Memory

Goal: Give the agent memory across steps and episodes.

Memory types:

- Episodic memory: what happened before
- Semantic memory: learned facts about the world
- Reflection memory: lessons learned from prior outcomes

Possible implementation:

- SQLite or JSONL for early version
- Vector store such as Chroma or FAISS for retrieval

Success criteria:

- Agent can retrieve relevant past experiences
- Agent behavior changes based on memory
- Memory references are logged per action

---

### Milestone 4: Goal Management and Planning

Goal: Allow the agent to reason over competing goals.

Example goals:

- Maintain energy
- Explore the environment
- Collect resources
- Avoid obstacles
- Complete assigned tasks

Success criteria:

- Agent selects goals explicitly
- Goal selection is logged
- Agent can balance competing priorities

---

### Milestone 5: Accountability Layer

Goal: Make agent decisions explainable and auditable.

For each significant action, log:

- Observation
- Retrieved memories
- Active goal
- Candidate plans
- Final action
- Explanation
- Outcome

Success criteria:

- A human reviewer can reconstruct why an action was taken
- The system can generate a readable decision trace
- Logs are structured enough for evaluation

---

### Milestone 6: Long-Horizon Runs

Goal: Run the agent for hundreds or thousands of steps.

Measure:

- Task success
- Survival/resource maintenance
- Repeated failures
- Memory growth
- Goal changes
- Behavior patterns

Success criteria:

- Agent can operate over long simulations
- Behavior can be replayed and analyzed
- Failure modes become visible

---

### Milestone 7: Behavioral Drift Detection

Goal: Detect when agent behavior changes meaningfully over time.

Possible drift signals:

- Change in action distribution
- Change in goal priority
- Increased rule violations
- Repeated avoidance of important tasks
- Decreased task completion rate
- Changes in explanation patterns

Success criteria:

- Drift score can be computed
- Drift events can be visualized
- System can explain likely causes of drift

---

### Milestone 8: Evaluation Harness

Goal: Compare different agent designs.

Example variants:

- Baseline reactive agent
- LLM-only agent
- LLM + memory
- LLM + memory + reflection
- LLM + memory + accountability layer

Evaluation dimensions:

- Task completion
- Consistency
- Explainability
- Auditability
- Drift detection
- Latency/cost

Success criteria:

- Repeatable experiments
- Results table
- Clear comparison between approaches

---

### Milestone 9: Dashboard and Demo

Goal: Create a polished capstone demo.

Dashboard views:

- Environment replay
- Agent action timeline
- Memory timeline
- Goal evolution
- Decision trace viewer
- Drift detection report

Success criteria:

- Demo tells a clear story
- User can inspect why the agent acted
- Final system is portfolio-ready

## How Working With the Simulator Would Work

The simulator should be treated as the agent's temporary body and world. The agent does not need to know whether it is controlling a grid-world character, a MuJoCo robot, or a real robot. It only needs a consistent interface.

A clean interface could look like this:

```python
class Environment:
    def reset(self):
        pass

    def observe(self):
        pass

    def step(self, action):
        pass

    def render(self):
        pass
```

The agent receives observations and returns actions:

```python
observation = env.observe()
action, trace = agent.act(observation)
next_state, reward, done, info = env.step(action)
logger.record(observation, action, trace, next_state)
```

This allows the same brain/accountability architecture to work across different embodiments:

```text
Simple Grid World → MiniGrid → MuJoCo → Physical Robot
```

The capstone should start with the simplest simulator that can support meaningful evaluation. MuJoCo can be a later milestone or stretch goal, not the starting dependency.

## Recommended Repository Structure

```text
accountable-embodied-agents/
├── README.md
├── pyproject.toml
├── .env.example
├── configs/
│   ├── baseline.yaml
│   ├── memory_agent.yaml
│   └── accountability_agent.yaml
├── src/
│   └── accountable_agents/
│       ├── envs/
│       │   ├── gridworld.py
│       │   └── adapters.py
│       ├── agents/
│       │   ├── base.py
│       │   ├── llm_agent.py
│       │   └── memory_agent.py
│       ├── memory/
│       │   ├── episodic.py
│       │   ├── semantic.py
│       │   └── retrieval.py
│       ├── planning/
│       │   └── planner.py
│       ├── accountability/
│       │   ├── logger.py
│       │   ├── traces.py
│       │   └── explanations.py
│       ├── evaluation/
│       │   ├── metrics.py
│       │   ├── drift.py
│       │   └── experiments.py
│       └── dashboard/
│           └── app.py
├── experiments/
│   ├── run_experiment.py
│   └── results/
├── notebooks/
├── tests/
└── docs/
    ├── proposal.md
    ├── architecture.md
    └── evaluation_plan.md
```

## Initial Tech Stack

Suggested starting stack:

- Python
- Gymnasium or custom grid world
- OpenAI/Anthropic/local LLM API
- SQLite or JSONL for logs
- Chroma or FAISS for vector memory
- Streamlit for dashboard
- Pandas/Matplotlib for evaluation
- Pytest for basic testing

Optional later:

- MiniGrid
- MuJoCo
- LangGraph
- Docker
- FastAPI

## Practical First Sprint

The first sprint should avoid complexity.

Build:

1. A simple grid world
2. A rule-based baseline agent
3. An LLM agent that can choose from valid actions
4. JSONL logging of every step
5. A small replay script

Do not start with MuJoCo, vector databases, or complex RL. The goal is to prove the loop works first.

## Capstone Positioning

This project is not primarily about building a robot or inventing a new neural network architecture. The contribution is the end-to-end AI engineering system for evaluating persistent autonomous agents:

- Memory
- Planning
- Goal evolution
- Accountability
- Behavioral drift
- Evaluation

The simulator is the experimental testbed. The long-term vision is embodied AI and robotics.
