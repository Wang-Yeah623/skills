#!/usr/bin/env python3
"""Validate the structure and JSONL consistency of project quality artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SYSTEM_FILES = (
    "project-map.md",
    "acceptance.md",
    "risk-register.md",
    "coverage-matrix.md",
    "audit-queue.md",
    "issue-ledger.jsonl",
)

LEDGER_FIELDS = {
    "id",
    "discovered_at",
    "area",
    "severity",
    "symptom",
    "impact",
    "evidence",
    "reproduction",
    "root_cause",
    "fix",
    "regression_test",
    "validation",
    "status",
    "classification",
}

SEVERITIES = {"P0", "P1", "P2", "P3"}
STATUSES = {
    "hypothesis",
    "confirmed",
    "fixing",
    "fixed",
    "verified",
    "wont-fix",
    "closed",
}
CLASSIFICATIONS = {
    "unclassified",
    "new-defect",
    "recurrence",
    "regression",
    "latent",
    "environment",
    "false-positive",
}


def resolve_quality_dir(target: Path) -> Path:
    target = target.expanduser().resolve()
    if target.name == ".quality":
        return target
    nested = target / ".quality"
    return nested if nested.is_dir() else target


def has_content(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def validate_markdown(path: Path, errors: list[str]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {path.name}: {exc}")
        return

    if len(text.strip()) < 40:
        errors.append(f"{path.name} is empty or too small")
    if not any(line.startswith("# ") for line in text.splitlines()):
        errors.append(f"{path.name} has no level-1 heading")
    if path.name != "project-map.md" and not any(
        line.startswith("## ") for line in text.splitlines()
    ):
        errors.append(f"{path.name} has no level-2 sections")
    if path.name in {"risk-register.md", "coverage-matrix.md"} and "|" not in text:
        errors.append(f"{path.name} does not contain a Markdown table")


def validate_ledger(path: Path, errors: list[str]) -> int:
    seen: set[str] = set()
    count = 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"cannot read issue-ledger.jsonl: {exc}")
        return 0

    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        count += 1
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"issue-ledger.jsonl:{line_number}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(item, dict):
            errors.append(f"issue-ledger.jsonl:{line_number}: entry must be an object")
            continue

        missing = sorted(LEDGER_FIELDS - item.keys())
        if missing:
            errors.append(
                f"issue-ledger.jsonl:{line_number}: missing fields: {', '.join(missing)}"
            )

        issue_id = item.get("id")
        if not isinstance(issue_id, str) or not issue_id.strip():
            errors.append(f"issue-ledger.jsonl:{line_number}: id must be a non-empty string")
        elif issue_id in seen:
            errors.append(f"issue-ledger.jsonl:{line_number}: duplicate id {issue_id}")
        else:
            seen.add(issue_id)

        if item.get("severity") not in SEVERITIES:
            errors.append(f"issue-ledger.jsonl:{line_number}: invalid severity")
        if item.get("status") not in STATUSES:
            errors.append(f"issue-ledger.jsonl:{line_number}: invalid status")
        if item.get("classification") not in CLASSIFICATIONS:
            errors.append(f"issue-ledger.jsonl:{line_number}: invalid classification")

        status = item.get("status")
        if status in {"confirmed", "fixing", "fixed", "verified"}:
            if not has_content(item.get("evidence")) or not has_content(
                item.get("reproduction")
            ):
                errors.append(
                    f"issue-ledger.jsonl:{line_number}: {status} requires evidence and reproduction"
                )
        if status in {"fixed", "verified"}:
            if not has_content(item.get("regression_test")) or not has_content(
                item.get("validation")
            ):
                errors.append(
                    f"issue-ledger.jsonl:{line_number}: {status} requires regression_test and validation"
                )
    return count


def validate(target: Path, profile: str) -> tuple[list[str], list[str]]:
    quality_dir = resolve_quality_dir(target)
    errors: list[str] = []
    notes: list[str] = [f"quality_dir={quality_dir}"]

    required = ("project-map.md",) if profile == "map" else SYSTEM_FILES
    if not quality_dir.is_dir():
        return [f"quality directory does not exist: {quality_dir}"], notes

    for name in required:
        path = quality_dir / name
        if not path.is_file():
            errors.append(f"missing required file: {name}")
            continue
        if name.endswith(".md"):
            validate_markdown(path, errors)

    if profile != "map":
        ledger = quality_dir / "issue-ledger.jsonl"
        if ledger.is_file():
            notes.append(f"ledger_entries={validate_ledger(ledger, errors)}")

        runs = quality_dir / "runs"
        if not runs.is_dir():
            errors.append("missing required directory: runs")
        elif profile == "audit":
            reports = sorted(runs.glob("*.md"))
            if not reports:
                errors.append("audit profile requires at least one runs/*.md report")
            for report in reports:
                validate_markdown(report, errors)
            notes.append(f"run_reports={len(reports)}")

    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="repository root or .quality directory")
    parser.add_argument(
        "--profile",
        choices=("map", "system", "audit"),
        default="audit",
        help="minimum artifact set to require",
    )
    args = parser.parse_args()

    errors, notes = validate(args.target, args.profile)
    for note in notes:
        print(f"INFO: {note}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"VALIDATION_FAILED: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"VALIDATION_OK: profile={args.profile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
