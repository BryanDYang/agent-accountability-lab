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

# Week 3

## What got done

- Met with the professor and TA twice to discuss the project direction, scope, and next steps.
- Prepared a new proposal for a meeting follow-through assistant that tracks commitments, suggestions, and decisions across research meetings.
- Received approval for the new project direction.
- Continued refining the proposal, including the MVP scope, evaluation plan, team responsibilities, and data-handling requirements.
- Worked on the pitch deck to present the new project and its proposed workflow.
- Set up the repository for the new direction with an installable Python CLI scaffold, locked dependencies, updated setup documentation, and a GitHub Actions smoke-test workflow. All three CLI tests, lint, and formatting checks passed locally.
- Reviewed `agent-sandbox` as a reference for packaging, dependency management, and offline testing. It is a simulation framework; access to the separate meeting-artifact pipeline still needs confirmation.

## Planned next steps

- Finish the proposal and pitch deck for the Milestone 1 submission.
- Assemble the required submission PDF and include the repository URL and this weekly check-in.
- Confirm the proposed next-milestone ownership: Will for transcript/task contracts and extraction, Bryan for CLI/import integration, and Guadalupe for fixtures, annotations, and evaluation.
- Prepare one synthetic three-meeting development sequence with expected commitments, owners, source references, and task states after each meeting.
- Build the initial evaluation scorer and verify it against known correct and deliberately incorrect outputs before running the first extraction baseline.
- Confirm reusable sponsor components and the meeting-artifact format; begin with timestamped transcript imports while audio integration is being clarified.

## Current blockers and dependencies

- **Meeting-pipeline access:** `agent-sandbox` does not establish access to the recording/transcription pipeline. Confirm the artifact format and permitted reuse; synthetic timestamped transcripts allow development to proceed meanwhile.
- **Evaluation ground truth:** We still need a shared annotation guide and expected task states. Start with one small development sequence and resolve disagreements before expanding the dataset.
- **Model and operating assumptions:** Select a model after a small quality/cost pilot, and confirm the initial OS and calendar integration. Keep API calls out of the offline CI smoke tests.
- **Submission readiness:** Finish the proposal/deck consistency review and PDF packaging. Verify a successful hosted CI run and repository issue labels before submission; local checks alone do not confirm GitHub configuration.
