# Agent Accountability Lab: Six-Slide Pitch Deck Draft

## Slide 1: Agent Accountability Lab

### Visual context governance for reliable coding agents

See what context was considered, what was rejected, what reached the model, and what changed.

**CIS-5980 | AI Engineering**  
Bryan Yang, Will Liu, and Guadalupe Cantera

**Visual direction:** Minimal white canvas with a thin blue evidence line connecting a task, decision ledger, and coding agent.

## Slide 2: Relevant context can still be wrong

Coding agents combine information from many sources:

- User tasks and target files
- Repository and directory rules
- Company and library documentation
- Retrieved files and tool output
- Memories from previous runs

Those sources can be stale, out of scope, duplicated, untrusted, or mutually inconsistent.

Developers often see the request and final answer without seeing what context was considered, why a source was removed, or what exact input reached the model. Context failures therefore become difficult to explain, reproduce, and evaluate.

**Visual direction:** Several source fragments converge toward a coding model. Highlight the missing evidence between collection and execution.

## Slide 3: Governance becomes an inspectable evidence chain

```text
Task + controlled candidate context
                 ↓
Deterministic governance decisions
ADMIT | REJECT | QUARANTINE | DEDUPLICATE
                 ↓
Decision ledger + exact compiled input
                 ↓
Coding model under the assigned condition
                 ↓
Edits, tests, violations, tokens, and latency
```

The coding model receives either the complete ungoverned candidate set or the governed context bundle. The decision ledger preserves provenance, reason codes, policy versions, the exact model request, and evaluated outcomes.

**Visual direction:** Use one horizontal five-stage flow. A blue evidence trail should continue from candidate context through the final outcome.

## Slide 4: The same task is tested with and without governance

### Common controlled inputs

- Repository revision
- User request and target files
- Candidate set and available tools
- Coding model and parameters
- Trial seed when supported

### Paired conditions

**Without governance:** Every candidate enters model context.  
**Governance enabled:** Deterministic policies filter, scope, deduplicate, order, and reason-code candidates before inference.

### Evidence compared

- Invalid-context admission and false rejection
- Task success and repository-rule violations
- Input, output, and governance tokens
- Governance and total latency
- Decision clarity and trace completeness

**Key principle:** Token reduction alone does not count as success.

**Visual direction:** Split the slide into ungoverned and governed runs with one shared input rail and one shared outcome rail.

## Slide 5: The first build is intentionally narrow and bounded

### Provisional implementation

- React, TypeScript, and Vite
- Python 3.12 and FastAPI
- SQLite evidence storage
- Provider-neutral model adapter
- Pytest and Playwright evaluation
- CSS custom properties and a small project-owned component vocabulary

### Provisional operating limits

- **60 task-model runs:** six scenario classes, two conditions, five repeats
- **$50:** total hosted-model API cap
- **$20:** maximum short-lived deployment cost; $0 preferred
- **16 GB memory and 20 GB storage:** minimum local-model planning assumption

### Data and safeguards

- Team-authored synthetic repositories and fixtures
- Source and license inventory before fixture freeze
- No employer code, customer data, private chats, credentials, or student records
- Disposable repositories, restricted tools, secret checks, and no production access
- Quarantine unresolved high-risk conflicts and state evaluation limitations clearly

**Visual direction:** Use three broad regions for implementation, operating limits, and safeguards. Emphasize the numeric limits without presenting them as measured results.

## Slide 6: Milestone 1 aligns the plan before code

### Complete in the current draft

- Problem, target users, and value proposition
- High-level architecture and evaluation direction
- Provisional technology and budget assumptions
- Data, licensing, ethics, and safety plans
- Early fixture-access and licensing checkpoint

### Before submission

- Confirm team ownership and weekly check-in
- Verify requirements against the official Canvas rubric
- Export and visually verify the pitch deck
- Assemble the final submission PDF

### Deferred to Milestone 2

- Exact model selection and integration
- Governance contracts and executable scenarios
- Pilot runs and final metric thresholds
- CI and optional comparison-model work

### Feedback requested

1. Is the workbench sufficiently differentiated from a prompt builder?
2. Is deterministic context governance the right MVP boundary?
3. Does the paired evaluation support the proposed reliability claim?

**Visual direction:** Close with three steps: approve the plan, build one narrow scenario, and calibrate after the pilot.
