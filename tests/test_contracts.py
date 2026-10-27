"""Tests for synthetic AML record contracts."""

import json
import unittest

from copy import deepcopy
from datetime import date, datetime, timedelta, timezone, tzinfo
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from pydantic import ValidationError

from aml_triage.contracts import (
    Account,
    Alert,
    CaseMetadata,
    CitedStatement,
    Contradiction,
    Counterparty,
    Customer,
    Evidence,
    InvestigationInput,
    InvestigationOutput,
    RecordCitation,
    Transaction,
    VerificationCheck,
    validate_investigation_output_references,
)


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "data" / "golden_cases" / "inputs"


def load_case(case_id: str) -> dict:
    """Load an existing synthetic golden case."""

    path = INPUTS / f"{case_id}.json"

    return json.loads(path.read_text(encoding="utf-8"))


class TestCustomerAccountContracts(unittest.TestCase):

    def test_all_five_golden_cases(self):
        """All existing customer and account records must validate."""

        for case_id in ("G01", "G02", "G03", "G04", "G05"):

            with self.subTest(case=case_id):

                data = load_case(case_id)

                customer = Customer.model_validate(
                    data["customer"]
                )

                self.assertEqual(
                    customer.customer_id,
                    data["customer"]["customer_id"],
                )

                for account_data in data["accounts"]:

                    account = Account.model_validate(
                        account_data
                    )

                    self.assertEqual(
                        account.customer_id,
                        customer.customer_id,
                    )

    def test_money_and_dates_have_correct_types(self):
        """Money must become Decimal; dates must become date objects."""

        data = load_case("G01")

        customer = Customer.model_validate(
            data["customer"]
        )

        self.assertIsInstance(
            customer.expected_monthly_activity.minimum,
            Decimal,
        )

        self.assertIsInstance(
            customer.onboarding_date,
            date,
        )

    def test_negative_expected_activity_is_rejected(self):
        """Expected monetary activity cannot be negative."""

        data = deepcopy(load_case("G01"))

        data["customer"]["expected_monthly_activity"]["minimum"] = "-100.00"

        with self.assertRaises(ValidationError):
            Customer.model_validate(data["customer"])

    def test_inverted_activity_range_is_rejected(self):
        """Maximum activity cannot be less than minimum activity."""

        data = deepcopy(load_case("G01"))

        data["customer"]["expected_monthly_activity"]["maximum"] = "100.00"

        with self.assertRaises(ValidationError):
            Customer.model_validate(data["customer"])

    def test_incomplete_daily_cash_range_is_rejected(self):
        """The two daily cash range bounds must be supplied together."""

        data = deepcopy(load_case("G01"))

        activity = data["customer"]["expected_monthly_activity"]

        activity.pop("typical_daily_cash_deposit_max")

        with self.assertRaises(ValidationError):
            Customer.model_validate(data["customer"])

    def test_invalid_account_currency_is_rejected(self):
        """Currency must follow our three-uppercase-letter format."""

        data = deepcopy(load_case("G01"))

        data["accounts"][0]["currency"] = "usd"

        with self.assertRaises(ValidationError):
            Account.model_validate(data["accounts"][0])

    def test_unknown_customer_field_is_rejected(self):
        """Unexpected customer fields must not be silently accepted."""

        data = deepcopy(load_case("G01"))

        data["customer"]["unknown_field"] = "unexpected value"

        with self.assertRaises(ValidationError):
            Customer.model_validate(data["customer"])

    def test_missing_customer_id_is_rejected(self):
        """Customer ID is required."""

        data = deepcopy(load_case("G01"))

        data["customer"].pop("customer_id")

        with self.assertRaises(ValidationError):
            Customer.model_validate(data["customer"])

    def test_invalid_profile_date_order_is_rejected(self):
        """Profile verification cannot precede onboarding."""

        data = deepcopy(load_case("G01"))

        data["customer"]["profile_last_verified"] = "2020-01-01"

        with self.assertRaises(ValidationError):
            Customer.model_validate(data["customer"])


class TestTransactionContracts(unittest.TestCase):

    def test_all_transactions_in_five_golden_cases(self):
        """Every transaction in the valid synthetic fixtures must validate."""

        for case_id in ("G01", "G02", "G03", "G04", "G05"):

            with self.subTest(case=case_id):

                data = load_case(case_id)

                for transaction_data in data["transactions"]:

                    transaction = Transaction.model_validate(
                        transaction_data
                    )

                    self.assertEqual(
                        transaction.transaction_id,
                        transaction_data["transaction_id"],
                    )

    def test_amount_and_timestamp_have_correct_types(self):
        """Amounts become Decimal and timestamps become aware datetimes."""

        transaction_data = load_case("G01")["transactions"][0]
        transaction = Transaction.model_validate(transaction_data)

        self.assertIsInstance(transaction.amount, Decimal)
        self.assertIsInstance(transaction.occurred_at, datetime)
        self.assertIsNotNone(transaction.occurred_at.utcoffset())

    def test_invalid_amounts_are_rejected(self):
        """Transaction amounts must be positive, finite, and cent-precision."""

        for amount in ("0", "-1.00", "NaN", "Infinity", "-Infinity", "1.001"):

            with self.subTest(amount=amount):

                transaction_data = deepcopy(load_case("G01")["transactions"][0])
                transaction_data["amount"] = amount

                with self.assertRaises(ValidationError):
                    Transaction.model_validate(transaction_data)

    def test_invalid_currency_and_direction_are_rejected(self):
        """Currency and direction must use their supported formats."""

        for field, value in (("currency", "usd"), ("direction", "outgoing")):

            with self.subTest(field=field):

                transaction_data = deepcopy(load_case("G01")["transactions"][0])
                transaction_data[field] = value

                with self.assertRaises(ValidationError):
                    Transaction.model_validate(transaction_data)

    def test_unsupported_transaction_type_is_rejected(self):
        transaction_data = deepcopy(load_case("G01")["transactions"][0])
        transaction_data["transaction_type"] = "crypto_transfer"

        with self.assertRaises(ValidationError):
            Transaction.model_validate(transaction_data)

    def test_naive_timestamp_is_rejected(self):
        transaction_data = deepcopy(load_case("G01")["transactions"][0])
        transaction_data["occurred_at"] = "2026-10-12T10:00:00"

        with self.assertRaises(ValidationError):
            Transaction.model_validate(transaction_data)

    def test_missing_required_fields_are_rejected(self):
        """All declared transaction fields, including nullable fields, are required."""

        for field in (
            "transaction_id",
            "account_id",
            "transaction_type",
            "direction",
            "amount",
            "currency",
            "occurred_at",
            "counterparty_id",
            "description",
        ):

            with self.subTest(field=field):

                transaction_data = deepcopy(load_case("G01")["transactions"][0])
                transaction_data.pop(field)

                with self.assertRaises(ValidationError):
                    Transaction.model_validate(transaction_data)

    def test_nullable_fields_accept_explicit_null(self):
        transaction_data = load_case("G01")["transactions"][0]
        transaction = Transaction.model_validate(transaction_data)

        self.assertIsNone(transaction.counterparty_id)
        self.assertIsNone(transaction.description)

    def test_empty_identifiers_and_counterparty_are_rejected(self):
        for field in ("transaction_id", "account_id", "counterparty_id"):

            with self.subTest(field=field):

                transaction_data = deepcopy(load_case("G02")["transactions"][0])
                transaction_data[field] = ""

                with self.assertRaises(ValidationError):
                    Transaction.model_validate(transaction_data)

    def test_unknown_field_is_rejected(self):
        transaction_data = deepcopy(load_case("G01")["transactions"][0])
        transaction_data["unknown_field"] = "unexpected value"

        with self.assertRaises(ValidationError):
            Transaction.model_validate(transaction_data)


class TestCounterpartyContracts(unittest.TestCase):

    def test_all_counterparties_in_five_golden_cases(self):
        for case_id in ("G01", "G02", "G03", "G04", "G05"):

            with self.subTest(case=case_id):
                for record in load_case(case_id)["counterparties"]:
                    counterparty = Counterparty.model_validate(record)
                    self.assertEqual(counterparty.model_dump(), record)

    def test_missing_required_fields_are_rejected(self):
        for field in ("counterparty_id", "display_name", "relationship_status"):

            with self.subTest(field=field):
                record = load_case("G02")["counterparties"][0]
                record.pop(field)

                with self.assertRaises(ValidationError):
                    Counterparty.model_validate(record)

    def test_empty_identifier_and_name_are_rejected(self):
        for field in ("counterparty_id", "display_name"):

            with self.subTest(field=field):
                record = load_case("G02")["counterparties"][0]
                record[field] = ""

                with self.assertRaises(ValidationError):
                    Counterparty.model_validate(record)

    def test_incorrect_field_types_are_rejected(self):
        for field in ("counterparty_id", "display_name", "relationship_status"):
            for value in (None, 123, True, [], {}):

                with self.subTest(field=field, value=value):
                    record = load_case("G02")["counterparties"][0]
                    record[field] = value

                    with self.assertRaises(ValidationError):
                        Counterparty.model_validate(record)

    def test_unknown_field_is_rejected(self):
        record = load_case("G02")["counterparties"][0]
        record["verified"] = True

        with self.assertRaises(ValidationError):
            Counterparty.model_validate(record)

    def test_unverified_relationship_is_preserved(self):
        record = load_case("G02")["counterparties"][0]
        counterparty = Counterparty.model_validate(record)

        self.assertEqual(counterparty.relationship_status, "unverified")
        self.assertEqual(counterparty.model_dump(), record)

    def test_relationship_status_vocabulary_is_open(self):
        record = load_case("G02")["counterparties"][0]
        record["relationship_status"] = "pending_relationship_review"

        counterparty = Counterparty.model_validate(record)

        self.assertEqual(counterparty.relationship_status, record["relationship_status"])


class TestAlertCaseMetadataContracts(unittest.TestCase):

    def test_alert_and_case_metadata_in_five_golden_cases(self):
        for case_id in ("G01", "G02", "G03", "G04", "G05"):

            with self.subTest(case=case_id):
                data = load_case(case_id)
                alert = Alert.model_validate(data["alert"])
                metadata = CaseMetadata.model_validate(data["case"])

                self.assertEqual(alert.alert_id, data["alert"]["alert_id"])
                self.assertEqual(alert.customer_id, data["alert"]["customer_id"])
                self.assertEqual(alert.rule_id, data["alert"]["rule_id"])
                self.assertEqual(alert.transaction_ids, data["alert"]["transaction_ids"])
                self.assertEqual(metadata.case_id, data["case"]["case_id"])
                self.assertEqual(metadata.primary_alert_id, data["case"]["primary_alert_id"])
                self.assertEqual(metadata.policy_id, data["case"]["policy_id"])

                for timestamp in (alert.created_at, metadata.opened_at):
                    self.assertIsInstance(timestamp, datetime)
                    self.assertIsNotNone(timestamp.tzinfo)
                    self.assertIsNotNone(timestamp.utcoffset())

    def test_cases_without_counterparties_are_accepted(self):
        for case_id in ("G01", "G05"):

            with self.subTest(case=case_id):
                data = load_case(case_id)
                counterparties = [
                    Counterparty.model_validate(record)
                    for record in data["counterparties"]
                ]

                self.assertEqual(counterparties, [])
                self.assertIsInstance(Alert.model_validate(data["alert"]), Alert)
                self.assertIsInstance(CaseMetadata.model_validate(data["case"]), CaseMetadata)

    def test_missing_required_fields_are_rejected(self):
        for model, key, fields in (
            (Alert, "alert", ("alert_id", "customer_id", "rule_id", "created_at", "transaction_ids")),
            (CaseMetadata, "case", ("case_id", "primary_alert_id", "opened_at", "policy_id")),
        ):
            for field in fields:

                with self.subTest(model=model.__name__, field=field):
                    record = load_case("G01")[key]
                    record.pop(field)

                    with self.assertRaises(ValidationError):
                        model.model_validate(record)

    def test_empty_identifiers_are_rejected(self):
        for model, key, fields in (
            (Alert, "alert", ("alert_id", "customer_id", "rule_id")),
            (CaseMetadata, "case", ("case_id", "primary_alert_id", "policy_id")),
        ):
            for field in fields:

                with self.subTest(model=model.__name__, field=field):
                    record = load_case("G01")[key]
                    record[field] = ""

                    with self.assertRaises(ValidationError):
                        model.model_validate(record)

    def test_incorrect_identifier_types_are_rejected(self):
        for model, key, fields in (
            (Alert, "alert", ("alert_id", "customer_id", "rule_id")),
            (CaseMetadata, "case", ("case_id", "primary_alert_id", "policy_id")),
        ):
            for field in fields:
                for value in (None, 123, True, [], {}):

                    with self.subTest(model=model.__name__, field=field, value=value):
                        record = load_case("G01")[key]
                        record[field] = value

                        with self.assertRaises(ValidationError):
                            model.model_validate(record)

    def test_invalid_or_naive_timestamps_are_rejected(self):
        class NoOffsetTimezone(tzinfo):
            def utcoffset(self, dt):
                return None

        for model, key, field in (
            (Alert, "alert", "created_at"),
            (CaseMetadata, "case", "opened_at"),
        ):
            for value in (
                "not-a-timestamp",
                "2026-02-30T10:00:00Z",
                "2026-10-16T10:00:00",
                "2026-10-16",
                datetime(2026, 10, 16, 10),
                datetime(2026, 10, 16, 10, tzinfo=NoOffsetTimezone()),
            ):

                with self.subTest(model=model.__name__, value=value):
                    record = load_case("G01")[key]
                    record[field] = value

                    with self.assertRaises(ValidationError):
                        model.model_validate(record)

    def test_incorrect_timestamp_types_are_rejected(self):
        for model, key, field in (
            (Alert, "alert", "created_at"),
            (CaseMetadata, "case", "opened_at"),
        ):
            for value in (None, True, [], {}, date(2026, 10, 16)):

                with self.subTest(model=model.__name__, value=value):
                    record = load_case("G01")[key]
                    record[field] = value

                    with self.assertRaises(ValidationError):
                        model.model_validate(record)

    def test_timezone_offsets_and_aware_datetimes_are_accepted(self):
        expected = datetime(2026, 10, 16, 13, tzinfo=timezone(timedelta(hours=3)))

        for model, key, field in (
            (Alert, "alert", "created_at"),
            (CaseMetadata, "case", "opened_at"),
        ):
            for value in ("2026-10-16T13:00:00+03:00", expected):

                with self.subTest(model=model.__name__, value=value):
                    record = load_case("G01")[key]
                    record[field] = value
                    timestamp = getattr(model.model_validate(record), field)

                    self.assertIsInstance(timestamp, datetime)
                    self.assertEqual(timestamp, expected)
                    self.assertEqual(timestamp.utcoffset(), timedelta(hours=3))

    def test_empty_alert_transaction_list_is_rejected(self):
        record = load_case("G01")["alert"]
        record["transaction_ids"] = []

        with self.assertRaises(ValidationError):
            Alert.model_validate(record)

    def test_empty_alert_transaction_identifier_is_rejected(self):
        for value in ([""], ["TX-G01-01", ""]):

            with self.subTest(value=value):
                record = load_case("G01")["alert"]
                record["transaction_ids"] = value

                with self.assertRaises(ValidationError):
                    Alert.model_validate(record)

    def test_incorrect_alert_transaction_list_types_are_rejected(self):
        for value in (None, "TX-G01-01", 123, True, {"TX-G01-01": True}):

            with self.subTest(value=value):
                record = load_case("G01")["alert"]
                record["transaction_ids"] = value

                with self.assertRaises(ValidationError):
                    Alert.model_validate(record)

    def test_incorrect_alert_transaction_identifier_types_are_rejected(self):
        for value in (None, 123, True, [], {}):

            with self.subTest(value=value):
                record = load_case("G01")["alert"]
                record["transaction_ids"] = ["TX-G01-01", value]

                with self.assertRaises(ValidationError):
                    Alert.model_validate(record)

    def test_unknown_fields_are_rejected(self):
        for model, key in ((Alert, "alert"), (CaseMetadata, "case")):

            with self.subTest(model=model.__name__):
                record = load_case("G01")[key]
                record["unknown_field"] = "unexpected value"

                with self.assertRaises(ValidationError):
                    model.model_validate(record)

    def test_identifiers_are_not_resolved_against_other_records(self):
        data = load_case("G01")
        data["alert"]["customer_id"] = "CUST-NOT-SUPPLIED"
        data["alert"]["rule_id"] = "RULE-NOT-SPECIFIED"
        data["alert"]["transaction_ids"] = ["TX-NOT-SUPPLIED"]
        data["case"]["primary_alert_id"] = "ALT-NOT-SUPPLIED"
        data["case"]["policy_id"] = "POLICY-NOT-SPECIFIED"

        alert = Alert.model_validate(data["alert"])
        metadata = CaseMetadata.model_validate(data["case"])

        self.assertEqual(alert.customer_id, "CUST-NOT-SUPPLIED")
        self.assertEqual(alert.rule_id, "RULE-NOT-SPECIFIED")
        self.assertEqual(alert.transaction_ids, ["TX-NOT-SUPPLIED"])
        self.assertEqual(metadata.primary_alert_id, "ALT-NOT-SUPPLIED")
        self.assertEqual(metadata.policy_id, "POLICY-NOT-SPECIFIED")


class TestEvidenceVerificationCheckContracts(unittest.TestCase):

    def test_all_evidence_and_checks_in_five_golden_cases(self):
        for case_id in ("G01", "G02", "G03", "G04", "G05"):
            data = load_case(case_id)

            for model, key in (
                (Evidence, "evidence"),
                (VerificationCheck, "verification_checks"),
            ):
                for index, record in enumerate(data[key]):

                    with self.subTest(case=case_id, model=model.__name__, index=index):
                        parsed = model.model_validate(record)
                        self.assertEqual(parsed.model_dump(), record)
                        self.assertEqual(
                            model.model_validate_json(json.dumps(record)).model_dump(),
                            record,
                        )

    def test_contextual_evidence_without_transaction_references_is_accepted(self):
        for case_id, index in (("G01", 0), ("G04", 2)):

            with self.subTest(case=case_id):
                record = load_case(case_id)["evidence"][index]
                self.assertEqual(record["related_transaction_ids"], [])

                evidence = Evidence.model_validate(record)

                self.assertEqual(evidence.related_transaction_ids, [])
                self.assertEqual(evidence.model_dump(), record)

    def test_heterogeneous_nested_facts_are_preserved(self):
        record = load_case("G01")["evidence"][0]
        record["facts"] = {
            "text": "synthetic context",
            "amount_text": "00100.00",
            "integer": 2,
            "number": 1.25,
            "boolean": True,
            "null": None,
            "list": ["note", 3, 0.5, False, None, {"nested": [[], {}]}],
            "object": {"inner": {"flag": False, "count": 0, "unknown": None}},
        }

        for method, payload in (
            (Evidence.model_validate, record),
            (Evidence.model_validate_json, json.dumps(record)),
        ):

            with self.subTest(method=method.__name__):
                evidence = method(payload)
                self.assertEqual(evidence.facts, record["facts"])
                self.assertIs(type(evidence.facts["integer"]), int)
                self.assertIs(type(evidence.facts["number"]), float)
                self.assertIs(type(evidence.facts["boolean"]), bool)
                self.assertIsNone(evidence.facts["null"])
                self.assertEqual(
                    json.loads(evidence.model_dump_json())["facts"], record["facts"]
                )

    def test_empty_facts_dictionary_is_accepted(self):
        record = load_case("G01")["evidence"][0]
        record["facts"] = {}

        self.assertEqual(Evidence.model_validate(record).facts, {})

    def test_missing_required_fields_are_rejected(self):
        for model, key, fields in (
            (Evidence, "evidence", (
                "evidence_id", "evidence_type", "source", "verification_status",
                "related_transaction_ids", "facts",
            )),
            (VerificationCheck, "verification_checks", (
                "check_id", "check_type", "status", "subject_evidence_ids", "findings",
            )),
        ):
            for field in fields:

                with self.subTest(model=model.__name__, field=field):
                    record = load_case("G01")[key][0]
                    record.pop(field)

                    with self.assertRaises(ValidationError):
                        model.model_validate(record)

    def test_empty_required_strings_are_rejected(self):
        for model, key, fields in (
            (Evidence, "evidence", (
                "evidence_id", "evidence_type", "source", "verification_status",
            )),
            (VerificationCheck, "verification_checks", ("check_id", "check_type", "status")),
        ):
            for field in fields:

                with self.subTest(model=model.__name__, field=field):
                    record = load_case("G01")[key][0]
                    record[field] = ""

                    with self.assertRaises(ValidationError):
                        model.model_validate(record)

    def test_incorrect_string_field_types_are_rejected(self):
        for model, key, fields in (
            (Evidence, "evidence", (
                "evidence_id", "evidence_type", "source", "verification_status",
            )),
            (VerificationCheck, "verification_checks", ("check_id", "check_type", "status")),
        ):
            for field in fields:
                for value in (None, 123, 1.5, True, [], {}, b"text"):

                    with self.subTest(model=model.__name__, field=field, value=value):
                        record = load_case("G01")[key][0]
                        record[field] = value

                        with self.assertRaises(ValidationError):
                            model.model_validate(record)

    def test_invalid_reference_list_structures_are_rejected(self):
        for model, key, field in (
            (Evidence, "evidence", "related_transaction_ids"),
            (VerificationCheck, "verification_checks", "subject_evidence_ids"),
        ):
            for value in (
                None, "REF-1", 123, True, {}, {"REF-1": True},
                ("REF-1",), {"REF-1"}, [None], [123], [True], [[]], [{}], [b"REF-1"],
            ):

                with self.subTest(model=model.__name__, value=value):
                    record = load_case("G01")[key][0]
                    record[field] = value

                    with self.assertRaises(ValidationError):
                        model.model_validate(record)

    def test_empty_reference_identifiers_are_rejected(self):
        for model, key, field in (
            (Evidence, "evidence", "related_transaction_ids"),
            (VerificationCheck, "verification_checks", "subject_evidence_ids"),
        ):
            for value in ([""], ["REF-1", ""]):

                with self.subTest(model=model.__name__, value=value):
                    record = load_case("G01")[key][0]
                    record[field] = value

                    with self.assertRaises(ValidationError):
                        model.model_validate(record)

    def test_invalid_findings_are_rejected(self):
        for value in (
            None, "a recorded finding", 123, True, {}, {"finding": "text"},
            ("text",), {"text"}, [None], [123], [True], [[]], [{}], [b"text"],
            [""], ["a recorded finding", ""],
        ):

            with self.subTest(value=value):
                record = load_case("G01")["verification_checks"][0]
                record["findings"] = value

                with self.assertRaises(ValidationError):
                    VerificationCheck.model_validate(record)

    def test_empty_check_lists_are_accepted(self):
        record = load_case("G01")["verification_checks"][0]
        record["subject_evidence_ids"] = []
        record["findings"] = []

        check = VerificationCheck.model_validate(record)

        self.assertEqual(check.subject_evidence_ids, [])
        self.assertEqual(check.findings, [])

    def test_facts_must_be_a_dictionary(self):
        for value in (None, "{}", 123, 1.5, True, [], [("key", "value")], b"{}"):

            with self.subTest(value=value):
                record = load_case("G01")["evidence"][0]
                record["facts"] = value

                with self.assertRaises(ValidationError):
                    Evidence.model_validate(record)

    def test_non_json_fact_values_are_rejected(self):
        for value in (
            object(), datetime(2026, 10, 16, 10), date(2026, 10, 16), Decimal("1.25"),
            b"text", bytearray(b"text"), {1, 2}, frozenset({1, 2}), (1, 2), 1j, Ellipsis,
        ):
            for facts in ({"value": value}, {"nested": [{"value": value}]}):

                with self.subTest(value_type=type(value).__name__, facts=facts):
                    record = load_case("G01")["evidence"][0]
                    record["facts"] = facts

                    with self.assertRaises(ValidationError):
                        Evidence.model_validate(record)

    def test_nonfinite_fact_numbers_are_rejected(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            for facts in ({"value": value}, {"nested": [{"value": value}]}):
                record = load_case("G01")["evidence"][0]
                record["facts"] = facts

                for method, payload in (
                    (Evidence.model_validate, record),
                    (Evidence.model_validate_json, json.dumps(record)),
                ):

                    with self.subTest(value=value, facts=facts, method=method.__name__):
                        with self.assertRaises(ValidationError):
                            method(payload)

    def test_non_string_fact_keys_are_rejected(self):
        for facts in (
            {1: "value"}, {None: "value"}, {b"key": "value"},
            {"nested": {1: "value"}}, {"nested": [{False: "value"}]},
        ):

            with self.subTest(facts=facts):
                record = load_case("G01")["evidence"][0]
                record["facts"] = facts

                with self.assertRaises(ValidationError):
                    Evidence.model_validate(record)

    def test_unknown_outer_fields_are_rejected(self):
        for model, key in ((Evidence, "evidence"), (VerificationCheck, "verification_checks")):

            with self.subTest(model=model.__name__):
                record = load_case("G01")[key][0]
                record["unknown_field"] = "unexpected value"

                with self.assertRaises(ValidationError):
                    model.model_validate(record)

    def test_type_and_status_vocabularies_are_open(self):
        for model, key, fields in (
            (Evidence, "evidence", ("evidence_type", "verification_status")),
            (VerificationCheck, "verification_checks", ("check_type", "status")),
        ):
            for field in fields:

                with self.subTest(model=model.__name__, field=field):
                    record = load_case("G01")[key][0]
                    record[field] = "custom_recorded_value"

                    self.assertEqual(model.model_validate(record).model_dump(), record)

    def test_verified_status_is_only_preserved_as_supplied_data(self):
        record = load_case("G01")["evidence"][1]
        record["source"] = "customer_supplied"

        evidence = Evidence.model_validate(record)

        self.assertEqual(evidence.verification_status, "verified")
        self.assertEqual(evidence.model_dump(), record)

    def test_reference_identifiers_are_not_resolved(self):
        record = load_case("G01")["evidence"][0]
        record["related_transaction_ids"] = ["TX-NOT-SUPPLIED"]
        check_record = load_case("G01")["verification_checks"][0]
        check_record["subject_evidence_ids"] = ["EV-NOT-SUPPLIED"]

        evidence = Evidence.model_validate(record)
        check = VerificationCheck.model_validate(check_record)

        self.assertEqual(evidence.related_transaction_ids, ["TX-NOT-SUPPLIED"])
        self.assertEqual(check.subject_evidence_ids, ["EV-NOT-SUPPLIED"])


class TestInvestigationInputContracts(unittest.TestCase):

    def assert_invalid_input(self, data, *message_fragments, location=None):
        """Check both supported entry points for JSON-compatible invalid inputs."""
        for validate, payload in (
            (InvestigationInput.model_validate, data),
            (InvestigationInput.model_validate_json, json.dumps(data)),
        ):
            with self.subTest(validation=validate.__name__):
                with self.assertRaises(ValidationError) as caught:
                    validate(payload)
                for fragment in message_fragments:
                    self.assertIn(fragment, str(caught.exception))
                if location is not None:
                    self.assertIn(location, [error["loc"] for error in caught.exception.errors()])

    def test_all_five_golden_cases_with_python_and_json(self):
        for case_id in ("G01", "G02", "G03", "G04", "G05"):
            data = load_case(case_id)
            for validate, payload in (
                (InvestigationInput.model_validate, data),
                (InvestigationInput.model_validate_json, json.dumps(data)),
            ):
                with self.subTest(case=case_id, validation=validate.__name__):
                    investigation = validate(payload)
                    self.assertEqual(
                        json.loads(investigation.model_dump_json(exclude_unset=True)), data
                    )
                    for field, model in (
                        ("case", CaseMetadata), ("customer", Customer), ("alert", Alert),
                    ):
                        self.assertIsInstance(getattr(investigation, field), model)
                    for field, model in (
                        ("accounts", Account), ("counterparties", Counterparty),
                        ("transactions", Transaction), ("evidence", Evidence),
                        ("verification_checks", VerificationCheck),
                    ):
                        for record in getattr(investigation, field):
                            self.assertIsInstance(record, model)
                    self.assertIsInstance(investigation.customer.onboarding_date, date)
                    self.assertIsInstance(investigation.transactions[0].amount, Decimal)
                    for timestamp in (
                        investigation.case.opened_at, investigation.alert.created_at,
                        investigation.transactions[0].occurred_at,
                    ):
                        self.assertIsInstance(timestamp, datetime)
                        self.assertIsNotNone(timestamp.utcoffset())

    def test_every_top_level_field_is_required(self):
        for field in (
            "schema_version", "case", "customer", "accounts", "counterparties",
            "transactions", "alert", "evidence", "verification_checks",
        ):
            with self.subTest(field=field):
                data = load_case("G01")
                data.pop(field)
                self.assert_invalid_input(data, location=(field,))

    def test_unknown_top_level_fields_and_answer_metadata_are_rejected(self):
        for field in (
            "unknown_field", "expected_action", "recommended_action", "reference_rationale",
            "rubric_version", "evaluation_label", "reference_answers",
        ):
            with self.subTest(field=field):
                data = load_case("G01")
                data[field] = "unexpected value"
                self.assert_invalid_input(data, location=(field,))

    def test_unsupported_and_incorrectly_typed_schema_versions_are_rejected(self):
        for value in ("", "1", "2.0", "1.0 ", 1, 1.0, True, None, [], {}):
            with self.subTest(value=value):
                data = load_case("G01")
                data["schema_version"] = value
                self.assert_invalid_input(data, location=("schema_version",))

        data = load_case("G01")
        data["schema_version"] = b"1.0"
        with self.assertRaises(ValidationError):
            InvestigationInput.model_validate(data)

    def test_collection_fields_require_actual_lists(self):
        for field in (
            "accounts", "counterparties", "transactions", "evidence", "verification_checks",
        ):
            for value in (None, {}, "[]", 123, True):
                with self.subTest(field=field, value=value):
                    data = load_case("G02")
                    data[field] = value
                    self.assert_invalid_input(data, location=(field,))

            records = load_case("G02")[field]
            for value in (tuple(records), iter(records), {"record"}, b"[]"):
                with self.subTest(field=field, value_type=type(value).__name__):
                    data = load_case("G02")
                    data[field] = value
                    with self.assertRaises(ValidationError):
                        InvestigationInput.model_validate(data)

    def test_incorrect_single_record_types_are_rejected(self):
        for field in ("case", "customer", "alert"):
            for value in (None, [], "record", 123, True):
                with self.subTest(field=field, value=value):
                    data = load_case("G01")
                    data[field] = value
                    self.assert_invalid_input(data, location=(field,))

    def test_invalid_nested_records_are_rejected(self):
        for field, index, nested_field, value in (
            ("case", None, "primary_alert_id", ""),
            ("customer", None, "name", ""),
            ("accounts", 0, "currency", "usd"),
            ("counterparties", 0, "display_name", ""),
            ("transactions", 0, "amount", "-1.00"),
            ("alert", None, "created_at", "2026-10-16T10:00:00"),
            ("evidence", 0, "facts", []),
            ("verification_checks", 0, "findings", [""]),
        ):
            with self.subTest(field=field, nested_field=nested_field):
                data = load_case("G02")
                record = data[field] if index is None else data[field][index]
                record[nested_field] = value
                self.assert_invalid_input(data)

    def test_identical_and_conflicting_duplicate_record_ids_are_rejected(self):
        for field, id_field, model, changed_field in (
            ("accounts", "account_id", Account, "account_type"),
            ("counterparties", "counterparty_id", Counterparty, "display_name"),
            ("transactions", "transaction_id", Transaction, "description"),
            ("evidence", "evidence_id", Evidence, "source"),
            ("verification_checks", "check_id", VerificationCheck, "status"),
        ):
            for conflicting in (False, True):
                with self.subTest(field=field, conflicting=conflicting):
                    data = load_case("G02")
                    duplicate = deepcopy(data[field][0])
                    if conflicting:
                        duplicate[changed_field] = "another recorded value"
                    model.model_validate(duplicate)
                    data[field].append(duplicate)
                    index = len(data[field]) - 1
                    self.assert_invalid_input(
                        data, f"{field}[{index}].{id_field}", "duplicate identifier",
                        duplicate[id_field],
                    )

    def test_g05_duplicate_transaction_fixture_is_rejected(self):
        data = load_case("G05_invalid_duplicate")
        self.assert_invalid_input(data, "transactions[1].transaction_id", "TX-G05-01")

    def test_case_primary_alert_must_match(self):
        data = load_case("G01")
        data["case"]["primary_alert_id"] = "ALT-OTHER"
        CaseMetadata.model_validate(data["case"])
        self.assert_invalid_input(data, "case.primary_alert_id", "alert.alert_id", "ALT-OTHER")

    def test_alert_customer_must_match(self):
        data = load_case("G01")
        data["alert"]["customer_id"] = "CUST-OTHER"
        Alert.model_validate(data["alert"])
        self.assert_invalid_input(data, "alert.customer_id", "customer.customer_id", "CUST-OTHER")

    def test_every_account_must_belong_to_the_customer(self):
        data = load_case("G01")
        account = deepcopy(data["accounts"][0])
        account["account_id"] = "ACC-OTHER"
        account["customer_id"] = "CUST-OTHER"
        Account.model_validate(account)
        data["accounts"].append(account)
        self.assert_invalid_input(data, "accounts[1].customer_id", "CUST-OTHER")

    def test_transaction_account_references_must_resolve(self):
        data = load_case("G02")
        data["transactions"][1]["account_id"] = "ACC-MISSING"
        Transaction.model_validate(data["transactions"][1])
        self.assert_invalid_input(data, "transactions[1].account_id", "ACC-MISSING")

    def test_non_null_counterparty_references_must_resolve(self):
        data = load_case("G02")
        data["transactions"][1]["counterparty_id"] = "CP-MISSING"
        Transaction.model_validate(data["transactions"][1])
        self.assert_invalid_input(data, "transactions[1].counterparty_id", "CP-MISSING")

        data = load_case("G02")
        data["counterparties"] = []
        self.assert_invalid_input(data, "transactions[0].counterparty_id", "CP-G02-01")

    def test_alert_transaction_references_must_resolve(self):
        data = load_case("G02")
        data["alert"]["transaction_ids"].append("TX-MISSING")
        Alert.model_validate(data["alert"])
        self.assert_invalid_input(data, "alert.transaction_ids[1]", "TX-MISSING")

    def test_evidence_transaction_references_must_resolve(self):
        data = load_case("G02")
        data["evidence"][1]["related_transaction_ids"].append("TX-MISSING")
        Evidence.model_validate(data["evidence"][1])
        self.assert_invalid_input(data, "evidence[1].related_transaction_ids[1]", "TX-MISSING")

    def test_check_evidence_references_must_resolve(self):
        data = load_case("G01")
        data["verification_checks"][1]["subject_evidence_ids"].append("EV-MISSING")
        VerificationCheck.model_validate(data["verification_checks"][1])
        self.assert_invalid_input(
            data, "verification_checks[1].subject_evidence_ids[2]", "EV-MISSING"
        )

    def test_duplicates_within_each_reference_list_are_rejected(self):
        for field, index, nested_field, model in (
            ("alert", None, "transaction_ids", Alert),
            ("evidence", 1, "related_transaction_ids", Evidence),
            ("verification_checks", 0, "subject_evidence_ids", VerificationCheck),
        ):
            with self.subTest(field=field):
                data = load_case("G02")
                record = data[field] if index is None else data[field][index]
                references = record[nested_field]
                references.append(references[0])
                model.model_validate(record)
                path = field if index is None else f"{field}[{index}]"
                self.assert_invalid_input(
                    data, f"{path}.{nested_field}[{len(references) - 1}]",
                    "duplicate reference", references[0],
                )

    def test_reserved_evaluation_keys_are_rejected_at_any_fact_depth(self):
        for key in (
            "expected_action", "recommended_action", "reference_rationale", "rubric_version",
        ):
            for facts in (
                {key: None},
                {"nested": {key: "value"}},
                {"items": [True, {key: False}]},
                {"levels": [[{"nested": [0, {key: {"anything": "value"}}]}]]},
            ):
                with self.subTest(key=key, facts=facts):
                    data = load_case("G02")
                    data["evidence"][1]["facts"] = facts
                    # The guard belongs only to the composed investigation contract.
                    self.assertEqual(Evidence.model_validate(data["evidence"][1]).facts, facts)
                    self.assert_invalid_input(
                        data, "evidence[1].facts", "evaluation-only key", key
                    )

    def test_empty_counterparties_and_explicit_null_references_are_preserved(self):
        for case_id in ("G01", "G05"):
            with self.subTest(case=case_id):
                data = load_case(case_id)
                investigation = InvestigationInput.model_validate(data)
                self.assertEqual(investigation.counterparties, [])
                self.assertTrue(investigation.transactions)
                for transaction in investigation.transactions:
                    self.assertIsNone(transaction.counterparty_id)

    def test_contextual_evidence_without_transaction_references_is_preserved(self):
        for case_id, evidence_id in (("G01", "EV-G01-01"), ("G04", "EV-003")):
            with self.subTest(case=case_id):
                investigation = InvestigationInput.model_validate(load_case(case_id))
                evidence = next(
                    record for record in investigation.evidence
                    if record.evidence_id == evidence_id
                )
                self.assertEqual(evidence.related_transaction_ids, [])

    def test_g04_evidence_can_reference_transactions_outside_the_alert(self):
        investigation = InvestigationInput.model_validate(load_case("G04"))

        self.assertIn("TX-105", [record.transaction_id for record in investigation.transactions])
        self.assertNotIn("TX-105", investigation.alert.transaction_ids)
        invoice = next(record for record in investigation.evidence if record.evidence_id == "EV-004")
        self.assertEqual(invoice.related_transaction_ids, ["TX-105"])

    def test_g05_missing_beneficiary_information_remains_valid(self):
        investigation = InvestigationInput.model_validate(load_case("G05"))

        self.assertIsNone(investigation.transactions[0].counterparty_id)
        self.assertIsNone(investigation.evidence[0].facts["beneficiary_account_ref"])
        self.assertEqual(investigation.verification_checks[0].status, "unresolved")

    def test_empty_check_reference_and_findings_lists_remain_valid(self):
        data = load_case("G01")
        data["verification_checks"][0]["subject_evidence_ids"] = []
        data["verification_checks"][0]["findings"] = []

        investigation = InvestigationInput.model_validate(data)

        self.assertEqual(investigation.verification_checks[0].subject_evidence_ids, [])
        self.assertEqual(investigation.verification_checks[0].findings, [])

    def test_empty_evidence_and_check_collections_are_permitted_when_references_allow(self):
        for clear_evidence in (False, True):
            with self.subTest(clear_evidence=clear_evidence):
                data = load_case("G01")
                data["verification_checks"] = []
                if clear_evidence:
                    data["evidence"] = []

                investigation = InvestigationInput.model_validate(data)

                self.assertEqual(investigation.verification_checks, [])
                self.assertEqual(len(investigation.evidence), len(data["evidence"]))

    def test_empty_accounts_or_transactions_fail_on_references(self):
        for field, error_path in (
            ("accounts", "transactions[0].account_id"),
            ("transactions", "alert.transaction_ids[0]"),
        ):
            with self.subTest(field=field):
                data = load_case("G01")
                data[field] = []
                self.assert_invalid_input(data, error_path, "unknown reference")

    def test_supplied_but_unreferenced_records_and_separate_id_namespaces_are_valid(self):
        data = load_case("G02")
        for field, id_field in (
            ("accounts", "account_id"), ("counterparties", "counterparty_id"),
            ("transactions", "transaction_id"), ("evidence", "evidence_id"),
            ("verification_checks", "check_id"),
        ):
            record = deepcopy(data[field][0])
            record[id_field] = "UNREFERENCED"
            data[field].append(record)

        investigation = InvestigationInput.model_validate(data)

        self.assertEqual(json.loads(investigation.model_dump_json(exclude_unset=True)), data)
        self.assertNotIn("UNREFERENCED", investigation.alert.transaction_ids)
        self.assertNotIn(
            "UNREFERENCED",
            [record.account_id for record in investigation.transactions],
        )
        self.assertNotIn(
            "UNREFERENCED",
            [record.counterparty_id for record in investigation.transactions],
        )
        for check in investigation.verification_checks:
            self.assertNotIn("UNREFERENCED", check.subject_evidence_ids)

    def test_references_across_separate_records_and_repeated_findings_are_valid(self):
        data = load_case("G01")
        evidence = deepcopy(data["evidence"][1])
        evidence["evidence_id"] = "EV-ANOTHER"
        data["evidence"].append(evidence)
        check = deepcopy(data["verification_checks"][0])
        check["check_id"] = "CHK-ANOTHER"
        check["findings"] *= 2
        data["verification_checks"].append(check)

        investigation = InvestigationInput.model_validate(data)

        self.assertEqual(
            investigation.evidence[-1].related_transaction_ids,
            investigation.evidence[1].related_transaction_ids,
        )
        self.assertEqual(
            investigation.verification_checks[-1].subject_evidence_ids,
            investigation.verification_checks[0].subject_evidence_ids,
        )
        self.assertEqual(investigation.verification_checks[-1].findings, check["findings"])
        self.assertEqual(len(investigation.verification_checks[-1].findings), 2)

    def test_submitted_order_and_nested_values_are_preserved_without_mutation(self):
        data = load_case("G04")
        for field, id_field in (("accounts", "account_id"), ("counterparties", "counterparty_id")):
            record = deepcopy(data[field][0])
            record[id_field] = "ZZ-UNREFERENCED"
            data[field].append(record)
        data["evidence"][0]["facts"]["nested"] = {
            "values": ["001.00", 1, 1.25, True, None, {"items": [False, [], {}]}]
        }
        data["alert"]["transaction_ids"].reverse()
        for record in data["evidence"]:
            record["related_transaction_ids"].reverse()
        for record in data["verification_checks"]:
            record["subject_evidence_ids"].reverse()
            record["findings"] += ["Recorded note B", "Recorded note A", "Recorded note B"]
        for field in (
            "accounts", "counterparties", "transactions", "evidence", "verification_checks",
        ):
            data[field].reverse()
        original = deepcopy(data)

        for validate, payload in (
            (InvestigationInput.model_validate, data),
            (InvestigationInput.model_validate_json, json.dumps(data)),
        ):
            with self.subTest(validation=validate.__name__):
                investigation = validate(payload)
                self.assertEqual(
                    json.loads(investigation.model_dump_json(exclude_unset=True)), original
                )
                self.assertEqual(data, original)

    def test_ordinary_words_and_reserved_key_text_are_not_banned(self):
        data = load_case("G01")
        data["evidence"][0]["facts"] = {
            "description": "close investigate escalate expected_action recommended_action",
            "reference_rationale_notes": "rubric_version",
        }
        data["verification_checks"][0]["findings"] = [
            "The supplied text mentions close, escalate, and reference_rationale."
        ]

        investigation = InvestigationInput.model_validate(data)

        self.assertEqual(investigation.evidence[0].facts, data["evidence"][0]["facts"])
        self.assertEqual(
            investigation.verification_checks[0].findings,
            data["verification_checks"][0]["findings"],
        )

    def test_validation_requires_no_reference_or_policy_file_reads(self):
        data = load_case("G01")
        data["case"]["policy_id"] = "POLICY-NOT-IN-REPOSITORY"
        json_payload = json.dumps(data)

        with patch("builtins.open", side_effect=OSError("unexpected file read")), patch.object(
            Path, "open", side_effect=OSError("unexpected file read")
        ):
            for validate, payload in (
                (InvestigationInput.model_validate, data),
                (InvestigationInput.model_validate_json, json_payload),
            ):
                with self.subTest(validation=validate.__name__):
                    investigation = validate(payload)
                    self.assertEqual(investigation.case.policy_id, data["case"]["policy_id"])

    def test_no_additional_temporal_or_currency_relationships_are_imposed(self):
        data = load_case("G04")
        data["case"]["opened_at"] = "2020-01-01T00:00:00Z"
        data["accounts"][0]["currency"] = "EUR"
        data["customer"]["expected_monthly_activity"]["currency"] = "GBP"

        investigation = InvestigationInput.model_validate(data)

        self.assertEqual(investigation.case.opened_at.year, 2020)
        self.assertEqual(investigation.accounts[0].currency, "EUR")
        self.assertEqual(investigation.customer.expected_monthly_activity.currency, "GBP")
        self.assertEqual(investigation.transactions[0].currency, "USD")


class TestInvestigationOutputContracts(unittest.TestCase):

    def citation(self, record_type="transaction", record_id="TX-OUTPUT-01"):
        return {"record_type": record_type, "record_id": record_id}

    def statement(self, text="A synthetic ledger row records a transfer.", citations=None):
        return {
            "statement": text,
            "citations": [self.citation()] if citations is None else citations,
        }

    def contradiction(self):
        return {
            "description": "Two supplied notes describe different destinations.",
            "left": self.statement(
                "The first note names destination A.", [self.citation("evidence", "EV-OUT-A")]
            ),
            "right": self.statement(
                "The second note names destination B.", [self.citation("evidence", "EV-OUT-B")]
            ),
        }

    def candidate_output(self, action="investigate"):
        """Author candidate data independently of golden inputs and reference answers."""
        return {
            "schema_version": "1.0",
            "case_id": "CASE-OUTPUT-01",
            "alert_id": "ALERT-OUTPUT-01",
            "assessment_status": "recommendation_provided",
            "recommended_action": action,
            "rationale": self.statement("A preliminary recommendation is submitted for review."),
            "factual_findings": [self.statement()],
            "interpretations": [self.statement("The recorded destination needs clarification.")],
            "unresolved_questions": [],
            "missing_information": [],
            "contradictions": [],
            "recommendation_scope": "preliminary",
            "human_review_required": True,
        }

    def abstention(self):
        data = self.candidate_output()
        data.update(
            assessment_status="unable_to_recommend",
            recommended_action=None,
            rationale=self.statement("The available context cannot support a recommendation.", []),
            factual_findings=[],
            interpretations=[],
        )
        return data

    def assert_valid_record(self, model, data):
        for validate, payload in (
            (model.model_validate, data),
            (model.model_validate_json, json.dumps(data)),
        ):
            with self.subTest(model=model.__name__, validation=validate.__name__):
                parsed = validate(payload)
                self.assertEqual(parsed.model_dump(), data)
                self.assertEqual(json.loads(parsed.model_dump_json()), data)
        return parsed

    def assert_invalid_record(self, model, data, *message_fragments):
        for validate, payload in (
            (model.model_validate, data),
            (model.model_validate_json, json.dumps(data)),
        ):
            with self.subTest(model=model.__name__, validation=validate.__name__):
                with self.assertRaises(ValidationError) as caught:
                    validate(payload)
                for fragment in message_fragments:
                    self.assertIn(fragment, str(caught.exception))

    def test_all_record_namespaces_are_accepted(self):
        for namespace in (
            "case", "customer", "account", "counterparty", "transaction", "alert",
            "evidence", "verification_check",
        ):
            with self.subTest(namespace=namespace):
                self.assert_valid_record(RecordCitation, self.citation(namespace, "RECORD-01"))

    def test_preliminary_dispositions_are_accepted(self):
        for action in ("close", "investigate", "escalate"):
            with self.subTest(action=action):
                data = self.candidate_output(action)
                parsed = self.assert_valid_record(InvestigationOutput, data)
                self.assertIsInstance(parsed.rationale, CitedStatement)
                self.assertIsInstance(parsed.factual_findings[0].citations[0], RecordCitation)
                self.assertIs(parsed.human_review_required, True)

    def test_abstention_accepts_null_action_and_uncited_rationale(self):
        data = self.abstention()
        self.assert_valid_record(InvestigationOutput, data)
        data["factual_findings"] = [self.statement()]
        data["interpretations"] = [self.statement("The supplied context has limits.")]
        self.assert_valid_record(InvestigationOutput, data)

    def test_every_field_is_required_at_each_model_level(self):
        for model, original in (
            (RecordCitation, self.citation()),
            (CitedStatement, self.statement()),
            (Contradiction, self.contradiction()),
            (InvestigationOutput, self.candidate_output()),
            (InvestigationOutput, self.abstention()),
        ):
            for field in original:
                with self.subTest(model=model.__name__, field=field):
                    data = deepcopy(original)
                    data.pop(field)
                    self.assert_invalid_record(model, data, field, "Field required")

    def test_unknown_fields_are_rejected_at_every_model_level(self):
        for model, original in (
            (RecordCitation, self.citation()),
            (CitedStatement, self.statement()),
            (Contradiction, self.contradiction()),
            (InvestigationOutput, self.candidate_output()),
        ):
            data = deepcopy(original)
            data["unexpected"] = "extra supplied value"
            self.assert_invalid_record(model, data, "unexpected", "Extra inputs")

        for field in (
            "confidence", "final_decision", "escalation_criteria_met", "narrative",
            "execution_metadata", "expected_action", "reference_rationale", "rubric_version",
        ):
            data = self.candidate_output()
            data[field] = "unexpected"
            self.assert_invalid_record(InvestigationOutput, data, field, "Extra inputs")

        for path in (
            ("rationale",), ("rationale", "citations", 0), ("factual_findings", 0),
            ("contradictions", 0), ("contradictions", 0, "left"),
            ("contradictions", 0, "right", "citations", 0),
        ):
            data = self.candidate_output()
            data["contradictions"] = [self.contradiction()]
            nested = data
            for part in path:
                nested = nested[part]
            nested["unexpected"] = "extra nested value"
            self.assert_invalid_record(InvestigationOutput, data, "unexpected", "Extra inputs")

    def test_identifiers_require_strict_non_whitespace_strings(self):
        for model, original, field in (
            (RecordCitation, self.citation(), "record_id"),
            (InvestigationOutput, self.candidate_output(), "case_id"),
            (InvestigationOutput, self.candidate_output(), "alert_id"),
        ):
            for value in ("", " \t\r\n", "\u00a0\u2003", "\x1c", None, 1, 1.5, True, [], {}):
                with self.subTest(model=model.__name__, field=field, value=value):
                    data = deepcopy(original)
                    data[field] = value
                    self.assert_invalid_record(model, data, field)

    def test_statements_and_descriptions_require_non_whitespace_strings(self):
        for model, original, field in (
            (CitedStatement, self.statement(), "statement"),
            (Contradiction, self.contradiction(), "description"),
        ):
            for value in ("", " \t\r\n", "\u00a0\u2003", "\x1c", None, 1, 1.5, True, [], {}):
                with self.subTest(model=model.__name__, field=field, value=value):
                    data = deepcopy(original)
                    data[field] = value
                    self.assert_invalid_record(model, data, field)

        for status_data in (self.candidate_output(), self.abstention()):
            status_data["rationale"]["statement"] = " \n"
            self.assert_invalid_record(InvestigationOutput, status_data, "rationale", "statement")

    def test_unsupported_record_namespaces_are_rejected(self):
        for value in ("", "policy", "Transaction", "transaction ", None, 1, True, [], {}):
            with self.subTest(value=value):
                data = self.citation()
                data["record_type"] = value
                self.assert_invalid_record(RecordCitation, data, "record_type")

    def test_unsupported_statuses_and_actions_are_rejected(self):
        for field, values in (
            ("assessment_status", ("", "complete", "recommendation_provided ", None, 1, True, [])),
            ("recommended_action", ("", "abstain", "sar", "Close", "close ", "null", 1, True, {})),
        ):
            for value in values:
                with self.subTest(field=field, value=value):
                    data = self.candidate_output()
                    data[field] = value
                    self.assert_invalid_record(InvestigationOutput, data, field)

    def test_invalid_status_action_combinations_are_rejected(self):
        data = self.candidate_output()
        data["recommended_action"] = None
        self.assert_invalid_record(InvestigationOutput, data, "recommended_action")
        for action in ("close", "investigate", "escalate"):
            with self.subTest(action=action):
                data = self.abstention()
                data["recommended_action"] = action
                self.assert_invalid_record(InvestigationOutput, data, "recommended_action", "null")

    def test_schema_version_requires_exact_string(self):
        for value in ("", "1", "2.0", "1.0 ", 1, 1.0, True, None, [], {}):
            with self.subTest(value=value):
                data = self.candidate_output()
                data["schema_version"] = value
                self.assert_invalid_record(InvestigationOutput, data, "schema_version")

    def test_human_review_requires_exact_boolean_true(self):
        for original in (self.candidate_output(), self.abstention()):
            for value in (False, 1, 1.0, 0, -1, "true", "True", "", None, [], {}):
                with self.subTest(status=original["assessment_status"], value=value):
                    data = deepcopy(original)
                    data["human_review_required"] = value
                    self.assert_invalid_record(InvestigationOutput, data, "human_review_required")

    def test_recommendation_scope_requires_preliminary(self):
        for original in (self.candidate_output(), self.abstention()):
            for value in ("", "final", "Preliminary", "preliminary ", True, 1, None, [], {}):
                with self.subTest(status=original["assessment_status"], value=value):
                    data = deepcopy(original)
                    data["recommendation_scope"] = value
                    self.assert_invalid_record(InvestigationOutput, data, "recommendation_scope")

    def test_collection_fields_require_actual_lists(self):
        for model, original, fields in (
            (CitedStatement, self.statement(), ("citations",)),
            (InvestigationOutput, self.candidate_output(), (
                "factual_findings", "interpretations", "unresolved_questions",
                "missing_information", "contradictions",
            )),
        ):
            for field in fields:
                for value in (None, "[]", 1, True, {}, [None], [1], ["text"], [[]]):
                    with self.subTest(model=model.__name__, field=field, value=value):
                        data = deepcopy(original)
                        data[field] = value
                        self.assert_invalid_record(model, data, field)

                for value in (tuple(original[field]), iter(original[field]), {"item"}, b"[]"):
                    with self.subTest(model=model.__name__, field=field, type=type(value).__name__):
                        data = deepcopy(original)
                        data[field] = value
                        with self.assertRaises(ValidationError):
                            model.model_validate(data)

    def test_python_only_incorrect_scalar_types_are_rejected(self):
        for model, original, fields in (
            (RecordCitation, self.citation(), ("record_type", "record_id")),
            (CitedStatement, self.statement(), ("statement",)),
            (Contradiction, self.contradiction(), ("description",)),
            (InvestigationOutput, self.candidate_output(), (
                "schema_version", "case_id", "alert_id", "assessment_status",
                "recommended_action", "recommendation_scope", "human_review_required",
            )),
        ):
            for field in fields:
                for value in (b"text", bytearray(b"text"), Decimal("1"), object()):
                    with self.subTest(model=model.__name__, field=field, type=type(value).__name__):
                        data = deepcopy(original)
                        data[field] = value
                        with self.assertRaises(ValidationError):
                            model.model_validate(data)

    def test_invalid_nested_records_are_rejected(self):
        for value in (None, "text", 1, True, [], {}):
            data = self.candidate_output()
            data["rationale"] = value
            self.assert_invalid_record(InvestigationOutput, data, "rationale")

        for side in ("left", "right"):
            for value in (None, "text", 1, True, [], {}):
                data = self.contradiction()
                data[side] = value
                self.assert_invalid_record(Contradiction, data, side)

        for path, value in (
            (("rationale", "citations", 0, "record_type"), "invented_namespace"),
            (("factual_findings", 0, "citations", 0, "record_id"), " \t"),
            (("interpretations", 0, "statement"), ""),
            (("unresolved_questions", 0, "statement"), None),
            (("missing_information", 0, "citations"), {}),
            (("contradictions", 0, "right", "statement"), " \n"),
        ):
            data = self.candidate_output()
            data["unresolved_questions"] = [self.statement("What is the destination?", [])]
            data["missing_information"] = [self.statement("Destination details are missing.", [])]
            data["contradictions"] = [self.contradiction()]
            nested = data
            for part in path[:-1]:
                nested = nested[part]
            nested[path[-1]] = value
            self.assert_invalid_record(InvestigationOutput, data, str(path[0]))

    def test_factual_findings_and_interpretations_always_require_citations(self):
        for original in (self.candidate_output(), self.abstention()):
            for field in ("factual_findings", "interpretations"):
                data = deepcopy(original)
                data[field] = [self.statement(), self.statement("An uncited assertion.", [])]
                self.assert_invalid_record(InvestigationOutput, data, f"{field}[1].citations")

    def test_recommendations_require_at_least_one_factual_finding(self):
        for action in ("close", "investigate", "escalate"):
            data = self.candidate_output(action)
            data["factual_findings"] = []
            self.assert_invalid_record(InvestigationOutput, data, "factual_findings")

    def test_recommendation_rationale_requires_citations(self):
        for action in ("close", "investigate", "escalate"):
            data = self.candidate_output(action)
            data["rationale"]["citations"] = []
            self.assert_invalid_record(InvestigationOutput, data, "rationale.citations")

    def test_contradiction_sides_require_citations(self):
        for sides in (("left",), ("right",), ("left", "right")):
            data = self.contradiction()
            for side in sides:
                data[side]["citations"] = []
            self.assert_invalid_record(Contradiction, data, f"{sides[0]}.citations")
            output = self.candidate_output()
            output["contradictions"] = [data]
            self.assert_invalid_record(InvestigationOutput, output, "contradictions")

    def test_duplicate_citations_within_a_statement_are_rejected(self):
        data = self.statement(citations=[self.citation(), self.citation()])
        self.assert_invalid_record(CitedStatement, data, "citations[1]", "duplicate citation")
        output = self.candidate_output()
        output["rationale"] = data
        self.assert_invalid_record(InvestigationOutput, output, "rationale", "duplicate citation")

    def test_citation_reuse_and_exact_identifier_namespaces_are_preserved(self):
        citations = [
            self.citation("transaction", "SHARED"), self.citation("evidence", "SHARED"),
            self.citation("transaction", " SHARED "), self.citation("transaction", "shared"),
        ]
        statement = self.statement(citations=citations)
        self.assert_valid_record(CitedStatement, statement)
        data = self.candidate_output()
        data["rationale"] = deepcopy(statement)
        data["factual_findings"] = [deepcopy(statement), deepcopy(statement)]
        data["interpretations"] = [deepcopy(statement)]
        data["contradictions"] = [{
            "description": "Two accounts cite different portions of the same records.",
            "left": deepcopy(statement),
            "right": deepcopy(statement),
        }]
        self.assert_valid_record(InvestigationOutput, data)

    def test_questions_and_missing_information_may_be_uncited(self):
        self.assert_valid_record(CitedStatement, self.statement("An unanswered question.", []))
        for data in (self.candidate_output("escalate"), self.abstention()):
            data["unresolved_questions"] = [self.statement("Why do the notes differ?", [])]
            data["missing_information"] = [
                self.statement("The destination details are absent.", [])
            ]
            self.assert_valid_record(InvestigationOutput, data)

        data = self.candidate_output()
        data["interpretations"] = []
        self.assert_valid_record(InvestigationOutput, data)

    def test_text_order_and_submitted_data_are_preserved(self):
        data = self.candidate_output()
        data["case_id"] = "  CASE-OUTPUT-01  "
        data["alert_id"] = "\tALERT-OUTPUT-01 "
        statement = self.statement(
            "  Supplied note: caf\u00e9\nSecond line.  ",
            [self.citation("evidence", " EV-OUT-B "), self.citation("transaction", "TX-OUTPUT-01")],
        )
        data["rationale"] = deepcopy(statement)
        data["factual_findings"] = [self.statement("Recorded observation B."), deepcopy(statement)]
        data["interpretations"] = [self.statement("Possible explanation B."), deepcopy(statement)]
        data["unresolved_questions"] = [self.statement("Question B?", []), self.statement("A?", [])]
        data["missing_information"] = [self.statement("Missing B.", []), self.statement("A.", [])]
        first = self.contradiction()
        second = self.contradiction()
        first["description"] = "  Conflicting notes B.\n"
        second["description"] = "Conflicting notes A."
        data["contradictions"] = [first, second]
        original = deepcopy(data)
        self.assert_valid_record(InvestigationOutput, data)
        self.assertEqual(data, original)

    def test_existing_nested_model_instances_are_accepted(self):
        citation = RecordCitation.model_validate(self.citation())
        statement = CitedStatement(statement="A supplied statement.", citations=[citation])
        contradiction = Contradiction(
            description="Two recorded views.", left=statement, right=statement
        )
        data = self.candidate_output()
        data["rationale"] = statement
        data["factual_findings"] = [statement]
        data["contradictions"] = [contradiction]
        parsed = InvestigationOutput.model_validate(data)
        self.assertIsInstance(parsed.rationale, CitedStatement)
        self.assertEqual(parsed.rationale.citations[0].record_id, citation.record_id)

    def test_validation_does_not_resolve_citations_or_read_files(self):
        data = self.candidate_output()
        data["case_id"] = "CASE-NOT-RESOLVED"
        data["alert_id"] = "ALERT-NOT-RESOLVED"
        data["rationale"]["citations"] = [self.citation("evidence", "EVIDENCE-NOT-RESOLVED")]
        json_payload = json.dumps(data)
        with patch("builtins.open", side_effect=OSError("unexpected file read")), patch.object(
            Path, "open", side_effect=OSError("unexpected file read")
        ):
            for validate, payload in (
                (InvestigationOutput.model_validate, data),
                (InvestigationOutput.model_validate_json, json_payload),
            ):
                self.assertEqual(validate(payload).model_dump(), data)


class TestInvestigationOutputReferenceValidation(unittest.TestCase):

    NAMESPACE_IDS = {
        "case": "CASE-G02",
        "customer": "CUST-G02",
        "account": "ACC-G02",
        "counterparty": "CP-G02-01",
        "transaction": "TX-G02-01",
        "alert": "ALT-G02",
        "evidence": "EV-G02-01",
        "verification_check": "CHK-G02-01",
    }
    STATEMENT_LOCATIONS = (
        (("rationale",), "rationale"),
        (("factual_findings", 1), "factual_findings[1]"),
        (("interpretations", 1), "interpretations[1]"),
        (("unresolved_questions", 1), "unresolved_questions[1]"),
        (("missing_information", 1), "missing_information[1]"),
        (("contradictions", 1, "left"), "contradictions[1].left"),
        (("contradictions", 1, "right"), "contradictions[1].right"),
    )

    def investigation(self, case_id="G02"):
        return InvestigationInput.model_validate(load_case(case_id))

    def citation(self, record_type, record_id):
        return {"record_type": record_type, "record_id": record_id}

    def statement(self, citations):
        return {
            "statement": "Independent candidate statement for reference validation.",
            "citations": deepcopy(citations),
        }

    def candidate_output(self, investigation, citations=None):
        """Build candidate output from input identities, without reading reference answers."""
        if citations is None:
            citations = [
                self.citation("transaction", investigation.transactions[0].transaction_id),
                self.citation("evidence", investigation.evidence[0].evidence_id),
            ]
        data = {
            "schema_version": "1.0",
            "case_id": investigation.case.case_id,
            "alert_id": investigation.alert.alert_id,
            "assessment_status": "recommendation_provided",
            "recommended_action": "investigate",
            "rationale": self.statement(citations),
            "contradictions": [{
                "description": "Two candidate accounts requiring separate semantic review.",
                "left": self.statement(citations),
                "right": self.statement(citations),
            } for _ in range(2)],
            "recommendation_scope": "preliminary",
            "human_review_required": True,
        }
        for field in (
            "factual_findings", "interpretations", "unresolved_questions", "missing_information",
        ):
            data[field] = [self.statement(citations), self.statement(citations)]
        return data

    def abstention(self, investigation):
        data = self.candidate_output(investigation)
        data["assessment_status"] = "unable_to_recommend"
        data["recommended_action"] = None
        data["rationale"] = {
            "statement": "Insufficient context to support a preliminary recommendation.",
            "citations": [],
        }
        for field in (
            "factual_findings", "interpretations", "unresolved_questions", "missing_information",
            "contradictions",
        ):
            data[field] = []
        return data

    def statement_at(self, data, path):
        statement = data
        for part in path:
            statement = statement[part]
        return statement

    def assert_invalid_references(self, investigation, output, *message_fragments):
        with self.assertRaises(ValueError) as caught:
            validate_investigation_output_references(investigation, output)
        self.assertIs(type(caught.exception), ValueError)
        for fragment in message_fragments:
            self.assertIn(fragment, str(caught.exception))

    def test_matched_outputs_for_all_five_inputs_return_original_output(self):
        for case_id in ("G01", "G02", "G03", "G04", "G05"):
            data = load_case(case_id)
            for use_json in (False, True):
                with self.subTest(case=case_id, use_json=use_json):
                    investigation = (
                        InvestigationInput.model_validate_json(json.dumps(data))
                        if use_json else InvestigationInput.model_validate(data)
                    )
                    candidate = self.candidate_output(investigation)
                    output = (
                        InvestigationOutput.model_validate_json(json.dumps(candidate))
                        if use_json else InvestigationOutput.model_validate(candidate)
                    )
                    self.assertIs(
                        validate_investigation_output_references(investigation, output), output
                    )

    def test_all_eight_namespaces_resolve_in_every_statement_location(self):
        investigation = self.investigation()
        citations = [
            self.citation(kind, identifier) for kind, identifier in self.NAMESPACE_IDS.items()
        ]
        data = self.candidate_output(investigation, citations)
        output = InvestigationOutput.model_validate(data)
        self.assertIs(validate_investigation_output_references(investigation, output), output)
        self.assertEqual(output.model_dump(), data)

    def test_unknown_ids_are_rejected_in_every_namespace_and_location(self):
        investigation = self.investigation()
        for namespace in self.NAMESPACE_IDS:
            for path, label in self.STATEMENT_LOCATIONS:
                with self.subTest(namespace=namespace, location=label):
                    data = self.candidate_output(investigation)
                    self.statement_at(data, path)["citations"][1] = self.citation(
                        namespace, "RECORD-NOT-SUPPLIED"
                    )
                    output = InvestigationOutput.model_validate(data)
                    self.assert_invalid_references(
                        investigation, output, f"{label}.citations[1]",
                        namespace, "RECORD-NOT-SUPPLIED",
                    )

    def test_wrong_namespace_identifiers_are_rejected(self):
        investigation = self.investigation()
        namespaces = list(self.NAMESPACE_IDS)
        for index, namespace in enumerate(namespaces):
            other_namespace = namespaces[(index + 1) % len(namespaces)]
            wrong_id = self.NAMESPACE_IDS[other_namespace]
            with self.subTest(namespace=namespace, other_namespace=other_namespace):
                data = self.candidate_output(investigation)
                data["rationale"]["citations"][0] = self.citation(namespace, wrong_id)
                output = InvestigationOutput.model_validate(data)
                self.assert_invalid_references(
                    investigation, output, "rationale.citations[0]", namespace, wrong_id
                )

    def test_case_and_alert_identity_mismatches_are_rejected(self):
        investigation = self.investigation()
        for original in (self.candidate_output(investigation), self.abstention(investigation)):
            for field in ("case_id", "alert_id"):
                for value in ("OTHER-IDENTITY", original[field].lower(), f" {original[field]} "):
                    with self.subTest(
                        status=original["assessment_status"], field=field, value=value
                    ):
                        data = deepcopy(original)
                        data[field] = value
                        output = InvestigationOutput.model_validate(data)
                        self.assert_invalid_references(
                            investigation, output, field, repr(value), repr(original[field])
                        )

    def test_g04_transaction_outside_flagged_subset_is_accepted(self):
        investigation = self.investigation("G04")
        self.assertNotIn("TX-105", investigation.alert.transaction_ids)
        data = self.candidate_output(investigation, [self.citation("transaction", "TX-105")])
        output = InvestigationOutput.model_validate(data)
        self.assertIs(validate_investigation_output_references(investigation, output), output)

    def test_contextual_evidence_without_transaction_references_is_accepted(self):
        investigation = self.investigation("G01")
        evidence = investigation.evidence[0]
        self.assertEqual(evidence.related_transaction_ids, [])
        data = self.candidate_output(
            investigation, [self.citation("evidence", evidence.evidence_id)]
        )
        output = InvestigationOutput.model_validate(data)
        self.assertIs(validate_investigation_output_references(investigation, output), output)

    def test_nullable_counterparties_are_preserved_without_fabrication(self):
        for case_id in ("G01", "G05"):
            with self.subTest(case=case_id):
                investigation = self.investigation(case_id)
                original = deepcopy(investigation.model_dump())
                output = InvestigationOutput.model_validate(self.candidate_output(investigation))
                self.assertIs(
                    validate_investigation_output_references(investigation, output), output
                )
                self.assertEqual(investigation.counterparties, [])
                self.assertTrue(
                    all(tx.counterparty_id is None for tx in investigation.transactions)
                )

                data = self.candidate_output(investigation)
                data["rationale"]["citations"][0] = self.citation("counterparty", "CP-NOT-SUPPLIED")
                invalid_output = InvestigationOutput.model_validate(data)
                self.assert_invalid_references(
                    investigation, invalid_output, "rationale.citations[0]", "counterparty"
                )
                self.assertEqual(investigation.model_dump(), original)

    def test_identifier_reuse_across_namespaces_and_unreferenced_records_are_valid(self):
        data = load_case("G02")
        account = deepcopy(data["accounts"][0])
        account["account_id"] = "SHARED-RECORD"
        data["accounts"].append(account)
        counterparty = deepcopy(data["counterparties"][0])
        counterparty["counterparty_id"] = "SHARED-RECORD"
        data["counterparties"].append(counterparty)
        investigation = InvestigationInput.model_validate(data)
        citations = [
            self.citation("account", "SHARED-RECORD"),
            self.citation("counterparty", "SHARED-RECORD"),
        ]
        output = InvestigationOutput.model_validate(self.candidate_output(investigation, citations))
        self.assertIs(validate_investigation_output_references(investigation, output), output)

    def test_questions_and_missing_information_can_have_empty_citations(self):
        investigation = self.investigation()
        data = self.candidate_output(investigation)
        for field in ("unresolved_questions", "missing_information"):
            data[field] = [self.statement([]), self.statement([])]
        output = InvestigationOutput.model_validate(data)
        self.assertIs(validate_investigation_output_references(investigation, output), output)

    def test_abstention_without_citations_is_accepted(self):
        investigation = self.investigation("G05")
        output = InvestigationOutput.model_validate(self.abstention(investigation))
        self.assertEqual(output.rationale.citations, [])
        self.assertEqual(output.factual_findings, [])
        self.assertIsNone(output.recommended_action)
        self.assertIs(validate_investigation_output_references(investigation, output), output)

    def test_citation_identifiers_are_matched_without_normalization(self):
        investigation = self.investigation()
        identifier = investigation.transactions[0].transaction_id
        for value in (identifier.lower(), f" {identifier}", f"{identifier} "):
            with self.subTest(value=value):
                data = self.candidate_output(investigation)
                data["rationale"]["citations"][0] = self.citation("transaction", value)
                output = InvestigationOutput.model_validate(data)
                self.assert_invalid_references(
                    investigation, output, "rationale.citations[0]", repr(value)
                )

    def test_exact_matching_accepts_original_spaces_and_case(self):
        data = load_case("G02")
        data["case"]["case_id"] = " Case-Mixed-01 "
        data["alert"]["alert_id"] = " Alert-Mixed-01 "
        data["case"]["primary_alert_id"] = data["alert"]["alert_id"]
        data["accounts"][0]["account_id"] = " Account-Mixed-01 "
        for transaction in data["transactions"]:
            transaction["account_id"] = data["accounts"][0]["account_id"]
        investigation = InvestigationInput.model_validate(data)
        citations = [
            self.citation("case", investigation.case.case_id),
            self.citation("alert", investigation.alert.alert_id),
            self.citation("account", investigation.accounts[0].account_id),
        ]
        output = InvestigationOutput.model_validate(self.candidate_output(investigation, citations))
        self.assertIs(validate_investigation_output_references(investigation, output), output)
        self.assertEqual(output.case_id, " Case-Mixed-01 ")
        self.assertEqual(output.rationale.citations[2].record_id, " Account-Mixed-01 ")

    def test_success_preserves_values_order_and_nested_object_identity(self):
        investigation = self.investigation("G04")
        data = self.candidate_output(investigation)
        data["rationale"]["statement"] = "  Candidate text with original whitespace.\n"
        data["rationale"]["citations"].reverse()
        output = InvestigationOutput.model_validate(data)
        input_before = deepcopy(investigation.model_dump())
        output_before = deepcopy(output.model_dump())
        original_transactions = investigation.transactions
        original_rationale = output.rationale
        original_citations = output.rationale.citations
        original_citation = output.rationale.citations[0]
        original_side = output.contradictions[1].right
        for _ in range(2):
            self.assertIs(validate_investigation_output_references(investigation, output), output)
        self.assertEqual(investigation.model_dump(), input_before)
        self.assertEqual(output.model_dump(), output_before)
        self.assertIs(investigation.transactions, original_transactions)
        self.assertIs(output.rationale, original_rationale)
        self.assertIs(output.rationale.citations, original_citations)
        self.assertIs(output.rationale.citations[0], original_citation)
        self.assertIs(output.contradictions[1].right, original_side)

    def test_failure_preserves_supplied_objects(self):
        investigation = self.investigation("G04")
        data = self.candidate_output(investigation)
        data["contradictions"][1]["right"]["citations"][1]["record_id"] = "MISSING-EVIDENCE"
        output = InvestigationOutput.model_validate(data)
        input_before = deepcopy(investigation.model_dump())
        output_before = deepcopy(output.model_dump())
        original_side = output.contradictions[1].right
        self.assert_invalid_references(
            investigation, output, "contradictions[1].right.citations[1]", "MISSING-EVIDENCE"
        )
        self.assertEqual(investigation.model_dump(), input_before)
        self.assertEqual(output.model_dump(), output_before)
        self.assertIs(output.contradictions[1].right, original_side)

    def test_validation_reads_no_policy_or_reference_files(self):
        data = load_case("G02")
        data["case"]["policy_id"] = "POLICY-NOT-LOADED"
        investigation = InvestigationInput.model_validate(data)
        output = InvestigationOutput.model_validate(self.candidate_output(investigation))
        with patch("builtins.open", side_effect=OSError("unexpected file read")), patch.object(
            Path, "open", side_effect=OSError("unexpected file read")
        ):
            self.assertIs(validate_investigation_output_references(investigation, output), output)

    def test_actions_claims_and_recorded_verification_statuses_are_not_evaluated(self):
        data = load_case("G02")
        data["evidence"][0]["verification_status"] = "custom_supplied_status"
        data["verification_checks"][0]["status"] = "custom_supplied_status"
        investigation = InvestigationInput.model_validate(data)
        for action in ("close", "investigate", "escalate"):
            candidate = self.candidate_output(investigation)
            candidate["recommended_action"] = action
            candidate["rationale"]["statement"] = "The cited transfer amount is zero."
            output = InvestigationOutput.model_validate(candidate)
            self.assertIs(validate_investigation_output_references(investigation, output), output)
            self.assertEqual(output.recommended_action, action)
            self.assertEqual(output.rationale.statement, "The cited transfer amount is zero.")
        self.assertEqual(investigation.evidence[0].verification_status, "custom_supplied_status")
        self.assertEqual(investigation.verification_checks[0].status, "custom_supplied_status")

    def test_cited_transactions_and_evidence_need_not_reference_each_other(self):
        investigation = self.investigation("G04")
        evidence = next(
            record for record in investigation.evidence if record.evidence_id == "EV-004"
        )
        self.assertNotIn("TX-101", evidence.related_transaction_ids)
        citations = [self.citation("transaction", "TX-101"), self.citation("evidence", "EV-004")]
        output = InvestigationOutput.model_validate(self.candidate_output(investigation, citations))
        self.assertIs(validate_investigation_output_references(investigation, output), output)

    def test_empty_evidence_and_check_collections_do_not_require_citations(self):
        data = load_case("G01")
        data["verification_checks"] = []
        data["evidence"] = []
        investigation = InvestigationInput.model_validate(data)
        citations = [self.citation("transaction", investigation.transactions[0].transaction_id)]
        output = InvestigationOutput.model_validate(self.candidate_output(investigation, citations))
        self.assertIs(validate_investigation_output_references(investigation, output), output)


if __name__ == "__main__":
    unittest.main()
