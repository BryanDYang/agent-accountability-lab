# Guardian Agent

Guardian Agent is a capstone project exploring observable context governance for reliable coding agents. The proposed workbench shows what candidate context was considered, which governance decisions were made, what exact input reached the coding model, and how governed and ungoverned runs differed.

The repository is currently focused exclusively on the Milestone 1 submission: the problem, target users, value proposition, high-level architecture, evaluation plan, team responsibilities, feasibility, risks, and pitch artifacts. Implementation decisions and prototype work are intentionally deferred to Milestone 2.

## Source of truth

The authoritative milestone 1 scope is [Project Proposal](docs/milestone_1/project_proposal.md).

Milestone 1 includes a concise evaluation direction in the project proposal. Detailed formulas, statistical methods, and threshold calibration are deferred to the draft [Milestone 2 Evaluation Plan](docs/milestone_2/evaluation_plan.md).

Deferred project-readiness decisions, repository setup, model integration, pilot evaluation, and final threshold calibration are tracked in the [Milestone 2 TODO](docs/milestone_2/TODO.md).

The interactive product concept is available as a dependency-free [HTML mockup](docs/mockup/index.html). Open the file directly in a browser to explore the candidate context, governance trace, exact model input, and governed-versus-ungoverned comparison.

The proposed six-slide presentation is available as a [Milestone 1 Pitch Deck Draft](docs/milestone_1/pitch_deck.md). Export and visual verification remain submission tasks.

Historical planning documents are retained in [docs/archive](docs/archive/README.md) for decision history only. They are not current requirements.

## Repository structure

```text
docs/
├── mockup/
│   ├── index.html
│   └── capstone_workflow_diagram.drawio
├── milestone_1/
│   ├── pitch_deck.md
│   └── project_proposal.md
├── milestone_2/
│   ├── TODO.md
│   └── evaluation_plan.md
└── archive/
    └── milestone_1/
```

## License

This project is licensed under the [MIT License](LICENSE).
