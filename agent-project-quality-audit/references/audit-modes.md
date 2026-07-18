# Audit modes

Use one mode per request. A mode controls authority, required artifacts, and stopping conditions.

## Mode selector

| Mode | Use when | Source changes | Stop condition |
|---|---|---:|---|
| `map` | First contact with an unfamiliar project | No | A usable project map exists |
| `bootstrap` | Establishing the quality system for the first time | No by default | Map, acceptance, risks, coverage, queue, and ledger exist; optionally one read-only scope is complete |
| `audit-readonly` | The user wants findings without code changes | No | One bounded scope is evidenced and recorded |
| `audit-fix` | The user explicitly requests confirmed defects to be repaired | Yes, after repair gate | One bounded scope is repaired or blocked and regression evidence is recorded |
| `next-cycle` | `.quality` history already exists | Depends on explicit authority | Highest-priority uncovered scope is completed once |
| `runtime-incident` | A concrete runtime failure, log, or operation is supplied | No until fix authority is clear | Incident is reproduced/classified, then repaired only if authorized |
| `verify-fix` | Reviewing whether a recent repair really worked | No by default | Verdict is `effective`, `partially effective`, `ineffective`, or `insufficient evidence` |
| `converge` | Several high-risk domains have already been audited | No by default | Release convergence is assessed against accumulated evidence |

## `map`

1. Inspect documentation, structure, manifests, entry points, state, persistence, integrations, tests, and run commands.
2. Separate fact, inference, and unknown.
3. Write `project-map.md` to the selected quality directory.
4. Do not list broad speculative defects or modify source.

## `bootstrap`

1. Complete `map` if no reliable map exists.
2. Derive acceptance criteria from repository evidence and supplied product facts.
3. Score risk areas and populate the coverage matrix and queue.
4. Initialize an empty JSONL issue ledger and `runs/`.
5. If budget permits, select one bounded scope and perform `audit-readonly`; otherwise stop after system creation.

## `audit-readonly`

1. Read existing quality history; bootstrap only missing minimum artifacts.
2. Select one high-priority, low-coverage scope.
3. Trace it end to end and attempt safe, non-mutating reproduction.
4. Record confirmed findings separately from hypotheses.
5. Update coverage, risks, queue, ledger, and a run report. Do not edit source.

## `audit-fix`

1. Perform the read-only evidence phase first.
2. Confirm explicit write authority and safe worktree state.
3. For each confirmed issue in the selected scope, establish fail-before evidence.
4. Apply the minimum root-cause fix and run layered validation.
5. Stop after the selected scope even when another issue appears; queue unrelated findings.

## `next-cycle`

1. Read all existing `.quality` artifacts and the latest run.
2. Do not rebuild the project map without evidence that it is stale.
3. Select the highest-priority uncovered or under-tested scope.
4. If a new symptom resembles an old item, classify it before acting: recurrence, regression, latent issue, environment issue, false positive, or new defect.
5. Complete one cycle and stop.

## `runtime-incident`

Capture actual input, environment, version/snapshot, configuration, and full sanitized error. Find the smallest stable reproduction, relate it to ledger history, trace the failing state transition, and add diagnostics when the evidence is insufficient. Never claim a fix for an unreproduced incident.

## `verify-fix`

Review the original issue record, diff, pre-fix evidence, regression test, and validation report. Check that the test fails on the old behavior and passes on the fixed behavior, the root cause was addressed, assertions were not weakened, adjacent behavior remains intact, project checks passed, and repeated execution is stable.

Return one verdict:

- `effective`: complete fail-before/pass-after and layered evidence;
- `partially effective`: target symptom improved but material evidence or scope remains;
- `ineffective`: recurrence, direct regression, or failing target evidence;
- `insufficient evidence`: required reproduction or validation is absent.

## `converge`

Use only after multiple bounded cycles. Review high-risk coverage, cross-module integration, recurrence/regression, executable acceptance checks, full build/test/start evidence, and unresolved release blockers. Return `not converged`, `near convergence`, or `meets current release standard`, with evidence and remaining gaps.
