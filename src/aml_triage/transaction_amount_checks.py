"""Restricted transaction-field comparisons, not general claim grounding.

Grammar version 1.0 uses case-sensitive whole-statement matching, exact ASCII
spaces and a final period, with no trimming or prose/number extraction:

    The incoming transaction was <CURRENCY> <AMOUNT>.
    Transaction <ID> amount was <CURRENCY> <AMOUNT>.

CURRENCY is three uppercase ASCII letters. AMOUNT is an unsigned decimal with
exactly two fractional digits, no leading zeros except 0.xx, and either no commas
or correctly grouped thousands (e.g. 48500.00, 48,500.00, 0.10). Signs, exponents,
non-finite values and other formats are outside this grammar. ID starts with an
ASCII letter/digit and continues with ASCII letters/digits, underscores or hyphens.

Both forms require exactly one transaction citation; other citation namespaces
are ignored. The explicit form also requires exact mentioned/cited ID agreement.
Ambiguous or unresolved references are not_checked, never guessed. The incoming
form compares amount, currency and direction=credit. The explicit form compares
only amount and currency, with no implied direction or transaction type.

Only factual_findings are inspected. Call with validated models; the auditor also
requires contextual validation first. Inputs and outputs are never modified.
Reports contain per-finding outcomes and completed-comparison coverage, with
Decimal values serialized as strings. Source field_pointer values are JSON
Pointers relative to the exact typed transaction record, not collection offsets.
Section status describes this restricted check only: failed for any conflict,
passed for checked matches without conflicts, not_evaluated if nothing is safely
checkable or prerequisites failed. It is not general factual approval or a CLI
exit-code input. Unknown totals are null when output validation failed.
"""

import re

from decimal import Decimal

from aml_triage.contracts import (
    CitedStatement,
    InvestigationInput,
    InvestigationOutput,
    Transaction,
)


CHECK_VERSION = "1.0"
_AMOUNT = r"(?:0|[1-9][0-9]*|[1-9][0-9]{0,2}(?:,[0-9]{3})+)\.[0-9]{2}"
_VALUE = rf"(?P<currency>[A-Z]{{3}}) (?P<amount>{_AMOUNT})\."
_INCOMING = re.compile(r"The incoming transaction was " + _VALUE)
_EXPLICIT = re.compile(r"Transaction (?P<record_id>[A-Za-z0-9][A-Za-z0-9_-]*) amount was " + _VALUE)


def _unchecked(index: int, reason: str) -> dict:
    return {
        "finding_path": f"factual_findings[{index}]",
        "outcome": "not_checked",
        "reason": reason,
        "predicate": None,
        "transaction_id": None,
        "citation_path": None,
        "comparisons": [],
    }


def _check_finding(
    index: int, finding: CitedStatement, transactions: dict[str, Transaction],
) -> dict:
    result = _unchecked(index, "Statement is outside the supported whole-statement grammar.")
    match = _INCOMING.fullmatch(finding.statement)
    incoming = match is not None
    if match is None:
        match = _EXPLICIT.fullmatch(finding.statement)
    if match is None:
        return result
    result["predicate"] = (
        "incoming_transaction_amount" if incoming else "explicit_transaction_amount"
    )
    citations = [
        (position, citation) for position, citation in enumerate(finding.citations)
        if citation.record_type == "transaction"
    ]
    if len(citations) != 1:
        result["reason"] = "Exactly one transaction citation is required; no record was selected."
        return result
    position, citation = citations[0]
    if not incoming and match["record_id"] != citation.record_id:
        result["reason"] = (
            f"Mentioned transaction ID {match['record_id']!r} does not exactly match "
            f"cited transaction ID {citation.record_id!r}."
        )
        return result
    transaction = transactions.get(citation.record_id)
    if transaction is None:
        result["reason"] = f"Cited transaction {citation.record_id!r} is not supplied."
        return result

    claims = {"amount": Decimal(match["amount"].replace(",", "")), "currency": match["currency"]}
    if incoming:
        claims["direction"] = "credit"
    comparisons = []
    for field, claimed in claims.items():
        recorded = getattr(transaction, field)
        comparisons.append({
            "field": field,
            "claimed": str(claimed),
            "recorded": str(recorded),
            "matches": claimed == recorded,
            "source": {
                "record_type": "transaction", "record_id": transaction.transaction_id,
                "field_pointer": f"/{field}",
            },
        })
    conflicts = any(not comparison["matches"] for comparison in comparisons)
    result.update(
        outcome="conflicts_with_record" if conflicts else "matches_record",
        reason="Checked fields conflict with the cited record." if conflicts else (
            "Checked fields match the cited record; no broader factual support is established."
        ),
        transaction_id=transaction.transaction_id,
        citation_path=f"factual_findings[{index}].citations[{position}]",
        comparisons=comparisons,
    )
    return result


def _report(findings: list[dict], total: int | None, status: str, reason: str) -> dict:
    matches = sum(item["outcome"] == "matches_record" for item in findings)
    conflicts = sum(item["outcome"] == "conflicts_with_record" for item in findings)
    return {
        "check": "transaction_amount", "check_version": CHECK_VERSION,
        "status": status, "reason": reason, "phase": "deterministic_fact_checks",
        "diagnostics": [],
        "coverage": {
            "total_findings": total, "checked": matches + conflicts,
            "matches_record": matches, "conflicts_with_record": conflicts,
            "not_checked": None if total is None else total - matches - conflicts,
        },
        "findings": findings,
    }


def check_transaction_amounts(
    investigation: InvestigationInput, output: InvestigationOutput,
) -> dict:
    """Compare only recognized, unambiguously cited factual findings to typed fields."""
    transactions = {record.transaction_id: record for record in investigation.transactions}
    findings = [
        _check_finding(index, finding, transactions)
        for index, finding in enumerate(output.factual_findings)
    ]
    outcomes = {item["outcome"] for item in findings}
    if "conflicts_with_record" in outcomes:
        status, reason = "failed", "At least one restricted transaction-field comparison conflicts."
    elif "matches_record" in outcomes:
        status = "passed"
        reason = "Checked predicates match; inspect unchecked coverage separately."
    else:
        status, reason = "not_evaluated", "No finding met the grammar and citation requirements."
    return _report(findings, len(output.factual_findings), status, reason)


def skipped_transaction_amount_checks(output: InvestigationOutput | None, reason: str) -> dict:
    """Report blocked checks without recognizing statements or comparing record fields."""
    findings = [] if output is None else [
        _unchecked(index, reason) for index in range(len(output.factual_findings))
    ]
    total = None if output is None else len(output.factual_findings)
    return _report(findings, total, "not_evaluated", reason)
