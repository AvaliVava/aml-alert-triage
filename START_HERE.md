# Start here — existing repository workflow

Open this repository as an existing synthetic AML investigation engineering project. Phase 1 is complete. Phase 2 input contracts are implemented and locally tested; output contracts and a formal evaluation protocol remain pending. There is no implemented AML decision engine or investigation agent.

Read [README.md](README.md) for the overview and [PROJECT_STATUS.md](PROJECT_STATUS.md) for the current milestone, implementation checkpoint, and verification limits.

## Part A — set up and verify the existing repository

Open a terminal in the existing `aml-alert-triage` checkout. If you do not have a local checkout, clone the existing repository into a new directory:

```bash
git clone https://github.com/AvaliVava/aml-alert-triage.git
cd aml-alert-triage
```

Existing contributors should reuse their checkout. Do not recreate the repository, reinitialize Git, or replace the existing remote configuration. Confirm the working branch and pending changes before starting an authorized task:

```bash
git branch --show-current
git status --short
```

Confirm your interpreter with `python --version` (or `python3 --version` on Linux/macOS). Supported versions are **3.11–3.13**; the repository's starting version is 3.11. Pydantic V2 is an application dependency and is installed by the editable-install command below. Create the virtual environment once if it does not already exist; otherwise reuse it.

Windows PowerShell, from the repository root:

```powershell
# Run this creation step only if .venv does not already exist.
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts\check_setup.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

If the `python` command is unavailable, use `py -3.11 -m venv .venv` for the creation step instead, provided the Windows Python launcher and Python 3.11 are installed. Reuse an existing `.venv` without recreating it.

Linux/macOS, using a supported `python3` interpreter:

```bash
# Run this creation step only if .venv does not already exist.
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/python scripts/check_setup.py
./.venv/bin/python -m unittest discover -s tests -v
```

Using the virtual environment's Python directly avoids requiring shell activation. In an already activated environment or configured Linux CI, the equivalent commands are `python -m pip install -e .`, `python scripts/check_setup.py`, and `python -m unittest discover -s tests -v`.

The smoke check exercises the original CLI; its historical `week-1-foundation` phase label does not describe the current milestone. The test command runs the complete suite. The verified local baseline at implementation checkpoint `1375d9f` is **99 passing tests**; remote feature-branch GitHub Actions results remain unverified. These checks need no API keys and do not perform AML analysis, execute verification activities, or call an LLM.

## Part B — historical Phase 1 domain exercise

The following learning exercise is retained from the October 26, 2026 project foundation. It is background for contributors, not a requirement to repeat Phase 1 before working on the current task.

Read [the FFIEC suspicious activity reporting section](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04), especially **Managing Alerts** and **SAR Decision Making**. Then open [specs/aml_workflow.md](specs/aml_workflow.md).

Answer, in your own words:

1. What is the difference between **a transaction-monitoring alert** and **a decision to file a SAR**?
2. Why could a bank need customer background before interpreting a large or unusual transaction?
3. What evidence should a human reviewer look at before recommending escalation?
4. What important information might be missing from an alert?

### Fictional practice case (not labeled)

A synthetic small business typically deposits between USD 3,000 and USD 6,000 per week. This week, it deposits USD 24,000 across several transactions. The monitoring system flags an unusual change in volume. The available data does not explain whether the increase resulted from a legitimate event.

**Question:** What additional records or questions would you need before recommending closure, more investigation or escalation? Do not classify the customer as guilty or the activity as proven suspicious.

## Part C — current contribution workflow

Historical context: the original Day 1 starter asked the owner to create and publish the repository. That project-creation exercise has been completed. It is not the setup procedure for this checkout; [WORKLOG.md](WORKLOG.md) retains the foundation history.

1. Read [AGENTS.md](AGENTS.md), [PROJECT_STATUS.md](PROJECT_STATUS.md), [PROJECT_CHARTER.md](PROJECT_CHARTER.md), and [DECISIONS.md](DECISIONS.md), then inspect the code, tests, and specifications relevant to the authorized task. Some documents retain historical status wording; use [PROJECT_STATUS.md](PROJECT_STATUS.md) for the current milestone.
2. Keep changes within the task's approved file and behavior scope. Existing record contracts and aggregate validation are in [contracts.py](src/aml_triage/contracts.py); their automated tests are in [test_contracts.py](tests/test_contracts.py).
3. Run checks relevant to the change and report the actual results. Contract work uses the complete unit-test command above. Passing local checks does not establish that GitHub Actions passed.
4. Inspect `git diff --check`, `git status --short`, and `git diff --stat` before review. Report changed files, limitations, and checks that were not run, with reasons.
5. Follow the current task's authorization for documentation updates and Git actions. Stage, commit, push, and merge only when those actions are authorized.

The implemented engineering scope currently covers input validation only. Fictional labeling terms remain provisional, and supplied synthetic verification records do not represent banking verification performed by this project.
