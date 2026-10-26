"""Tests for synthetic AML record contracts."""

import json
import unittest

from copy import deepcopy
from datetime import date, datetime, timedelta, timezone, tzinfo
from decimal import Decimal
from pathlib import Path

from pydantic import ValidationError

from aml_triage.contracts import (
    Account,
    Alert,
    CaseMetadata,
    Counterparty,
    Customer,
    Evidence,
    Transaction,
    VerificationCheck,
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


if __name__ == "__main__":
    unittest.main()
