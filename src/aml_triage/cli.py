"""Minimal foundation-only CLI; does not evaluate AML transactions."""

import argparse
import json
from .status import get_status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AML alert triage research prototype")
    parser.add_argument("command", nargs="?", default="status", choices=["status"])
    args = parser.parse_args(argv)
    if args.command == "status":
        print(json.dumps(get_status(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
