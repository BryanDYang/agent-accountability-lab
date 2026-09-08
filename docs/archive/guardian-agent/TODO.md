# Milestone 2 TODO

These tasks are intentionally deferred until the Milestone 1 proposal, architecture, roles, and evaluation plan are approved.

## Prototype and model integration

- [ ] Select the primary local or open-source model and document the provider-neutral adapter boundary.
- [ ] Integrate the selected local or open-source model through the provider-neutral adapter.
- [ ] Implement one narrow end-to-end scenario with a valid rule, stale rule, and out-of-scope rule.
- [ ] Verify task input, candidate loading, exact model-input preview, and one ungoverned coding run.
- [ ] Decide whether a stronger comparison model is useful after the primary integration works.
- [ ] If justified, select and integrate the optional comparison model without making it a release blocker.

## Governance contracts

- [ ] Approve the initial source-precedence policy and reason-code vocabulary.
- [ ] Decide which candidate-context fields can be edited in the workbench.
- [ ] Review and approve the metric definitions and measurement policies before running the pilot.

## Pilot and evaluation calibration

- [ ] Review and refine the draft [Evaluation Plan](evaluation_plan.md) using the first pilot results.
- [ ] Run matched governed and ungoverned pilot trials using the same repository revision, task, candidate set, tools, and model configuration.
- [ ] Verify that the pilot records the complete evidence trace from candidates through decisions, exact model input, output, and scored outcome.
- [ ] Review pilot results for invalid-context admission, false rejection, task success, policy violations, tokens, and latency.
- [ ] Set final metric thresholds only after reviewing pilot effect sizes, variance, and failure cases.
- [ ] Use pilot findings to finalize the remaining scenario suite.

## Repository and follow-up

- [ ] Add a basic continuous-integration smoke-test workflow when executable project scaffolding exists.
- [ ] Create and verify the GitHub issue labels and repository settings needed for implementation work.
- [ ] Record teaching-staff feedback, resulting decisions, and next steps after Milestone 1 review.
