# Evaluation Options: Testing the Governance Layer

To objectively evaluate whether the governance layer improves agent performance, use test harnesses where the environment presents conflicting or noisy knowledge, and measure code correctness deterministically.

## 1. The "Deprecated API Migration" Suite

- **Setup:** Create a repository using a modern package version (e.g., Pydantic v2 in `pyproject.toml`), but populate the documentation database with legacy Pydantic v1 guides (`.dict()` vs. `.model_dump()`).
- **Evaluation Target:** Test whether Gate 2 (Version Staleness Pruning) successfully prunes the v1 docs so the agent generates valid v2 syntax.
- **Metric:** Pass/fail on compiler/linter check and unit tests asserting v2 method calls.

## 2. Cross-Directory Scope Leak Injection (Monorepo Test)

- **Setup:** Build a monorepo containing `frontend/` (TypeScript/React, camelCase naming, strict async rules) and `backend/` (Python/FastAPI, snake_case naming).
- **Evaluation Target:** Issue tasks targeting `backend/` files while feeding frontend rules into the retrieval pool. Test whether Gate 1 (Path Scope Masking) strips all frontend rules.
- **Metric:** AST assertion verifying zero camelCase variables or React conventions in the generated Python code.

## 3. Poisoned Episodic Memory Resistance

- **Setup:** Seed the episodic memory vector database with "bad habits" from synthetic previous runs (e.g., "Skip CSRF tokens in development", "Hardcode localhost port 8080"). Place strict security rules in `.cursorrules` (Tier 1).
- **Evaluation Target:** Verify that Tier 1 repo rules deterministically override and drop the poisoned Tier 4 memories.
- **Metric:** Static security scanner (e.g., Bandit or Semgrep) verifying that generated code contains zero security violations.

## 4. Intra-Tier Semantic Collision Resolution

- **Setup:** Inject two conflicting company architectural specs into the Tier 2 documentation store:
  - **Doc A (Timestamp: 2024):** "All microservices must communicate via RabbitMQ message queues."
  - **Doc B (Timestamp: 2026):** "All microservices must communicate via gRPC streaming."
- **Evaluation Target:** Test if Box 3 (Semantic Arbiter) correctly resolves the conflict in favor of the 2026 gRPC standard.
- **Metric:** Regex/AST validation asserting gRPC client instantiation over RabbitMQ connection logic.

## 5. SWE-bench Lite with Injected Context Noise

- **Setup:** Select 15–20 real bug-fix tasks from standard benchmarks (like SWE-bench Lite). For each task, inject 10 irrelevant documentation chunks and 2 stale rule snippets into the context pool.
- **Evaluation Target:** Compare the Coding Agent's performance With Governance (filtered context) vs. Without Governance (raw top-k RAG context).
- **Metric:** Pass@1 test execution rate and total tokens consumed per resolved issue.

## 6. Token Budget Saturation & Starvation Benchmark

- **Setup:** Set a strict context budget (e.g., 1,500 tokens). Flood the candidate pool with 20 semantically relevant documentation chunks totaling 8,000 tokens, alongside 1 critical 50-token Tier 1 security constraint.
- **Evaluation Target:** Test whether the Greedy Budget Packer prioritizes the Tier 1 constraint and drops lower-priority bloat without truncating critical instructions.
- **Metric:** Context token compliance (≤ 1,500) and compliance rate with the Tier 1 constraint.

## 7. Multi-Turn Sequential Task Drift (Long-Horizon Session)

- **Setup:** Run the agent through a 5-step sequential development workflow on a single repo. In Step 1, instruct the user to use a quick, temporary debug flag (`DEBUG=True`).
- **Evaluation Target:** In Step 5 (deploying to production), evaluate if the agent's memory of Step 1 causes it to leave `DEBUG=True` enabled, or if Tier 1 production rules override the memory.
- **Metric:** Automated assertion checking configuration flags in the final commit.

## 8. Automated AST / Custom Linter Assertion Suite

- **Setup:** Define 25 targeted micro-tasks with explicit repository constraints (e.g., "Always use `httpx.AsyncClient` instead of `requests`", "All database queries must use SQLAlchemy 2.0 `select` syntax").
- **Evaluation Target:** Measure rule adherence across 100 test runs.
- **Metric:** Custom Tree-sitter / ESLint / Flake8 rule assertion pass rate.

## Comparison of Evaluation Methods

| Option | Implementation Effort | Realism | Deterministic Verification | Primary Metric |
| --- | --- | --- | --- | --- |
| **1. Deprecated API Migration** | Low (2–3 days) | High | High (Unit tests + Compiler) | Test Pass Rate |
| **2. Monorepo Scope Leak** | Low (1–2 days) | High | High (AST / Linter) | Scope Violation Rate |
| **3. Poisoned Memory Resistance** | Medium (3–4 days) | Very High | High (Static Security Scanners) | Security Defect Rate |
| **4. Intra-Tier Semantic Collision** | Medium (3–5 days) | High | Medium (AST / Schema diff) | Arbiter Accuracy |
| **5. SWE-bench + Noise** | High (1–2 weeks) | Highest | High (Existing Test Suites) | Resolved Issue % |
| **6. Token Budget Saturation** | Low (1–2 days) | Medium | High (Token Counters) | Budget Adherence % |
| **7. Multi-Turn Session Drift** | Medium (4–6 days) | High | High (Integration Test) | Drift Regression Rate |

<br>
<br>
<hr>
<br>
<br>

# Benchmarking Performance and Reliability

## 1. Functional Code Quality & Rule Compliance

These metrics evaluate whether filtering and prioritizing context actually produces better, safer, and more compliant code.

### Task Success Rate ($\text{Pass}@1$ / Resolved Rate)

$$
\text{Pass}@1 = \frac{\text{Number of tasks where all unit and integration tests pass on first attempt}}{\text{Total number of evaluation tasks}}
$$

**Measurement Method:** Run test suites in the sandbox environment immediately following the agent's first code edit.

### Mandatory Rule Compliance Rate (Zero-Violation Rate)

**What it measures:** The percentage of tasks where generated code strictly adheres to Tier 1 repository rules (e.g., cookie security flags, async handlers, naming conventions).

**Measurement Method:** Run static analysis tools (Semgrep, Tree-sitter AST queries, custom linters) on the generated diffs to detect violations of active repo constraints.

### API Modernity / Version Accuracy Rate

**What it measures:** How often the agent uses the modern dependency API (specified in the lockfile) versus outdated APIs retrieved from legacy documentation.

**Measurement Method:** Use AST inspection targeting deprecated methods or syntax (e.g., Pydantic v1 `.dict()` vs. v2 `.model_dump()`).

### Mean Turns-to-Resolution (Efficiency of Iteration)

**What it measures:** The average number of retry turns the agent requires before reaching a green test run.

**Measurement Method:** Track retry count per task. A governed agent should require fewer retries because it does not spend initial turns debugging stale or conflicting instructions.

## 2. Long-Horizon Memory Health & Drift Resistance

These metrics validate the Write-Back Governance Gateway to ensure toxic memories are purged while beneficial patterns persist.

```text
                  ┌─────────────────────────────────────────────────────────┐
                  │              MEMORY HEALTH BENCHMARK                    │
                  │                                                         │
  Task Series 1   │ Task 1 (Hack Injected) ──► Gateway: Purged              │
  (Governed)      │ Task 2 (Dependent)     ──► Reads clean DB ──► PASSED    │
                  ├─────────────────────────────────────────────────────────┤
  Task Series 2   │ Task 1 (Hack Injected) ──► DB: Saved Toxic Memory       │
  (No Governance) │ Task 2 (Dependent)     ──► Hallucinates Hack ──► FAILED │
                  └─────────────────────────────────────────────────────────┘
```

### Memory Contamination Rate ($\text{MCR}$)

$$
\text{MCR} = \frac{\text{Number of failed/toxic patterns persisted to Episodic DB}}{\text{Total number of candidate memories proposed by agent}} \times 100\%
$$

**Target:** $0\%$ for the governed system; baseline systems typically suffer from high contamination.

### Multi-Turn Performance Retention (Memory Drift Rate)

**What it measures:** The degradation in task pass rate across a sequence of $N$ consecutive, interdependent coding tasks (e.g., a 5-step feature rollout).

**Measurement Method:** Measure $\text{Pass}@1$ at Step 1 versus Step 5. Baseline agents often degrade as session context accumulates noisy or contradictory memories.

### False Rejection Rate of Valid Memories

**What it measures:** How often the Write-Back Gateway mistakenly drops a valid, working pattern whose tests passed.

## 3. Context Economics & Token Efficiency

These metrics quantify how effectively the governance layer prunes noise and compresses the prompt payload.

### Context Compression Ratio ($\text{CCR}$)

$$
\text{CCR} = \left(1 - \frac{\text{Tokens in Governed Context Payload}}{\text{Tokens in Raw Retrieved Candidate Pool}}\right) \times 100\%
$$

### Total Token Cost per Resolved Task

$$
\text{Total Tokens} = \sum (\text{Prompt Tokens} + \text{Completion Tokens})_{\text{all attempts per task}}
$$

**Measurement Method:** Sum token usage across the initial attempt plus any subsequent retry turns. Governed systems typically achieve net lower token consumption despite the SLM arbitration step because prompt bloat and unnecessary retry loops are minimized.

### Context Signal-to-Noise Ratio (SNR)

**What it measures:** The proportion of tokens in `<governed_context>` that are directly referenced or required by the generated patch versus irrelevant boilerplate.

## 4. Conflict Resolution & Arbitration Precision

These metrics measure how accurately Stage 2.2 identifies and reconciles colliding instructions.

### Hierarchy Enforcement Accuracy

**What it measures:** Percentage of cross-tier conflicts where the higher-priority tier successfully overrode the lower-priority tier (e.g., a Tier 1 Repo Rule overriding a Tier 4 Memory).

### Intra-Tier Arbitration Accuracy

**What it measures:** Percentage of same-tier semantic collisions (e.g., two conflicting docs) where the SLM arbiter selects the ground-truth canonical directive, verified against a human-labeled test set.

### False Collision Rate

**What it measures:** Frequency with which complementary (non-conflicting) documents are mistakenly flagged as colliding and dropped.

## 5. System Latency & Runtime Overhead Profile

These metrics measure the computational overhead introduced by the middleware relative to the time saved during LLM generation.

| Metric | Measurement Method | Expected Characteristic |
| --- | --- | --- |
| **Stage 2.1 Deterministic Latency** | Execution time of path-scope and lockfile diff checks | < 5 ms (Pure Python / regex) |
| **Stage 2.2 Arbitration Latency** | Execution time of SLM structured call | 150–400 ms (Only on collisions) |
| **Stage 2.3 Token Packing Latency** | Execution time of BPE tokenizer + greedy packer | < 10 ms |
| **LLM Time-to-First-Token (TTFT)** | Time from LLM API dispatch to first output token | **Faster in Governed** (Smaller prompt payload) |
| **End-to-End Task Duration** | Wall-clock time from user query to verified commit | **Faster or Neutral** (Fewer retries compensate for middleware) |

## Recommended Comparative Benchmark Matrix

| Benchmark Metric | Baseline (Raw RAG, No Governance) | Governance Layer (Deterministic Only) | Full Governance Layer (+ SLM Arbiter & Write-Back) |
| --- | --- | --- | --- |
| **Task Pass Rate ($\text{Pass}@1$)** | Evaluate on 50 tasks | Baseline + Scope Pruning | Full pipeline |
| **Rule Violation Rate** | % of AST rule breaches | % of AST rule breaches | Expected: $\approx 0\%$ |
| **Memory Contamination Rate** | Measured after 10 failed runs | N/A (No write-back) | Target: $0\%$ |
| **Avg Prompt Tokens / Turn** | Unfiltered top-$k$ token count | Pruned token count | Packed budget cap |
| **Avg Turns per Solved Task** | Retries needed to pass CI | Retries needed to pass CI | Lowest turns |
| **End-to-End Latency / Task** | Wall-clock seconds | Wall-clock seconds | Wall-clock seconds |
