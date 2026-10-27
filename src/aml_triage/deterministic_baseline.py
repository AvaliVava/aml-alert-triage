"""Small provisional baseline over supplied records, not an adjudicated AML policy.

assess_investigation accepts a validated InvestigationInput, produces the existing
InvestigationOutput, and resolves all typed citations before returning. It reads
no files, labels, manifests, annotations or check-status conclusions. Rule IDs
appear in statement text because the output contract has no rule-metadata field.

MI-01: explicitly incomplete payment fields or unrepresented recipient accounts.
MI-02: a customer explanation without a linked invoice/order/dispatch record.
BEN-01/BEN-02: exact invoice/wire beneficiary comparison or unknown comparison.
CASH-01/02/03: flagged cash sums, individual daily-range comparisons, and
supplied reconciliation/sales coverage gaps. Arithmetic agreement never closes.
REF-01: literal provisional supplier referral, using linked ledger transactions,
an exact supported review instruction and a synthetic procurement register.
BASE-01: otherwise abstain. No rule produces close. Unknown policies abstain.

REF-01 source reliance is explicit: synthetic_bank_ledger and
synthetic_procurement_registry are recognized supplied provenance, not newly
authenticated or independently verified sources. Original aggregate payee fields
and generator payment rows are supported. Optional ledger totals must agree;
payment rows must match typed transaction amounts, currencies and timestamps.
Directly linked synthetic bank wire beneficiary references are cross-checked
against qualifying ledger mappings. A disagreement blocks referral and produces
a question citing both sources. Wires cannot independently establish mappings;
invoice instructions and unrelated wires do not override recorded recipients.
Instructions support only 'Transfers/Payments to ACCOUNT require senior review
before release[.]', with a matching structured account when present. Multiple
instructions, conflicting mappings/registers, unsupported fields and any recorded
authorized change prevent referral certainty. Historical/future authorization
snapshot semantics and other instruction paraphrases are outside this version.
Completed senior review is not a policy exception and bypass is not inferred.
Evidence money accepts finite nonnegative cent-precision decimal strings/integers,
not JSON floats; unsupported fractional amounts are not silently rounded. POS
numeric summaries and their linked coverage are checked explicitly.
Unflagged cash is not subjected to a universal sales-document requirement.

Absence claims describe only the supplied recognized record scope. These rules
do not establish authenticity, fraud, fund flows, commercial purpose, complete
investigation coverage or regulatory compliance. Evaluation remains separate.
"""

from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation, localcontext
import re

from aml_triage.contracts import (
    CitedStatement, Contradiction, Evidence, InvestigationInput, InvestigationOutput,
    RecordCitation, validate_investigation_output_references,
)


BASELINE_VERSION = "0.1.0"
_INSTRUCTION = re.compile(
    r"(?:Transfers|Payments) to (\S+) require senior review before release\.?"
)


def _text(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _decimal(value) -> Decimal | None:
    if type(value) not in (str, int, Decimal):
        return None
    try:
        parsed = Decimal(value)
        if not parsed.is_finite() or parsed < 0:
            return None
        parts = parsed.as_tuple()
        excess = max(-parts.exponent - 2, 0)
        return None if excess and any(parts.digits[-excess:]) else parsed
    except InvalidOperation:
        return None


def _timestamp(value) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
        return parsed if parsed.utcoffset() is not None else None
    except ValueError:
        return None


def _sum(values) -> Decimal:
    values = list(values)
    with localcontext() as context:
        context.prec = max(50, sum(max(value.adjusted() + 1, 1)
                                   + max(-value.as_tuple().exponent, 0) for value in values) + 10)
        return sum(values, Decimal(0))


def _citation(kind: str, identifier: str) -> tuple[str, str]:
    return kind, identifier


def _ev(record: Evidence) -> tuple[str, str]:
    return _citation("evidence", record.evidence_id)


def _statement(text: str, *citations: tuple[str, str]) -> CitedStatement:
    return CitedStatement(statement=text, citations=[
        RecordCitation(record_type=kind, record_id=identifier)
        for kind, identifier in dict.fromkeys(citations)
    ])


class _Assessment:
    def __init__(self, investigation: InvestigationInput):
        self.input = investigation
        self.facts, self.interpretations, self.questions, self.missing = [], [], [], []
        self.contradictions = []
        self.concerns = []

    def question(self, rule: str, text: str, *citations, missing: bool = False):
        item = _statement(f"[{rule}] {text}", *citations)
        self.questions.append(item)
        self.concerns.append(item)
        if missing:
            self.missing.append(item)

    def linked(self, transaction_id: str, kinds: tuple[str, ...]) -> list[Evidence]:
        return [record for record in self.input.evidence if record.evidence_type in kinds
                and transaction_id in record.related_transaction_ids]


def _information(result: _Assessment) -> None:
    for transaction in result.input.transactions:
        tx = _citation("transaction", transaction.transaction_id)
        result.facts.append(_statement(
            f"Transaction {transaction.transaction_id} amount was "
            f"{transaction.currency} {transaction.amount:,.2f}.", tx,
        ))
        records = result.linked(
            transaction.transaction_id, ("payment_record", "wire_payment_record"),
        )
        if transaction.direction == "debit" and (
            transaction.transaction_id in result.input.alert.transaction_ids or records
        ):
            accounts = []
            for record in records:
                facts = record.facts
                accounts.extend(facts[key] for key in
                                ("beneficiary_account_ref", "payee_account_ref") if key in facts)
                rows = facts.get("payments")
                if isinstance(rows, list):
                    accounts.extend(row.get("payee_account_ref") for row in rows
                                    if isinstance(row, dict)
                                    and row.get("transaction_id") == transaction.transaction_id)
                if "commercial_purpose" in facts and not _text(facts["commercial_purpose"]):
                    result.facts.append(_statement(
                        f"[MI-01] Payment record {record.evidence_id} has no usable "
                        "commercial_purpose value.", _ev(record),
                    ))
                    result.question("MI-01", "What commercial-purpose information is available "
                                    "for this outgoing payment in the supplied review scope?",
                                    tx, _ev(record), missing=True)
            if not accounts or not all(_text(value) for value in accounts):
                refs = [_ev(record) for record in records]
                result.facts.append(_statement(
                    f"[MI-01] Recognized payment records for {transaction.transaction_id} "
                    "do not consistently supply a usable beneficiary-account value.", tx, *refs,
                ))
                result.question("MI-01", f"What beneficiary account applies to transaction "
                                f"{transaction.transaction_id}? Recognized supplied payment "
                                "records do not consistently provide a nonempty account reference.",
                                tx, *refs, missing=True)
        for explanation in result.linked(transaction.transaction_id, ("customer_explanation",)):
            claim = explanation.facts.get("claim")
            if _text(claim):
                result.facts.append(_statement(
                    f"[MI-02] Customer-supplied explanation {explanation.evidence_id} "
                    f"records the claim {claim!r}.", _ev(explanation),
                ))
            supporting = result.linked(transaction.transaction_id,
                                       ("supplier_invoice", "purchase_order", "dispatch_record"))
            if not supporting:
                result.question("MI-02", f"What document supports the customer explanation for "
                                f"{transaction.transaction_id}? No linked invoice, purchase order "
                                "or dispatch record is supplied; this limited inventory check "
                                "does not establish the claimed purpose.",
                                tx, _ev(explanation), missing=True)


def _beneficiaries(result: _Assessment) -> None:
    for transaction in result.input.transactions:
        if transaction.direction != "debit":
            continue
        invoices = result.linked(transaction.transaction_id, ("supplier_invoice",))
        wires = result.linked(transaction.transaction_id, ("wire_payment_record",))
        for invoice in invoices:
            for wire in wires:
                left, right = (record.facts.get("beneficiary_account_ref")
                               for record in (invoice, wire))
                refs = (_ev(invoice), _ev(wire),
                        _citation("transaction", transaction.transaction_id))
                if not (_text(left) and _text(right)):
                    result.question("BEN-02", "What beneficiary references complete the linked "
                                    "invoice/wire comparison? A missing or malformed value makes "
                                    "this comparison unknown, not a proven disagreement.",
                                    *refs, missing=True)
                    continue
                different = left != right
                result.facts.append(_statement(
                    f"[BEN-01] Invoice {invoice.evidence_id} records beneficiary {left!r}; wire "
                    f"record {wire.evidence_id} records {right!r}. The supplied references "
                    f"{'differ' if different else 'are equal'}.", *refs,
                ))
                if different:
                    result.contradictions.append(Contradiction(
                        description="Different beneficiary references for a shared transaction.",
                        left=_statement(f"Invoice records beneficiary {left!r}.", _ev(invoice)),
                        right=_statement(f"Wire record records beneficiary {right!r}.", _ev(wire)),
                    ))
                    result.question("BEN-01", "What explains the different invoice and wire "
                                    "beneficiary references? The mismatch alone establishes "
                                    "neither fraud nor an unauthorized payment.", *refs)


def _cash(result: _Assessment) -> None:
    grouped = defaultdict(list)
    for transaction in result.input.transactions:
        if (transaction.transaction_type == "cash_deposit" and transaction.direction == "credit"
                and transaction.transaction_id in result.input.alert.transaction_ids):
            grouped[transaction.currency].append(transaction)
    profile = result.input.customer.expected_monthly_activity
    customer = _citation("customer", result.input.customer.customer_id)
    for currency, transactions in grouped.items():
        refs = [_citation("transaction", record.transaction_id) for record in transactions]
        total = _sum(record.amount for record in transactions)
        result.facts.append(_statement(
            f"[CASH-01] The {len(transactions)} supplied flagged credit cash deposits "
            f"in {currency} sum to {total:,.2f}; this is a multi-transaction total, "
            "not a daily comparison.", *refs,
        ))
        low, high = profile.typical_daily_cash_deposit_min, profile.typical_daily_cash_deposit_max
        if currency == profile.currency and low is not None and high is not None:
            for transaction, ref in zip(transactions, refs):
                relation = "above" if transaction.amount > high else (
                    "below" if transaction.amount < low else "within"
                )
                result.facts.append(_statement(
                    f"[CASH-02] Individual deposit {transaction.transaction_id} of {currency} "
                    f"{transaction.amount:,.2f} is {relation} the supplied typical daily range "
                    f"{low:,.2f}–{high:,.2f}. No multi-day total is compared to that range.",
                    ref, customer,
                ))
        ids = {record.transaction_id for record in transactions}
        reconciliations = [record for record in result.input.evidence
                           if record.evidence_type == "deposit_reconciliation"
                           and ids.intersection(record.related_transaction_ids)]
        usable = False
        for record in reconciliations:
            facts = record.facts
            reconciled, unmatched = (_decimal(facts.get(key))
                                     for key in ("reconciled_deposits", "unmatched_amount"))
            comparable = facts.get("currency") == currency
            complete = set(record.related_transaction_ids) == ids
            if comparable and unmatched is not None:
                result.facts.append(_statement(
                    f"[CASH-03] Supplied reconciliation {record.evidence_id} records "
                    f"unmatched_amount {currency} {unmatched:,.2f}.", _ev(record),
                ))
                if unmatched > 0:
                    result.question("CASH-03", "What explains the explicitly recorded unmatched "
                                    "cash amount within this supplied reconciliation?",
                                    _ev(record), *refs)
            if comparable and complete and reconciled is not None and unmatched is not None:
                usable = True
                if _sum((reconciled, unmatched)) != total:
                    result.question("CASH-03", "Why does the supplied reconciliation sum differ "
                                    "from the linked transaction total?", _ev(record), *refs)
        if not usable:
            result.question("CASH-03", "What reconciliation covers these supplied cash deposits? "
                            "No complete, currency-comparable numeric reconciliation is supplied "
                            "in the supported fields.", *refs,
                            *[_ev(record) for record in reconciliations], missing=True)
        sales = [record for record in result.input.evidence
                 if record.evidence_type == "point_of_sale_summary"
                 and record.facts.get("currency") == currency
                 and ids.intersection(record.related_transaction_ids)]
        by_id = {record.transaction_id: record for record in transactions}
        for record in sales:
            daily = record.facts.get("daily_sales")
            amounts = [_decimal(value) for value in daily] if isinstance(daily, list) else []
            summary = _decimal(record.facts.get("summary_total"))
            linked_total = _sum(by_id[identifier].amount for identifier in
                                record.related_transaction_ids if identifier in by_id)
            if (not amounts or any(value is None for value in amounts) or summary is None
                    or _sum(amounts) != summary or set(record.related_transaction_ids) - ids
                    or summary != linked_total):
                result.question("CASH-03", "Clarify the supplied POS numeric summary and its "
                                "linked deposit coverage; the supported fields do not establish "
                                "matching numeric totals and transaction coverage.",
                                _ev(record), *refs)
        covered = set().union(*(set(record.related_transaction_ids) for record in sales)) & ids
        if covered != ids:
            result.question("CASH-03", "What sales records cover the remaining cash deposits? "
                            "The supplied recognized POS summaries do not cover every deposit.",
                            *refs, *[_ev(record) for record in sales], missing=True)


def _payments(investigation: InvestigationInput) -> tuple[dict, list[str], list[Evidence]]:
    """Resolve supported supplied ledger mappings without guessing row ownership."""
    transactions = {record.transaction_id: record for record in investigation.transactions}
    mappings, problems, sources = defaultdict(set), [], []
    for ledger in investigation.evidence:
        if ledger.evidence_type != "payment_record" or not any(
            transactions[identifier].direction == "debit"
            for identifier in ledger.related_transaction_ids
        ):
            continue
        sources.append(ledger)
        if ledger.source != "synthetic_bank_ledger":
            problems.append("Payment provenance is outside the supported supplied-ledger source.")
            continue
        rows = ledger.facts.get("payments")
        if "payments" in ledger.facts and "payee_account_ref" in ledger.facts:
            problems.append("Mixed aggregate and row-level payee representations are unsupported.")
            continue
        if rows is None:
            account = ledger.facts.get("payee_account_ref")
            linked = [transactions[identifier] for identifier in ledger.related_transaction_ids]
            total = _decimal(ledger.facts.get("total_amount"))
            if (not _text(account) or not linked
                    or any(record.direction != "debit" for record in linked)):
                problems.append("Aggregate supplier payee mapping is missing or ambiguous.")
                continue
            if "total_amount" in ledger.facts and (
                total != _sum(record.amount for record in linked)
                or any(record.currency != ledger.facts.get("currency") for record in linked)
            ):
                problems.append("Aggregate ledger amount/currency conflicts with transactions.")
                continue
            for transaction in linked:
                mappings[transaction.transaction_id].add(account)
        elif isinstance(rows, list) and rows:
            seen = set()
            for row in rows:
                identifier = row.get("transaction_id") if isinstance(row, dict) else None
                transaction = transactions.get(identifier) if isinstance(identifier, str) else None
                if (transaction is None or identifier not in ledger.related_transaction_ids
                        or identifier in seen or transaction.direction != "debit"
                        or not _text(row.get("payee_account_ref"))
                        or _decimal(row.get("amount")) != transaction.amount
                        or row.get("currency") != transaction.currency
                        or _timestamp(row.get("occurred_at")) != transaction.occurred_at):
                    problems.append("Payment row mapping, amount, currency or time is ambiguous.")
                    continue
                seen.add(identifier)
                mappings[identifier].add(row["payee_account_ref"])
            if seen != set(ledger.related_transaction_ids):
                problems.append("Payment rows do not fully map their declared transaction links.")
        else:
            problems.append("Unsupported supplier payment-row structure.")
    if any(len(accounts) != 1 for accounts in mappings.values()):
        problems.append("Supplied ledgers give conflicting payee accounts for a transaction.")
    return mappings, problems, sources


def _referral(result: _Assessment) -> CitedStatement | None:
    investigation = result.input
    instructions = [record for record in investigation.evidence
                    if record.evidence_type == "supplier_instruction_notice"]
    registers = [record for record in investigation.evidence
                 if record.evidence_type == "supplier_authorization_register"]
    if not instructions and not registers:
        return None
    mappings, problems, ledgers = _payments(investigation)
    refs = [_ev(record) for record in instructions + registers + ledgers]
    refs.extend(_citation("transaction", record.transaction_id)
                for record in investigation.transactions if record.direction == "debit")
    if len(instructions) != 1:
        problems.append("Exactly one unambiguous supported review instruction is required.")
    if not registers or not ledgers:
        problems.append("Supplier register or linked payment ledger is absent.")
    if problems:
        result.question("REF-01", "Clarify supplied referral dependencies: " + " ".join(problems),
                        *refs, missing=True)
        return None
    instruction = instructions[0]
    match = _INSTRUCTION.fullmatch(instruction.facts.get("instruction", "")) if isinstance(
        instruction.facts.get("instruction"), str
    ) else None
    when = _timestamp(instruction.facts.get("issued_at"))
    account = match[1] if match else None
    if (account is None or when is None or instruction.source != "synthetic_internal_case_log" or (
        "review_required_account_ref" in instruction.facts
        and instruction.facts["review_required_account_ref"] != account
    )):
        result.question("REF-01", "What exact account, review requirement and aware timestamp "
                        "does the supplied instruction establish? Its fields are incomplete "
                        "or conflicting.", _ev(instruction), missing=True)
        return None
    qualifying = [record for record in investigation.transactions
                  if record.direction == "debit" and record.transaction_type != "cash_deposit"
                  and mappings.get(record.transaction_id) == {account}
                  and record.transaction_id in instruction.related_transaction_ids
                  and record.occurred_at > when]
    if len(qualifying) < 2:
        result.interpretations.append(_statement(
            "[REF-01] Fewer than two supplied outgoing transfers meet the explicit account, "
            "instruction-link and timing requirements; this detector does not establish referral.",
            *refs,
        ))
        return None
    # Corroboration only: wire records never create or replace ledger mappings.
    for wire in investigation.evidence:
        recipient = wire.facts.get("beneficiary_account_ref")
        if (wire.evidence_type != "wire_payment_record"
                or wire.source != "synthetic_bank_ledger" or not _text(recipient)):
            continue
        disputed = [record for record in qualifying
                    if record.transaction_id in wire.related_transaction_ids
                    and recipient != account]
        if disputed:
            disputed_ids = {record.transaction_id for record in disputed}
            result.question(
                "REF-01", f"Resolve conflicting bank-side recipient records: wire "
                f"{wire.evidence_id} records {recipient!r}, while supported payment ledgers map "
                f"the linked qualifying transfer(s) to {account!r}. Reconcile these direct "
                "records before asserting referral.",
                _ev(wire), *[_ev(ledger) for ledger in ledgers
                             if disputed_ids.intersection(ledger.related_transaction_ids)],
                *[_citation("transaction", record.transaction_id) for record in disputed],
            )
            return None
    required_ids = {record.transaction_id for record in qualifying}
    blocking_registers = []
    for register in registers:
        facts = register.facts
        approved = facts.get("approved_payee_account_refs")
        if approved is None and _text(facts.get("approved_payee_account_ref")):
            approved = [facts["approved_payee_account_ref"]]
        if (register.source != "synthetic_procurement_registry"
                or not required_ids.issubset(register.related_transaction_ids)
                or not isinstance(approved, list)
                or not all(_text(value) for value in approved)
                or ("approved_payee_account_refs" in facts
                    and "approved_payee_account_ref" in facts)
                or type(facts.get("authorized_change_recorded")) is not bool
                or ("actual_payee_account_ref" in facts
                    and facts["actual_payee_account_ref"] != account)):
            result.question("REF-01", "Clarify register provenance, account scope, approvals "
                            "and authorized-change fields before asserting referral.",
                            _ev(register), _ev(instruction), missing=True)
            return None
        blocking_registers.append(
            account in approved or facts["authorized_change_recorded"] is True,
        )
        if blocking_registers[-1]:
            result.facts.append(_statement(
                f"[REF-01] Supplied register {register.evidence_id} records approved accounts "
                f"{approved!r} and authorized_change_recorded="
                f"{facts['authorized_change_recorded']!r}; "
                "these records do not establish the required unapproved/no-change conjunction.",
                _ev(register),
            ))
    if any(blocking_registers):
        if not all(blocking_registers):
            result.question("REF-01", "Resolve the differing supplied register approval/change "
                            "states before asserting the referral conjunction.",
                            *[_ev(record) for record in registers])
        return None
    refs.extend(_citation("transaction", record.transaction_id) for record in qualifying)
    fact = _statement(
        f"[REF-01] {len(qualifying)} supplied outgoing transfers to recorded account {account!r} "
        f"occur after the senior-review instruction at {when.isoformat()}. Supplied procurement "
        "registers list that account outside approved entries "
        "and record no authorized change.", *refs,
    )
    result.facts.append(fact)
    return fact


def assess_investigation(investigation: InvestigationInput) -> InvestigationOutput:
    """Return a deterministic preliminary assessment; input must already be validated.

    Uses POLICY-AML-V1 only. Recommendations are scoped to the documented fixed
    predicates, not scored against provisional references. Caller data is never
    mutated. Citation validation is mandatory even for abstention.
    """
    if not isinstance(investigation, InvestigationInput):
        raise TypeError("investigation must be a validated InvestigationInput")
    result = _Assessment(investigation)
    # Exact decimal arithmetic even if a caller changed the ambient precision.
    with localcontext() as context:
        context.prec = max(50, sum(len(record.amount.as_tuple().digits)
                                   for record in investigation.transactions) + 10)
        _information(result)
        _beneficiaries(result)
        _cash(result)
        referral = _referral(result) if investigation.case.policy_id == "POLICY-AML-V1" else None
    known_policy = investigation.case.policy_id == "POLICY-AML-V1"
    action = "escalate" if referral else "investigate" if result.concerns and known_policy else None
    if referral:
        rationale = _statement(
            "[REF-01] The supplied records satisfy every implemented literal fictional referral "
            "element under the documented source-reliance assumption. Recommend preliminary "
            "escalation for human review; senior-review bypass and independent authenticity "
            "have not been established.",
            *((item.record_type, item.record_id) for item in referral.citations),
        )
    elif action:
        rationale = _statement(
            "[BASE-01] Specific material questions remain in the supplied scope, identified below. "
            "No complete REF-01 conjunction was established by this limited detector. "
            "Recommend preliminary investigation for human review.",
            *((item.record_type, item.record_id) for question in result.concerns
              for item in question.citations),
        )
    else:
        reason = ("no supported decision rule supplies sufficient justification in this limited "
                  "baseline" if known_policy else
                  f"supplied policy {investigation.case.policy_id!r} is unsupported")
        rationale = _statement(
            f"[BASE-01] Unable to recommend: {reason}. Arithmetic agreement does not justify "
            "closure; closure corroboration remains under review."
        )
    result.interpretations.append(_statement(
        "[BASE-01] This preliminary assessment applies limited fixed rules to supplied records. "
        "It performs no independent verification and establishes no fraud or fund tracing. "
        "Unreported issues are not certified absent. Human review is required.",
        _citation("case", investigation.case.case_id),
    ))
    output = InvestigationOutput(
        schema_version="1.0", case_id=investigation.case.case_id,
        alert_id=investigation.alert.alert_id,
        assessment_status="recommendation_provided" if action else "unable_to_recommend",
        recommended_action=action, rationale=rationale, factual_findings=result.facts,
        interpretations=result.interpretations, unresolved_questions=result.questions,
        missing_information=result.missing, contradictions=result.contradictions,
        recommendation_scope="preliminary", human_review_required=True,
    )
    return validate_investigation_output_references(investigation, output)
