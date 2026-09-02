# Week 1

- Created repository document markdown files
  - README.md
  - LICENSE
  - CONTRIBUTING.md
  - CODE_OF_CONDUCT.md
  - CI integration via `.github/workflows/ci.yml` with a passing smoke test
- Created milestone_1 documents
  - pitch_deck.md
  - project_proposal.md
- Created a diagram workflow of the full scope of the project

# Week 2

## What needs to be done

- Create a train/val/test split of datasets
- Define how you judge candidate outputs, both quantitatively with automated scores and qualitatively with structured grading rubrics, using real input/output examples.
  - Create a LLM as a judge rubric (1 - 5) grading system to judge the Agent's output for assessing hallucination, completeness, reasoning coherence, or adherence to formatting constraints.
- Look for open source governance layers to benchmark against.

## What got done

- Refined the Milestone 1 proposal after the team meeting.
  - Narrowed the project to a visual context-governance workbench for coding agents.
  - Defined the governed, ungoverned, and prompt-only comparison conditions.
  - Clarified the MVP, stretch goals, out-of-scope work, risks, timeline, and requested faculty feedback.
  - Added preliminary choices for the React and TypeScript front end, FastAPI back end, SQLite storage, Pytest, and Playwright.
- Created a six-slide pitch deck draft aligned with the current proposal.
- Created and refined the project workflow diagram, including the decision ledger and the evidence path from candidate context to evaluated outcome.
- Expanded the evaluation planning.
  - Documented candidate benchmark scenarios such as deprecated API migration, cross-directory scope leakage, poisoned memory, context-budget saturation, and long-horizon drift.
  - Documented proposed reliability, rule-compliance, context-efficiency, conflict-resolution, and latency metrics.
  - Moved detailed formulas, statistical methods, and threshold calibration into the Milestone 2 evaluation plan so Milestone 1 stays focused on scope and direction.
- Added a Milestone 2 TODO list covering the prototype, model integration, governance contracts, pilot, and evaluation calibration.
- Added the weekly team journal and the repository code of conduct, and updated the README with the team name.

## Current blockers and decisions needed

- Select the first local or open-source coding model and runtime instead of leaving the model integration unspecified.
- Define the Phase 2 evaluation implementation in enough detail to connect each controlled fixture to automated policy checks, code tests, traces, and paired-run reports.
- Create the train, validation, and test split after the scenario fixture format and labeling rules are frozen.
- Agree on the LLM-as-judge rubric and determine which qualities require human review instead of automated scoring.
- Identify an appropriate open-source governance baseline for comparison.
