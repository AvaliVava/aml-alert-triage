"""Audit two JSON files using the installed project, writing only JSON to stdout.

Usage: python scripts/audit_packet.py --input investigation.json --candidate assessment.json
Exit 0: all three mechanical stages passed (no semantic approval).
Exit 1: expected structural/contextual rejection, with no evaluator errors.
Exit 2: ingestion/unexpected evaluator error, or argparse usage error. Usage errors
use argparse's normal stderr diagnostics; supplied-file audit results are JSON.
"""

import argparse
import json

from aml_triage.auditor import audit_packet_files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit JSON structure and record references; no semantic scoring.",
        epilog=(
            "Exit codes: 0 mechanical checks passed; 1 validation failed; "
            "2 I/O/evaluator/usage error (takes precedence over validation failure)."
        ),
    )
    parser.add_argument("--input", required=True, help="Investigation JSON file")
    parser.add_argument("--candidate", required=True, help="Candidate assessment JSON file")
    args = parser.parse_args()
    report = audit_packet_files(args.input, args.candidate)
    print(json.dumps(report, indent=2, allow_nan=False))
    statuses = {stage["status"] for stage in report["stages"].values()}
    if "error" in statuses:
        return 2
    return 1 if "failed" in statuses else 0


if __name__ == "__main__":
    raise SystemExit(main())
