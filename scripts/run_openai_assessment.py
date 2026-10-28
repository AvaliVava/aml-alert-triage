"""Inspect one request by default; --live explicitly enables one guarded attempt.

Exit 0: dry run or structure/citation-valid assessment, not semantic approval.
Exit 1: recorded service failure. Exit 2: configuration, input or publication error.
No client or credential access on import, --help or the default dry-run path.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from aml_triage.contracts import InvestigationInput
from aml_triage.openai_service import AssessmentConfig, OpenAIAssessmentService, publish_run


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect or explicitly run one synthetic AML assessment."
    )
    parser.add_argument("--input", required=True, help="Supplied synthetic investigation JSON")
    parser.add_argument("--output", help="New .json bundle under outputs/; required for --live")
    parser.add_argument("--live", action="store_true", help="Explicitly authorize one request")
    parser.add_argument("--model", help="Explicit model identifier; no default")
    parser.add_argument("--max-output-tokens", type=int)
    parser.add_argument("--request-allowance", type=int, default=0, choices=(0, 1))
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--reasoning-effort", choices=(
        "none", "minimal", "low", "medium", "high", "xhigh", "max",
    ))
    args = parser.parse_args()
    try:
        config = AssessmentConfig(model=args.model, max_output_tokens=args.max_output_tokens,
                                  request_allowance=args.request_allowance, live_enabled=args.live,
                                  timeout_seconds=args.timeout,
                                  reasoning_effort=args.reasoning_effort)
        if args.live and not args.output:
            raise ValueError("live execution requires an explicit output destination")
        target = None
        if args.output:
            supplied = Path(args.output)
            if ".." in supplied.parts or supplied.suffix != ".json":
                raise ValueError("output must be a new .json file without parent traversal")
            target = supplied.resolve()
            target.relative_to(ROOT.resolve() / "outputs")
            if target.exists() or supplied.is_symlink():
                raise ValueError("output already exists")
        payload = Path(args.input).read_bytes()
        investigation = InvestigationInput.model_validate_json(payload)
        if target is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError):
        parser.error("Invalid configuration, investigation or output path; no request was made.")
    run = OpenAIAssessmentService(config).assess(investigation)
    run.record["input_file_sha256"] = sha256(payload).hexdigest()
    try:
        if target is not None:
            publish_run(run, target)
    except (OSError, ValueError):
        # The request may already have been processed: never retry after publication failure.
        print(json.dumps({"status": "publication_failed", "execution": run.record}))
        return 2
    print(json.dumps({"execution": run.record, "output": None if target is None else str(target)}))
    return 1 if run.record["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
