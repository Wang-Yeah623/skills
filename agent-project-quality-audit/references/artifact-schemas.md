# Quality artifact schemas

Keep artifacts under `.quality/` unless `quality_dir` is explicitly overridden. When using an external directory, record the target’s absolute path and Git commit or snapshot identifier in every run report.

```text
.quality/
├── project-map.md
├── acceptance.md
├── risk-register.md
├── coverage-matrix.md
├── audit-queue.md
├── issue-ledger.jsonl
└── runs/
    └── YYYY-MM-DDTHHMMSSZ-<scope>.md
```

## `project-map.md`

Include:

- project purpose and users;
- language, frameworks, build/runtime requirements;
- module and directory responsibilities;
- entry points and key call chains;
- core user journeys;
- data and state lifecycle;
- persistence and external dependencies;
- trust boundaries, permissions, background work, retry/timeout/recovery;
- build, start, test, lint, and static-check commands;
- existing test coverage by behavior;
- facts, inferences, and unresolved questions in separate sections;
- version evidence: Git commit/branch/dirty state, or snapshot identifier when Git is absent.

## `acceptance.md`

Each acceptance item must be observable and have:

| Field | Meaning |
|---|---|
| `AC-ID` | Stable identifier such as `AC-001` |
| Behavior | User- or operator-visible requirement |
| Verification | Command, test, or manual procedure |
| Evidence | Current result and artifact location |
| Status | `unknown`, `failing`, `passing`, or `blocked` |
| Source | Product fact, document, test, or inference |

Never silently turn an inferred product requirement into an authoritative one.

## `risk-register.md`

Use one row per bounded area:

| Area | Impact | Likelihood | Coverage gap | Change frequency | External dependency | Uncertainty | Total | Rationale | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|

Score dimensions 1–5. `Total` is their sum. Explain each score briefly. Allowed status values: `queued`, `in-progress`, `covered`, `partially-covered`, `blocked`, `accepted`.

## `coverage-matrix.md`

For every critical flow or area, record the latest evidence for:

- static analysis;
- unit tests;
- integration tests;
- end-to-end tests;
- real start/run;
- failure paths;
- repeatability/flakiness;
- concurrency/idempotency when relevant.

Use `none`, `partial`, `pass`, `fail`, `blocked`, or `not-applicable`, plus a link or command for any non-`none` claim.

## `audit-queue.md`

Order remaining scopes by current priority. Each entry includes scope, score, reason, prerequisites, explicit exclusions, and whether product input or extra permission is needed. Completed scopes remain traceable through the coverage matrix and run reports rather than being silently deleted.

## `issue-ledger.jsonl`

Store one JSON object per line. Use stable IDs such as `QA-YYYYMMDD-NNN`. Required keys may contain `null` while work is incomplete:

```json
{"id":"QA-20260718-001","discovered_at":"2026-07-18T12:00:00Z","area":"session restore","severity":"P1","symptom":"...","impact":"...","evidence":["command or file:line"],"reproduction":"...","root_cause":null,"fix":null,"regression_test":null,"validation":null,"status":"hypothesis","classification":"unclassified"}
```

Allowed `severity`: `P0`, `P1`, `P2`, `P3`.

Allowed `status`: `hypothesis`, `confirmed`, `fixing`, `fixed`, `verified`, `wont-fix`, `closed`.

Allowed `classification`: `unclassified`, `new-defect`, `recurrence`, `regression`, `latent`, `environment`, `false-positive`.

Evidence grades:

- `A`: stable runtime reproduction and captured output;
- `B`: deterministic test/compiler/tool proof or decisive executable check;
- `C`: strong static path without executable confirmation;
- `D`: plausible but incomplete hypothesis.

Only A/B evidence normally supports `confirmed`. If an indisputable static contradiction is treated as confirmed, explain why execution is unnecessary. `fixed` or `verified` requires non-empty regression and validation evidence.

## `runs/<timestamp>-<scope>.md`

Include:

- target, snapshot/commit, environment, mode, authority, and budget;
- selected scope, reason, exclusions, and success criteria;
- commands/checks run with exit codes and sanitized results, including baseline or pre-existing failures;
- confirmed issues, hypotheses, and ruled-out candidates;
- pre-fix and post-fix evidence when source changed;
- validation layers passed, failed, blocked, or skipped;
- files changed and unrelated user changes preserved;
- final diff or changed-file review;
- artifacts updated;
- uncovered risks and one recommended next scope.

Do not paste secrets or massive logs. Store a concise excerpt, checksum, or safe artifact path when full evidence is large.
