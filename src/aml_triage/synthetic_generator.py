"""Seeded DEVELOPMENT investigations; no labels, recommendations or verification.

generate_development_batch(seed=..., count=...) returns investigation bytes and
separate manifest bytes. JSON uses sorted keys, two-space indentation, UTF-8 and
one LF terminator; money is represented as two-place decimal strings. The clock,
global random state, filesystem paths and reference answers do not affect bytes.
Reproduction requires the same generator/template versions and configuration.

write_development_batch(output_dir, seed=..., count=...) refuses every existing
destination, including empty directories. It stages and validates the entire
batch before a directory rename. A sibling exclusive lock prevents competing
generator publications. The manifest is bookkeeping, never candidate input.

These new templates draw on the five exposed development scenarios conceptually.
Instances share template lineage and are not independent held-out cases or
adjudicated ground truth. All evidence/checks are fictional supplied records;
the program performs no banking verification or policy interpretation.
"""

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from hashlib import sha256
import json
import os
from pathlib import Path
import random
import tempfile

from aml_triage.contracts import InvestigationInput


GENERATOR_VERSION = "1.0.0"
TEMPLATE_VERSION = "1.0"
FAMILIES = (
    "incoming_transfer", "cash_sales", "supplier_authorization",
    "incomplete_outgoing", "beneficiary_comparison",
)
_MODES = (
    ("invoice_and_dispatch", "invoice_only", "explanation_only"),
    ("complete_sales", "partial_sales", "no_sales_records"),
    ("before_instruction", "after_instruction", "authorized_change", "split_timing",
     "different_accounts_same_supplier"),
    ("missing_account", "missing_purpose", "missing_both", "partial_reply"),
    ("equal_references", "different_references", "invoice_reference_absent"),
)
_INSPIRATION = ("G02", "G01, G04", "G03", "G05", "G04")


@dataclass(frozen=True)
class DevelopmentBatch:
    """Only investigations go to a candidate; manifest must remain separate."""

    investigations: dict[str, bytes]
    manifest: bytes


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False,
                       allow_nan=False) + "\n").encode("utf-8")


def _money(cents: int) -> str:
    return format(Decimal(cents).scaleb(-2), ".2f")


def _time(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


class _Case:
    def __init__(self, tag: str, rng: random.Random):
        self.tag, self.rng = tag, rng
        self.start = datetime(2026, 1, 1, 10, tzinfo=timezone.utc) + timedelta(
            days=rng.randrange(240),
        )
        self.currency = rng.choice(("USD", "EUR", "GBP"))
        self.data = {
            "schema_version": "1.0",
            "case": {"case_id": f"CASE-{tag}", "primary_alert_id": f"ALT-{tag}",
                     "policy_id": "POLICY-AML-V1"},
            "customer": {
                "customer_id": f"CUST-{tag}", "name": f"Fictional Development Business {tag}",
                "customer_type": "business", "industry": "trade_supplies",
                "onboarding_date": "2023-01-01", "profile_last_verified": "2025-12-01",
                "expected_monthly_activity": {
                    "minimum": "10000.00", "maximum": "30000.00", "currency": self.currency,
                },
            },
            "accounts": [{"account_id": f"ACC-{tag}", "customer_id": f"CUST-{tag}",
                          "account_type": "business_current", "currency": self.currency,
                          "opened_at": "2023-01-01"}],
            "counterparties": [], "transactions": [], "evidence": [],
            "verification_checks": [],
            "alert": {"alert_id": f"ALT-{tag}", "customer_id": f"CUST-{tag}"},
        }
        self.evidence("trading_profile", "synthetic_profile_record", [], {
            "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                               "Saturday", "Sunday"],
            "premises": {"type": "trade_unit", "visit_record": None},
            "staff_count": rng.randrange(3, 24),
            "seasonal_activity_reported": rng.choice((True, False)),
        })

    def counterparty(self) -> str:
        identifier = f"CP-{self.tag}-01"
        self.data["counterparties"].append({
            "counterparty_id": identifier, "display_name": f"Fictional Trade Contact {self.tag}",
            "relationship_status": "recorded_contact",
        })
        return identifier

    def transaction(self, kind: str, direction: str, when: datetime,
                    counterparty: str | None = None, cents: int | None = None) -> str:
        identifier = f"TX-{self.tag}-{len(self.data['transactions']) + 1:02d}"
        self.data["transactions"].append({
            "transaction_id": identifier, "account_id": f"ACC-{self.tag}",
            "transaction_type": kind, "direction": direction,
            "amount": _money(self.rng.randrange(2_000_000, 6_000_000) if cents is None else cents),
            "currency": self.currency, "occurred_at": _time(when),
            "counterparty_id": counterparty, "description": "Fictional trade transaction",
        })
        return identifier

    def evidence(self, kind: str, source: str, transactions: list[str], facts: dict) -> str:
        identifier = f"EV-{self.tag}-{len(self.data['evidence']) + 1:02d}"
        self.data["evidence"].append({
            "evidence_id": identifier, "evidence_type": kind, "source": source,
            "verification_status": "recorded", "related_transaction_ids": transactions,
            "facts": facts,
        })
        return identifier

    def check(self, kind: str, evidence: list[str], findings: list[str]) -> None:
        self.data["verification_checks"].append({
            "check_id": f"CHK-{self.tag}-{len(self.data['verification_checks']) + 1:02d}",
            "check_type": kind, "status": "recorded", "subject_evidence_ids": evidence,
            "findings": findings,
        })

    def finish(self, rule: str, flagged: list[str]) -> dict:
        self.data["transactions"].sort(key=lambda record: record["occurred_at"])
        latest = max(datetime.fromisoformat(record["occurred_at"])
                     for record in self.data["transactions"])
        alert_time = latest + timedelta(hours=20)
        self.data["alert"].update(
            rule_id=rule, created_at=_time(alert_time), transaction_ids=flagged,
        )
        self.data["case"]["opened_at"] = _time(alert_time + timedelta(hours=1))
        return self.data


def _incoming(case: _Case, mode: str) -> dict:
    party = case.counterparty()
    transaction = case.transaction("domestic_transfer", "credit", case.start, party)
    amount = case.data["transactions"][0]["amount"]
    purpose = case.rng.choice(("Wholesale goods", "Advance order", "Equipment sale"))
    ledger = case.evidence("payment_record", "synthetic_bank_ledger", [transaction], {
        "recorded_amount": amount, "currency": case.currency, "sender_reference": party,
    })
    invoice_ref = None if mode == "explanation_only" else f"INV-{case.tag}"
    sources = [ledger, case.evidence("customer_explanation", "customer_supplied", [transaction], {
        "claim": purpose, "invoice_reference": invoice_ref,
    })]
    if invoice_ref:
        sources.append(case.evidence("supplier_invoice", "customer_supplied", [transaction], {
            "invoice_reference": invoice_ref, "invoice_total": amount,
            "currency": case.currency, "description": purpose,
        }))
    if mode == "invoice_and_dispatch":
        sources.append(case.evidence("dispatch_record", "synthetic_carrier_record", [transaction], {
            "invoice_reference": invoice_ref,
            "dispatched_at": _time(case.start - timedelta(days=2)),
            "recorded_items": [{"description": "Trade goods",
                                "quantity": case.rng.randrange(5, 40)}],
        }))
    types = [item["evidence_type"] for item in case.data["evidence"][1:]]
    case.check("supplied_document_inventory", sources, [
        f"Supplied document types: {', '.join(types)}.",
        "Recorded sources have not been independently authenticated by this program.",
    ])
    case.transaction("domestic_transfer", "credit", case.start + timedelta(hours=2), party, 125_050)
    return case.finish("UNUSUAL_INCOMING_PAYMENT", [transaction])


def _cash(case: _Case, mode: str) -> dict:
    case.data["customer"]["industry"] = "grocery_retail"
    case.data["evidence"][0]["facts"]["seasonal_activity_reported"] = True
    case.data["customer"]["expected_monthly_activity"].update(
        typical_daily_cash_deposit_min="1000.00", typical_daily_cash_deposit_max="3000.00",
    )
    transactions = [case.transaction("cash_deposit", "credit", case.start + timedelta(days=day),
                                     cents=case.rng.randrange(650_000, 950_000))
                    for day in range(case.rng.randrange(3, 6))]
    records = case.data["transactions"]
    covered = len(records) if mode == "complete_sales" else (
        len(records) - 1 if mode == "partial_sales" else 0
    )
    total = sum((Decimal(record["amount"]) for record in records), Decimal(0))
    sales = sum((Decimal(record["amount"]) for record in records[:covered]), Decimal(0))
    sources = [case.evidence("promotion_notice", "customer_supplied", [], {
        "claim": "Seasonal promotion", "promotion_dates": [record["occurred_at"][:10]
                                                            for record in records],
    })]
    if covered:
        sources.append(case.evidence("point_of_sale_summary", "synthetic_merchant_record",
                                     transactions[:covered], {
            "daily_sales": [record["amount"] for record in records[:covered]],
            "currency": case.currency, "summary_total": format(sales, ".2f"),
        }))
    sources.append(case.evidence("deposit_reconciliation", "synthetic_reconciliation_record",
                                 transactions, {
        "deposit_total": format(total, ".2f"), "reconciled_deposits": format(sales, ".2f"),
        "unmatched_amount": format(total - sales, ".2f"), "currency": case.currency,
        "source_record_dates": [record["occurred_at"][:10] for record in records[:covered]],
    }))
    case.check("supplied_sales_inventory", sources, [
        f"Sales records cover {covered} of {len(records)} deposit dates; supplied unmatched amount "
        f"is {format(total - sales, '.2f')} {case.currency}.",
    ])
    return case.finish("UNUSUAL_CASH_INCREASE", transactions)


def _supplier(case: _Case, mode: str) -> dict:
    party = case.counterparty()
    notice_time = case.start + timedelta(hours=4)
    offsets = {"before_instruction": (0, 2), "split_timing": (0, 8)}.get(mode, (6, 8))
    transactions = [case.transaction("international_transfer", "debit",
                                     case.start + timedelta(hours=offset), party)
                    for offset in offsets]
    old, actual = f"PAYEE-{case.tag}-A", f"PAYEE-{case.tag}-B"
    second_payee = f"PAYEE-{case.tag}-C" if mode == "different_accounts_same_supplier" else actual
    payees = [actual, second_payee]
    changed = mode == "authorized_change"
    register = case.evidence("supplier_authorization_register", "synthetic_procurement_registry",
                             transactions, {
        "approved_payee_account_refs": [old, actual] if changed else [old],
        "authorized_change_recorded": changed,
        "change_effective_at": _time(case.start + timedelta(hours=5)) if changed else None,
    })
    instruction = case.evidence("supplier_instruction_notice", "synthetic_internal_case_log",
                                transactions, {
        "issued_at": _time(notice_time), "review_required_account_ref": actual,
        "instruction": f"Payments to {actual} require senior review before release.",
    })
    ledger = case.evidence("payment_record", "synthetic_bank_ledger", transactions, {
        "payments": [{"transaction_id": record["transaction_id"], "payee_account_ref": payee,
                      "amount": record["amount"], "currency": case.currency,
                      "occurred_at": record["occurred_at"]}
                     for record, payee in zip(case.data["transactions"], payees)],
    })
    if case.rng.choice((True, False)):
        case.evidence("senior_review_entry", "synthetic_internal_case_log", transactions, {
            "recorded_at": _time(case.start - timedelta(hours=1)),
            "reviewed_account_ref": actual, "recorded_scope": "Payee account review",
        })
    case.check("supplied_payment_document_inventory", [register, instruction, ledger], [
        "Payment, instruction and register entries are supplied for comparison.",
        "Any supplied senior-review entry is a recorded source, "
        "not work performed by this program.",
    ])
    return case.finish("REPEATED_PAYEE_EXCEPTION", transactions)


def _incomplete(case: _Case, mode: str) -> dict:
    account_missing = mode in ("missing_account", "missing_both")
    purpose_missing = mode != "missing_account"
    party = None if account_missing else case.counterparty()
    transaction = case.transaction("international_transfer", "debit", case.start, party)
    requested = (["beneficiary_account_reference"] if account_missing else []) + (
        ["commercial_purpose"] if purpose_missing else []
    )
    if mode == "partial_reply":
        requested = ["beneficiary_account_reference", "commercial_purpose"]
    ledger = case.evidence("payment_record", "synthetic_bank_ledger", [transaction], {
        "amount": case.data["transactions"][0]["amount"], "currency": case.currency,
        "beneficiary_account_ref": None if account_missing else f"PAYEE-{case.tag}",
        "commercial_purpose": None if purpose_missing else "Customer states trade settlement",
    })
    request = case.evidence("information_request", "synthetic_case_log", [transaction], {
        "requested_fields": requested, "requested_at": _time(case.start + timedelta(hours=1)),
        "response_status": "partial_response" if mode == "partial_reply" else "not_received",
        "supplied_fields": ["beneficiary_account_reference"] if mode == "partial_reply" else [],
    })
    case.check("supplied_information_inventory", [ledger, request], [
        "Null fields indicate information absent from this supplied record set.",
    ])
    return case.finish("BENEFICIARY_INFORMATION_INCOMPLETE", [transaction])


def _comparison(case: _Case, mode: str) -> dict:
    party = case.counterparty()
    transaction = case.transaction("international_transfer", "debit", case.start, party)
    amount = case.data["transactions"][0]["amount"]
    invoice_ref = None if mode == "invoice_reference_absent" else f"PAYEE-{case.tag}-A"
    wire_ref = f"PAYEE-{case.tag}-{'B' if mode == 'different_references' else 'A'}"
    invoice = case.evidence("supplier_invoice", "customer_supplied", [transaction], {
        "invoice_total": amount, "currency": case.currency,
        "beneficiary_account_ref": invoice_ref, "issued_at": _time(case.start - timedelta(days=2)),
    })
    wire = case.evidence("wire_payment_record", "synthetic_bank_ledger", [transaction], {
        "wire_amount": amount, "currency": case.currency, "beneficiary_account_ref": wire_ref,
    })
    case.check("supplied_account_reference_inventory", [invoice, wire], [
        f"Invoice records {invoice_ref!r}; wire record records {wire_ref!r}.",
        "These supplied records do not establish invoice authenticity or commercial purpose.",
    ])
    return case.finish("PAYMENT_RECORD_REVIEW", [transaction])


def _configuration(seed: int, count: int) -> None:
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer")


def generate_development_batch(*, seed: int, count: int = 50) -> DevelopmentBatch:
    """Build and validate a reproducible batch in memory, with a separate manifest."""
    _configuration(seed, count)
    rng = random.Random(seed)
    offsets = [rng.randrange(len(modes)) for modes in _MODES]
    artifacts, entries = {}, []
    builders = (_incoming, _cash, _supplier, _incomplete, _comparison)
    for index in range(count):
        family_index = index % len(FAMILIES)
        family = FAMILIES[family_index]
        modes = _MODES[family_index]
        mode = modes[(index // len(FAMILIES) + offsets[family_index]) % len(modes)]
        tag = f"DEV-S{seed}-{index + 1:04d}"
        data = builders[family_index](_Case(tag, rng), mode)
        payload = _json_bytes(data)
        InvestigationInput.model_validate_json(payload)
        filename = f"{data['case']['case_id']}.json"
        artifacts[filename] = payload
        entries.append({
            "case_id": data["case"]["case_id"], "scenario_family_id": family,
            "case_family_id": f"development-{family}-v{TEMPLATE_VERSION}",
            "template_version": TEMPLATE_VERSION, "source_condition": mode,
            "input_path": filename, "input_sha256": sha256(payload).hexdigest(),
        })
    manifest = {
        "manifest_schema_version": "1.0", "generator_version": GENERATOR_VERSION,
        "input_schema_version": "1.0", "dataset_partition": "development", "seed": seed,
        "case_count": count, "scenario_family_counts": dict(Counter(
            entry["scenario_family_id"] for entry in entries
        )),
        "lineage": {
            "shared_generator_templates": True, "independently_authored_cases": False,
            "reference_answers_used": False, "adjudicated_labels_included": False,
            "description": "New fictional templates inspired by exposed development inputs; "
                           "instances share family lineage and are not held-out examples.",
            "templates": [{"scenario_family_id": family, "template_version": TEMPLATE_VERSION,
                           "conceptual_source_inputs": [f"data/golden_cases/inputs/{tag}.json"
                                                        for tag in inspiration.split(', ')]}
                          for family, inspiration in zip(FAMILIES, _INSPIRATION)],
        },
        "usage": "Supply only an investigation file to a candidate; keep this manifest separate.",
        "cases": entries,
    }
    return DevelopmentBatch(artifacts, _json_bytes(manifest))


def write_development_batch(output_dir: str | Path, *, seed: int, count: int = 50) -> dict:
    """Validate first, then publish a new directory; existing destinations are refused.

    Staging/lock files are cleaned on ordinary failures. A process interruption
    may leave a hidden staging directory or lock for human inspection, never a
    partially populated published directory. Parent directories may be created.
    """
    _configuration(seed, count)
    target = Path(output_dir).absolute()
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Output destination already exists: {target}")
    batch = generate_development_batch(seed=seed, count=count)
    manifest = json.loads(batch.manifest)
    # Revalidate bytes at the publication boundary, including manifest integrity.
    if (len(batch.investigations) != count or len(manifest["cases"]) != count
            or {entry["input_path"] for entry in manifest["cases"]} != set(batch.investigations)):
        raise ValueError("Generated batch count does not match configuration")
    for entry in manifest["cases"]:
        payload = batch.investigations[entry["input_path"]]
        model = InvestigationInput.model_validate_json(payload)
        if (model.case.case_id != entry["case_id"]
                or entry["input_path"] != f"{model.case.case_id}.json"
                or sha256(payload).hexdigest() != entry["input_sha256"]):
            raise ValueError("Generated manifest identity or digest mismatch")
    target.parent.mkdir(parents=True, exist_ok=True)
    lock = target.parent / f".{target.name}.generation.lock"
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.close(descriptor)
        with tempfile.TemporaryDirectory(
            prefix=f".{target.name}.staging-", dir=target.parent,
        ) as temp:
            staging = Path(temp) / "dataset"
            staging.mkdir()
            for name, payload in batch.investigations.items():
                (staging / name).write_bytes(payload)
            (staging / "manifest.json").write_bytes(batch.manifest)
            for name, expected in {**batch.investigations, "manifest.json": batch.manifest}.items():
                if (staging / name).read_bytes() != expected:
                    raise OSError(f"Staged artifact bytes do not match validated payload: {name}")
            if target.exists() or target.is_symlink():
                raise FileExistsError(f"Output destination already exists: {target}")
            staging.rename(target)
    finally:
        lock.unlink()
    return manifest
