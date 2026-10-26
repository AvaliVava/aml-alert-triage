# Phase 1 problem definition

**Project:** AML Alert Triage Agent, synthetic-data research prototype.

## Problem
Investigating monitoring alerts can involve repeated data preparation, examination of customer activity, evidence gathering and narrative drafting. Fragmented, incomplete or stale information and inconsistent documentation may increase review burden and reduce traceability. These are domain-motivated concerns, **not measured claims about a specific bank**.

## Target users
Hypothetical AML analysts preparing cases and authorized reviewers examining supporting evidence.

## Engineering hypothesis (unverified)
A controlled pipeline combining deterministic feature computation, structured hosted-LLM assessment, evidence checking and grounded narrative drafting can generate useful, traceable *preliminary* investigation packages from synthetic supplied alerts.

## Inputs and outputs
**Inputs:** alert, customer profile, transaction history, available synthetic evidence.
**Outputs:** recommended `close/investigate/escalate`, rationale, identified transactions/documents, unresolved questions, draft narrative, execution metadata.

## Scope exclusions
No production-bank integration, no genuine customer data, no autonomous closure, no real regulatory filing, no guarantee of finding laundering, and no measured analyst time savings without an actual evaluation.

## Technical approach already selected
Single hosted LLM baseline; typed Python schemas; deterministic calculations; tests; synthetic data; no RAG in v1 unless evidence subsequently supports retrieval complexity. GitHub holds implementation truth, decisions and results.
