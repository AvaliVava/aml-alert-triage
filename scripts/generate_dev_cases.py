"""Publish fictional DEVELOPMENT inputs and a separate manifest using the installed project.

Usage: python scripts/generate_dev_cases.py --seed 20261027 --count 50 --output-dir PATH
Exit 0: validated batch published; exit 2: configuration, destination or validation error.
Success writes a JSON summary to stdout; errors use argparse's stderr diagnostics.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from aml_triage.synthetic_generator import write_development_batch


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate reproducible synthetic development investigations.",
    )
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        manifest = write_development_batch(args.output_dir, seed=args.seed, count=args.count)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    output = Path(args.output_dir).absolute()
    print(json.dumps({
        "dataset_partition": "development", "case_count": manifest["case_count"],
        "scenario_family_counts": manifest["scenario_family_counts"], "output_dir": str(output),
        "manifest_sha256": sha256((output / "manifest.json").read_bytes()).hexdigest(),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
