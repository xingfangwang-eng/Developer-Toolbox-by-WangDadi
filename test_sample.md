﻿﻿﻿﻿﻿﻿﻿# test-project: Core Architecture & Technical Specification

## 1. Lock-Free Concurrent Test Execution Engine with Microsecond Latency Tracking

The foundation of **test-project** is a **lock-free, asynchronous execution engine** architected for high-frequency demo validation under extreme load. It leverages `Goroutine` pools (Go) or `asyncio` task groups (Python) to sustain **10,000 concurrent test sessions** per node with zero context-switching overhead.

- **Parameter Name:** `--concurrency-level` (integer, default: `1000`, max: `10000`)
- **Latency Measurement:** Each request is timestamped using `CLOCK_MONOTONIC_RAW` with **microsecond precision** (`µs`). The engine computes P50, P95, P99, and P99.9 latencies in real-time via a **sliding window histogram** (window size: 10,000 samples).
- **Data Persistence:** Results are streamed to a **PostgreSQL** database through a dedicated `COPY` pipeline, achieving an ingestion rate of **50,000 events/second** without blocking the test loop. The pipeline uses `batch_size=500` and `flush_interval=100ms` to balance throughput and latency.
- **Feature:** The engine automatically detects "thundering herd" patterns using a **rolling variance monitor** (window size: 100ms). When variance exceeds `0.8`, it applies a **jitter-based backoff** algorithm (`base_delay * random(0.5, 1.5)`) to prevent server overload during demo stress tests. The backoff factor is logged as `backoff_factor` in each event.

## 2. Property-Based Test Data Fuzzer with Stateful Workflow Validation

This component dynamically generates **edge-case test data** based on a user-defined JSON Schema (draft-07). It is not a simple random generator; it uses **property-based testing** (inspired by QuickCheck) to find hidden bugs in demo APIs through **exhaustive state space exploration**.

- **Parameter Name:** `--fuzz-depth` (integer, default: `3`, range: `1-5`)
- **Technical Indicator:** At depth `5`, the fuzzer generates **over 2^32 unique combinations** of input parameters (e.g., `null`, `NaN`, `negative timestamps`, `Unicode overflow`, `nested 10-level JSON`). The combinatorial explosion is controlled via a **pruning algorithm** that discards semantically equivalent inputs.
- **Integration:** It hooks into the execution engine via a **gRPC interceptor** that validates each response against the schema in **<5ms** average time (measured using `CLOCK_THREAD_CPUTIME_ID`). Non-conforming responses are flagged with an exact `JSONPath` pointer (e.g., `$.data.items[3].id`) and logged to a dedicated `schema_violations` table in PostgreSQL.
- **Feature:** The fuzzer supports **stateful testing** for demo workflows (e.g., "create user -> update email -> delete user"), ensuring that the sequence of operations respects the application's finite state machine. State transitions are validated against a **deterministic finite automaton (DFA)** defined in the `--stateful-flow` parameter.

## 3. Automated Regression Diffing with Semantic Versioning Analysis

After each test run, **test-project** generates a **structured diff report** comparing the current results against a baseline (stored in a local `.test-baseline` directory). This goes beyond simple text comparison by employing **statistical divergence metrics** and **semantic versioning** for change detection.

- **Parameter Name:** `--baseline-tag` (string, e.g., `v1.2.3`)
- **Technical Indicator:** The diff engine uses **Levenshtein distance** for string fields and **statistical KL-divergence** for latency distributions. A regression is flagged if the KL-divergence exceeds a threshold of `0.15`. For numeric fields, it uses **Cohen's d effect size** with a threshold of `0.8`.
- **Output:** The report is exported as a **JSON file** (`report-{timestamp}.json`) containing:
  - `new_failures`: List of test IDs that passed in baseline but failed now.
  - `latency_regressions`: List of endpoints where P99 increased by >20%.
  - `schema_drift`: Detected fields that changed type (e.g., `int` -> `string`) or constraints (e.g., `minLength` changed from `3` to `5`).
- **Feature:** This tool can automatically create a **GitHub Issue** via the API if the `--auto-create-issue` flag is set to `true`, including the diff report as a markdown table. The issue title is prefixed with `[Regression]` and includes the baseline tag and timestamp.

---

## Step-by-Step Operational Guide

### Step 1: Initialize the Project and Establish Baseline
```bash
# Create a new test-project workspace with a PostgreSQL connection string
test-project init --db-url "postgres://user:pass@localhost:5432/test_demo?sslmode=disable" --project-name "my-demo" --baseline-dir ./.test-baseline

# Run a baseline test to establish performance metrics
test-project run --concurrency-level 500 --duration 60s --baseline-tag v1.0.0 --output-format json
```
This creates a `.test-baseline/v1.0.0/` directory containing the raw latency histograms (stored as parquet files), response schemas (as JSON Schema), and a `baseline_metadata.json` file with run parameters. The baseline is automatically tagged in the PostgreSQL database with `baseline_id = v1.0.0`.

### Step 2: Execute a Fuzzing Campaign with Stateful Workflow
```bash
# Launch a fuzzing session targeting the /api/v1/users endpoint
test-project fuzz --target "https://demo-api.example.com/api/v1/users" --fuzz-depth 4 --stateful-flow "create,update,delete" --output-dir ./fuzz-results --grpc-endpoint "localhost:50051"

# Monitor live stats
test-project stats --watch --interval 5s
```
The tool will output live stats to `stdout` every 5 seconds, showing:
- `states_explored`: Number of unique state transitions (e.g., `create->update->delete`)
- `schema_violations`: Count of responses that deviate from the schema, with `jsonpath` pointers
- `coverage_pct`: Percentage of DFA states visited (target: >95%)
- `mean_latency_us`: Average latency per request in microseconds

### Step 3: Compare Against Baseline and Generate Regression Report
```bash
# Run a new test and compare against the baseline
test-project run --concurrency-level 1000 --duration 120s --compare-with v1.0.0 --auto-create-issue true --github-token ${GITHUB_TOKEN} --repo "myorg/myrepo"

# View the regression report locally
cat regression-report-{timestamp}.json | jq '.latency_regressions'
```
If regressions are found, a file named `regression-report-{timestamp}.json` is saved locally, and a GitHub issue is created with the following summary:
```
**Regression Detected**: 2 new failures, P99 latency on /api/v1/orders increased by 35%.
**Schema Drift**: Field `$.data.items[].price` changed from `number` to `string`.
**Suggested Action**: Review commit range `a1b2c3d..e4f5g6h` for changes to `/api/v1/orders`.
```

---

## Industry Best Practices

### 1. **Treat Your Baseline as a Living Artifact**
- **Best Practice:** Version your baseline data (`.test-baseline/`) in the same repository as your application code. Use Git tags to align test baselines with release versions. Configure `--baseline-retention` to keep the last 10 baselines and auto-purge older ones.
- **Why:** This allows for **bisecting** a performance regression down to a specific commit. When a test fails, you can run `test-project diff --from v1.0.0 --to v1.1.0` to isolate the exact changeset that introduced the latency spike. Use `--diff-threshold 0.15` to control sensitivity.

### 2. **Use Fuzzing in CI/CD, Not Just Locally**
- **Best Practice:** Integrate `test-project fuzz` into your pre-merge CI pipeline with a **time-budget** (e.g., `--max-time 300s`). Set the `--fuzz-depth` to `3` for daily runs and `5` for weekly deep scans. Use `--stateful-flow` to test critical user journeys (e.g., "signup->login->purchase").
- **Why:** Shallow fuzzing (depth 3) catches obvious bugs quickly, while deep fuzzing (depth 5) uncovers rare race conditions and edge-case crashes. By running both on a schedule, you balance CI speed with thoroughness. Configure `--slack-webhook` to alert the
---

## Related Resources
- 👉 `https://www.wangdadi.xyz/?utm_source=github_local&lang=en`
