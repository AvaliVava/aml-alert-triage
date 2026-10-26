"""Dependency-free smoke check for a freshly downloaded repository."""

from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "PROJECT_CHARTER.md",
    "PROJECT_STATUS.md",
    "DECISIONS.md",
    "WORKLOG.md",
    "ROADMAP.md",
    "specs/aml_workflow.md",
    "src/aml_triage/status.py",
]


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")
    if not ((3, 11) <= sys.version_info[:2] < (3, 14)):
        print("FAIL: Foundation targets Python 3.11–3.13")
        return 1
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        print(f"FAIL: Missing files: {missing}")
        return 1
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + environment.get("PYTHONPATH", "")
    result = subprocess.run(
        [sys.executable, "-m", "aml_triage", "status"],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"FAIL: CLI smoke test: {result.stderr}")
        return 1
    print("PASS: Required project files found")
    print("PASS: Foundation CLI executes")
    print(result.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
