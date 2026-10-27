"""Write a preliminary baseline assessment to an explicit, previously absent file.

Usage: python scripts/run_baseline.py --input investigation.json --output assessment.json
Exit 0: validated output published (no semantic-quality approval).
Exit 2: usage, input validation, I/O or unsupported atomic-publication filesystem.
Uses an atomic no-overwrite hard link from a complete same-filesystem temporary
file. No partially written assessment is exposed. No unsafe overwrite fallback.
"""

import argparse
import json
import os
from pathlib import Path
import tempfile

from aml_triage.contracts import InvestigationInput, InvestigationOutput
from aml_triage.deterministic_baseline import assess_investigation


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the limited preliminary synthetic AML baseline.",
    )
    parser.add_argument("--input", required=True, help="Supplied investigation JSON")
    parser.add_argument("--output", required=True, help="New assessment JSON destination")
    args = parser.parse_args()
    try:
        target = Path(args.output).absolute()
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Output already exists: {target}")
        investigation = InvestigationInput.model_validate_json(Path(args.input).read_bytes())
        output = assess_investigation(investigation)
        payload = (json.dumps(output.model_dump(mode="json"), sort_keys=True,
                              indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
        InvestigationOutput.model_validate_json(payload)
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".baseline-", dir=target.parent) as temp:
            staged = Path(temp) / "assessment.json"
            staged.write_bytes(payload)
            if staged.read_bytes() != payload:
                raise OSError("Staged assessment bytes differ from the validated output")
            os.link(staged, target)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({"output": str(target), "assessment_status": output.assessment_status,
                      "recommended_action": output.recommended_action}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
