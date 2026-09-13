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

- Met with the professor and TA twice to discuss the revised project direction and received approval to proceed with a research meeting follow-through assistant.
- Updated the [Milestone 1 proposal](milestone_1/project_proposal.md) from the team's Word submission draft, covering the project charter, MVP, architecture, evaluation plan, responsible use, roles, timeline, and $75 planning budget.
- Clarified that proactive follow-through is a required MVP capability based on the professor discussion. Added scheduled reminders for outstanding commitments, user-configured delivery, cancellation and rescheduling after task changes, and corresponding evaluation and demo requirements.
- Revised the six-slide [pitch deck](milestone_1/pitch_deck.pptx) to emphasize follow-through between meetings, show reminder and completion examples, and align its scope with the proposal.
- Drafted the Milestone 2 evaluation-harness checkpoint with task owners: one synthetic three-meeting sequence, expected task states, an independent-meeting extraction baseline, and an offline scorer checked against correct and deliberately incorrect outputs.
- Set up the repository with an installable Python CLI scaffold, locked dependencies, setup and contribution documentation, and a GitHub Actions smoke-test workflow. The application remains a scaffold; meeting processing and reminder delivery are not implemented yet.
- Reviewed the professor's `agent-sandbox` as a reference for packaging, dependency management, and offline testing, and documented its provenance. It is a simulation framework, separate from the meeting-artifact pipeline.
- Checked the submission against the Milestone 1 assignment. Confirmed the six-slide limit, required proposal sections, repository files, GitHub issue labels, and successful hosted CI runs. All three local CLI tests, lint, and formatting checks passed.

## Planned next steps

- Replace the remaining project-name placeholders, assemble the proposal and pitch slides into the required single PDF, visually review the export, and confirm the Canvas deadline.
- Confirm the proposed next-milestone assignments: Will for transcript/task contracts and extraction, Bryan for CLI/import integration and the evaluation runner, and Guadalupe for fixtures, annotations, and evaluation design.
- Prepare and review the first synthetic three-meeting development sequence, including completion, a changed deadline, an unaccepted suggestion, an ambiguous reference, and a task not mentioned again.
- Implement the transcript/task contract, independent-meeting extraction baseline, and offline scorer. Record the model and prompt versions and keep live API calls separate from CI.
- Confirm access to reusable sponsor components and the meeting-artifact format; start with timestamped transcript imports while audio integration is clarified.
- Select the initial follow-up delivery channel, scheduling defaults, supported OS, and calendar integration, then run a small model quality/cost pilot.

## Current blockers and dependencies

- **Meeting-pipeline and data access:** Access and permitted reuse of the sponsor's recording/transcription pipeline and any pre-recorded research-meeting sequences still need confirmation. Synthetic transcripts allow initial development to proceed.
- **Evaluation ground truth:** The annotation guide, labeled sequence, and scorer are planned but not yet implemented. The pilot dataset will support limited claims; broader evaluation depends on additional independent sequences.
- **Integration choices:** The first reminder delivery channel, OS/calendar integration, and model remain open decisions. Follow-up must work from validated task state and user-enabled settings.
- **Submission packaging:** A final combined PDF and project name are still needed. The deck passed structural checks, but its visual verification remains incomplete because the preview export failed.
