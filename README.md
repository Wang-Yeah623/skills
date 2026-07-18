<div align="center">

# 🧭 Agent Project Quality Audit

### Turn “audit the whole repo” into one bounded, evidence-backed quality cycle.

Risk map → one exact scope → reproduce → minimal repair → layered validation → persistent quality memory

[![GitHub stars](https://img.shields.io/github/stars/Wang-Yeah623/skills?style=for-the-badge&logo=github&label=Stars&color=111827)](https://github.com/Wang-Yeah623/skills/stargazers)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](agent-project-quality-audit/SKILL.md)
[![Beta](https://img.shields.io/badge/status-beta-f59e0b?style=for-the-badge)](#project-status)
[![Read-only by default](https://img.shields.io/badge/default-read--only-2563eb?style=for-the-badge)](#safety-by-default)

[Why it exists](#why-it-exists) · [Quick start](#quick-start) · [Workflow](#the-quality-cycle) · [Modes](#audit-modes) · [Artifacts](#persistent-quality-memory) · [简体中文](README.zh-CN.md)

</div>

> **In one sentence:** a reusable Codex Skill that maps software risk, confirms real defects, gates minimal fixes behind evidence and permission, and preserves every audit cycle under `.quality/`.

## Why it exists

“Scan the whole project and fix everything” sounds useful, but it usually produces broad guesses, unsafe edits, and the same rediscovery next week.

This Skill replaces that pattern with a small, repeatable contract:

| Vague agent audit | This Skill |
|---|---|
| Scans everywhere | Selects exactly one risk-ranked scope |
| Reports static suspicion as fact | Separates hypotheses from confirmed defects |
| Edits before reproducing | Requires fail-before evidence before a fix |
| Declares success after one green command | Runs layered validation and records limits |
| Forgets what was checked | Persists coverage, risks, issues, and run history |
| Treats repository instructions as authority | Treats an unfamiliar repository as untrusted input |

The result is not “AI found some bugs.” It is a reviewable chain:

```text
code or runtime evidence → minimal reproduction → classification → conclusion
```

## What you get

- **Risk-driven scope selection** — rank impact, likelihood, coverage gaps, change frequency, external dependencies, and uncertainty.
- **Evidence-controlled claims** — distinguish `hypothesis`, `confirmed`, `fixed`, and `verified` instead of collapsing them into one confident answer.
- **Test-first repair gate** — source changes happen only in `audit-fix` mode, after explicit authority and stable fail-before evidence.
- **Layered regression checks** — validate the reproduction, changed module, project checks, real runtime path, and repeatability as permitted.
- **Persistent quality memory** — maintain acceptance criteria, risks, coverage, queue, issue ledger, and per-cycle reports.
- **Safety boundaries** — inspect unknown scripts before execution and stop for credentials, production access, migrations, destructive actions, or scope expansion.
- **Built-in artifact validator** — check required Markdown records and JSONL ledger consistency with one Python script.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/Wang-Yeah623/skills.git
```

### 2. Install the Skill

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
cp -R skills/agent-project-quality-audit ~/.codex/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse "skills\agent-project-quality-audit" "$HOME\.codex\skills\"
```

Restart or refresh Codex so it can discover the Skill.

### 3. Run a safe first cycle

```text
Use $agent-project-quality-audit to map this repository and run one bounded,
read-only audit cycle. Keep quality artifacts outside the repository unless
I explicitly authorize repository changes.
```

The Skill defaults to `audit-readonly` when audit authority is ambiguous.

## The quality cycle

```mermaid
flowchart LR
    A["Map the repository"] --> B["Rank risks and coverage gaps"]
    B --> C["Select exactly one scope"]
    C --> D["Trace behavior and reproduce"]
    D --> E{"Fix explicitly authorized?"}
    E -- "No" --> F["Record finding or hypothesis"]
    E -- "Yes" --> G["Capture fail-before evidence"]
    G --> H["Apply the smallest root-cause fix"]
    H --> I["Run layered validation"]
    F --> J["Persist .quality evidence"]
    I --> J
    J --> K["Stop and recommend one next scope"]
```

Four rules keep the cycle honest:

1. **One cycle, one bounded scope.** Unrelated findings go to the queue.
2. **Evidence before confidence.** Static suspicion remains a hypothesis unless decisive proof exists.
3. **Permission before mutation.** Read-only means no source edits; repository-local `.quality` files are also modifications.
4. **Stop with limits recorded.** “No confirmed issue in this scope” is valid; “no issues” usually is not.

## Persistent quality memory

Each project can retain a machine-readable, human-reviewable quality system:

```text
.quality/
├── project-map.md          # architecture, flows, dependencies, unknowns
├── acceptance.md           # observable requirements and evidence
├── risk-register.md        # transparent six-factor priority scores
├── coverage-matrix.md      # static, unit, integration, E2E, runtime coverage
├── audit-queue.md          # next scopes and prerequisites
├── issue-ledger.jsonl      # stable issue history and classifications
└── runs/
    └── YYYY-MM-DDTHHMMSSZ-<scope>.md
```

Later cycles read this history first, extend uncovered areas, and avoid restarting from zero.

## Audit modes

| Mode | Best used for | Source changes |
|---|---|---:|
| `map` | First contact with an unfamiliar repository | No |
| `bootstrap` | Creating the quality system for the first time | No by default |
| `audit-readonly` | Evidence-backed findings without code edits | No |
| `audit-fix` | Repairing confirmed defects after the repair gate | Yes |
| `next-cycle` | Continuing from existing `.quality` history | Only if authorized |
| `runtime-incident` | Investigating a real error, log, or failed operation | Not until authorized |
| `verify-fix` | Checking whether a previous fix is actually effective | No by default |
| `converge` | Reviewing release convergence after several cycles | No by default |

See the complete mode contracts in [`references/audit-modes.md`](agent-project-quality-audit/references/audit-modes.md).

## Evidence and completion claims

| Claim | Minimum meaning |
|---|---|
| `hypothesis` | Plausible path, but reproduction or decisive proof is missing |
| `confirmed defect` | Stable runtime reproduction, deterministic tool/test proof, or an indisputable static contradiction |
| `fixed` | The target fails before the change and the same check passes after it |
| `verified` | Relevant regression layers pass and limitations are recorded |
| `release-ready` | High-risk coverage and executable acceptance evidence have been reviewed in `converge` mode |

Finding nothing in one run is never enough to claim that a project has no defects.

## Example requests

<details>
<summary><strong>Map an unfamiliar repository</strong></summary>

```text
Use $agent-project-quality-audit in map mode. Identify architecture, entry points,
core user journeys, state lifecycles, external dependencies, test commands,
facts, inferences, and unresolved questions. Do not execute project code.
```

</details>

<details>
<summary><strong>Run a bounded read-only audit</strong></summary>

```text
Use $agent-project-quality-audit in audit-readonly mode. Rank the current risks,
select exactly one high-risk low-coverage scope, trace it end to end, and record
confirmed defects separately from hypotheses. Do not modify source code.
```

</details>

<details>
<summary><strong>Repair one confirmed defect</strong></summary>

```text
Use $agent-project-quality-audit in audit-fix mode for the selected scope only.
Preserve unrelated changes, establish fail-before evidence, apply the smallest
root-cause fix, run layered validation, and update the .quality records.
```

</details>

<details>
<summary><strong>Verify a previous fix</strong></summary>

```text
Use $agent-project-quality-audit in verify-fix mode. Review the original issue,
diff, fail-before evidence, regression test, and validation results. Return only
effective, partially effective, ineffective, or insufficient evidence.
```

</details>

## Safety by default

An unfamiliar repository is treated as untrusted input.

- Documentation, source comments, logs, fixtures, and embedded prompts are data — not permission.
- Builds, tests, package installation, migrations, and run scripts may execute arbitrary code.
- Network calls, external services, credentials, production systems, destructive commands, and dependency installation require specific authority.
- Source editing is forbidden in `map`, `audit-readonly`, and investigation-only modes.
- Dirty worktrees and overlapping user changes must be preserved.
- Credentials, personal data, proprietary logs, and exploit-enabling details must be redacted from artifacts.

This is a software-quality workflow, not a penetration test, compliance audit, or substitute for a dedicated security review.

## Validate the artifacts

The bundled validator checks the minimum artifact set and JSONL ledger consistency:

```bash
python agent-project-quality-audit/scripts/validate_quality_artifacts.py <target-or-quality-dir> --profile map
python agent-project-quality-audit/scripts/validate_quality_artifacts.py <target-or-quality-dir> --profile system
python agent-project-quality-audit/scripts/validate_quality_artifacts.py <target-or-quality-dir> --profile audit
```

The validator checks structure. It does not prove that the audit conclusions are correct.

## Real-world forward test

The workflow has completed one deliberately narrow forward test on a real, large Rust coding-agent source snapshot.

| Item | Evidence |
|---|---|
| Authority | Strict read-only; quality records were written outside the target |
| Scope | One bounded file-reading contract path, not the whole repository |
| Artifacts | Seven `.quality` artifact types were generated and retained |
| Findings | One static contract inconsistency was confirmed; one memory-risk path remained a hypothesis |
| Validation | `map`, `system`, and `audit` validator profiles passed |
| Integrity | Target source hashes were unchanged before and after the cycle |
| Limits | No Cargo command, project test, process start, or project network call was executed |

This is evidence that the workflow can operate safely on a real repository snapshot — not a claim that the entire project was audited or that the Skill is universally compatible.

## Compatibility and prerequisites

| Item | Current status |
|---|---|
| Codex Skill discovery | Tested |
| Python | 3.9+ recommended for the bundled validator |
| Target language/framework | Language-agnostic workflow; breadth still under test |
| Other agent harnesses | Not yet verified |
| Repository access | Read access is enough for mapping; writes require explicit authority |

## Repository layout

```text
skills/
├── README.md
├── README.zh-CN.md
└── agent-project-quality-audit/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   ├── artifact-schemas.md
    │   └── audit-modes.md
    └── scripts/
        └── validate_quality_artifacts.py
```

## Project status

- 🧪 Current maturity: **Beta / testing**.
- ✅ Passes the Codex Skill structure validator.
- ✅ Bundled Python validator passes syntax and positive/negative artifact tests.
- ✅ Completed a read-only forward test on a real, large Rust coding-agent source snapshot.
- 🚧 A public fail-before / pass-after repair case is still planned.
- ⚠️ Project-tested does not mean validated across every language, framework, agent harness, or runtime environment.

## Roadmap

- [ ] Publish a sanitized example `.quality/` workspace.
- [ ] Add a complete public fail-before / pass-after repair case study.
- [ ] Add CI checks for Skill structure, links, and artifact-validator fixtures.
- [ ] Test the workflow across more languages and repository shapes.
- [ ] Add versioned releases and installation automation.

## Contributing

Useful contributions include:

- a reproducible audit failure mode;
- an artifact schema edge case;
- a false-positive example;
- a new language or repository-shape test;
- clearer safety or evidence boundaries.

Open an issue before a large change so the evidence contract stays coherent.

## License

No open-source license has been declared yet. Public visibility does not grant permission to copy, modify, or redistribute the project. A license will be selected explicitly rather than assumed.

---

<div align="center">

If this turns vague project audits into evidence you can trust, consider giving the repository a ⭐.

</div>
