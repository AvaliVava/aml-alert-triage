"""Tests for AML customer and account data contracts."""

import json
import unittest

from copy import deepcopy
from datetime import date
from decimal import Decimal
from pathlib import Path

from pydantic import ValidationError

from aml_triage.contracts import (
    Account,
    Customer,
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


if __name__ == "__main__":
    unittest.main()