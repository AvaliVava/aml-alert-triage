# Start here — Week 1, Day 1

This is a **project foundation**, not an AI classifier. Use it to create a stable source of truth before implementation.

## Part A — verify the local foundation

1. Unzip the starter project. Open a terminal in the `aml-alert-triage` folder.
2. Confirm Python version (`python --version`). The foundation supports 3.11–3.13; the recommended starting version is 3.11.
3. Run:

   ```bash
   python scripts/check_setup.py
   python -m unittest discover -s tests -v
   ```

4. Read `PROJECT_STATUS.md` and record your own environment and test results when you push the first commit.

No API keys or installation of LLM libraries are needed for Week 1 Day 1.

## Part B — study the domain

Read [the FFIEC suspicious activity reporting section](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04), especially **Managing Alerts** and **SAR Decision Making**. Then open `specs/aml_workflow.md`.

Answer, in your own words:

1. What is the difference between **a transaction-monitoring alert** and **a decision to file a SAR**?
2. Why could a bank need customer background before interpreting a large or unusual transaction?
3. What evidence should a human reviewer look at before recommending escalation?
4. What important information might be missing from an alert?

### Fictional practice case (not labeled)

A synthetic small business typically deposits between USD 3,000 and USD 6,000 per week. This week, it deposits USD 24,000 across several transactions. The monitoring system flags an unusual change in volume. The available data does not explain whether the increase resulted from a legitimate event.

**Question:** What additional records or questions would you need before recommending closure, more investigation or escalation? Do not classify the customer as guilty or the activity as proven suspicious.

## Part C — make it durable on GitHub

GitHub repo creation is **not completed** in this downloaded starter. After reviewing these files:

1. Create a new, **empty** GitHub repository named `aml-alert-triage` (no generated README or .gitignore; those files already exist in the starter).
2. In the project folder, run:

   ```bash
   git init -b main
   git add .
   git commit -m "chore: initialize AML research project foundation"
   git remote add origin https://github.com/YOUR_USERNAME/aml-alert-triage.git
   git push -u origin main
   ```

   Replace `YOUR_USERNAME`; if Git asks for authentication, use GitHub's supported sign-in mechanism instead of committing a token.
3. Verify the first GitHub Actions run and record its outcome and commit SHA in `PROJECT_STATUS.md`/`WORKLOG.md`.
4. Open Codex with this same repository. Ask it to read `AGENTS.md`, `PROJECT_STATUS.md`, `DECISIONS.md` and tests **before making changes**.
5. Create the two Week 1 issues in `issues_to_create.md`.

**Day 1 is complete only after you have personally reviewed the domain exercise and the repository has been published and verified.**
