"""Typed contracts for synthetic AML investigation records."""

import json

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator


# Shared field types
Money = Annotated[
    Decimal,
    Field(ge=0, allow_inf_nan=False, decimal_places=2),
]

Currency = Annotated[
    str,
    Field(pattern=r"^[A-Z]{3}$"),
]

TransactionAmount = Annotated[
    Decimal,
    Field(gt=0, allow_inf_nan=False, decimal_places=2),
]


class ExpectedMonthlyActivity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    minimum: Money
    maximum: Money
    currency: Currency

    typical_daily_cash_deposit_min: Money | None = None
    typical_daily_cash_deposit_max: Money | None = None

    @model_validator(mode="after")
    def check_ranges(self) -> Self:
        if self.maximum < self.minimum:
            raise ValueError(
                "expected monthly maximum must be >= minimum"
            )

        low = self.typical_daily_cash_deposit_min
        high = self.typical_daily_cash_deposit_max

        if (low is None) != (high is None):
            raise ValueError(
                "daily cash deposit minimum and maximum "
                "must be supplied together"
            )

        if low is not None and high is not None and high < low:
            raise ValueError(
                "daily cash deposit maximum must be >= minimum"
            )

        return self


class Customer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    customer_type: Literal["business"]
    industry: str = Field(min_length=1)

    onboarding_date: date
    profile_last_verified: date

    expected_monthly_activity: ExpectedMonthlyActivity

    @model_validator(mode="after")
    def verify_profile_dates(self) -> Self:
        if self.profile_last_verified < self.onboarding_date:
            raise ValueError(
                "profile verification date cannot precede onboarding"
            )

        return self


class Account(BaseModel):
    model_config = ConfigDict(extra="forbid")

    account_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    account_type: str = Field(min_length=1)
    currency: Currency
    opened_at: date


class Transaction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transaction_id: str = Field(min_length=1)
    account_id: str = Field(min_length=1)
    transaction_type: Literal[
        "cash_deposit",
        "domestic_transfer",
        "international_transfer",
    ]
    direction: Literal["credit", "debit"]
    amount: TransactionAmount
    currency: Currency
    occurred_at: datetime
    counterparty_id: str | None = Field(min_length=1)
    description: str | None

    @field_validator("occurred_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("transaction timestamp must include a timezone")

        return value


class Counterparty(BaseModel):
    model_config = ConfigDict(extra="forbid")

    counterparty_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    relationship_status: str


class Alert(BaseModel):
    model_config = ConfigDict(extra="forbid")

    alert_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    created_at: datetime
    transaction_ids: list[Annotated[str, Field(min_length=1)]] = Field(min_length=1)

    @field_validator("created_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("alert timestamp must include a timezone")

        return value


class CaseMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    primary_alert_id: str = Field(min_length=1)
    opened_at: datetime
    policy_id: str = Field(min_length=1)

    @field_validator("opened_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("case timestamp must include a timezone")

        return value


class Evidence(BaseModel):
    """Supplied evidence records; validation does not perform verification."""

    model_config = ConfigDict(extra="forbid", strict=True)

    evidence_id: str = Field(min_length=1)
    evidence_type: str = Field(min_length=1)
    source: str = Field(min_length=1)
    verification_status: str = Field(min_length=1)
    related_transaction_ids: list[Annotated[str, Field(min_length=1)]]
    facts: dict[str, JsonValue]

    @field_validator("facts")
    @classmethod
    def require_json_facts(cls, value: dict[str, JsonValue]) -> dict[str, JsonValue]:
        # Reject non-finite numbers on both Python and JSON validation paths.
        json.dumps(value, allow_nan=False)
        return value


class VerificationCheck(BaseModel):
    """Recorded check results; validation does not execute a new check."""

    model_config = ConfigDict(extra="forbid", strict=True)

    check_id: str = Field(min_length=1)
    check_type: str = Field(min_length=1)
    status: str = Field(min_length=1)
    subject_evidence_ids: list[Annotated[str, Field(min_length=1)]]
    findings: list[Annotated[str, Field(min_length=1)]]


class InvestigationInput(BaseModel):
    """Related synthetic records, with structural integrity and no AML decisions."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"]
    case: CaseMetadata
    customer: Customer
    accounts: list[Account] = Field(strict=True)
    counterparties: list[Counterparty] = Field(strict=True)
    transactions: list[Transaction] = Field(strict=True)
    alert: Alert
    evidence: list[Evidence] = Field(strict=True)
    verification_checks: list[VerificationCheck] = Field(strict=True)

    @model_validator(mode="after")
    def validate_relationships(self) -> Self:
        record_ids: dict[str, set[str]] = {}

        for collection, field, records in (
            ("accounts", "account_id", self.accounts),
            ("counterparties", "counterparty_id", self.counterparties),
            ("transactions", "transaction_id", self.transactions),
            ("evidence", "evidence_id", self.evidence),
            ("verification_checks", "check_id", self.verification_checks),
        ):
            seen: set[str] = set()
            for index, record in enumerate(records):
                identifier = getattr(record, field)
                if identifier in seen:
                    raise ValueError(
                        f"{collection}[{index}].{field}: duplicate identifier {identifier!r}"
                    )
                seen.add(identifier)
            record_ids[collection] = seen

        if self.case.primary_alert_id != self.alert.alert_id:
            raise ValueError(
                f"case.primary_alert_id {self.case.primary_alert_id!r} "
                f"must match alert.alert_id {self.alert.alert_id!r}"
            )
        if self.alert.customer_id != self.customer.customer_id:
            raise ValueError(
                f"alert.customer_id {self.alert.customer_id!r} "
                f"must match customer.customer_id {self.customer.customer_id!r}"
            )

        for index, account in enumerate(self.accounts):
            if account.customer_id != self.customer.customer_id:
                raise ValueError(
                    f"accounts[{index}].customer_id {account.customer_id!r} "
                    f"must match customer.customer_id {self.customer.customer_id!r}"
                )

        for index, transaction in enumerate(self.transactions):
            if transaction.account_id not in record_ids["accounts"]:
                raise ValueError(
                    f"transactions[{index}].account_id: "
                    f"unknown reference {transaction.account_id!r}"
                )
            counterparty_id = transaction.counterparty_id
            if (
                counterparty_id is not None
                and counterparty_id not in record_ids["counterparties"]
            ):
                raise ValueError(
                    f"transactions[{index}].counterparty_id: "
                    f"unknown reference {counterparty_id!r}"
                )

        self._validate_references(
            self.alert.transaction_ids, record_ids["transactions"], "alert.transaction_ids"
        )
        for index, evidence in enumerate(self.evidence):
            self._validate_references(
                evidence.related_transaction_ids,
                record_ids["transactions"],
                f"evidence[{index}].related_transaction_ids",
            )
            self._reject_evaluation_keys(evidence.facts, f"evidence[{index}].facts")

        for index, check in enumerate(self.verification_checks):
            self._validate_references(
                check.subject_evidence_ids,
                record_ids["evidence"],
                f"verification_checks[{index}].subject_evidence_ids",
            )

        return self

    @staticmethod
    def _validate_references(values: list[str], target_ids: set[str], path: str) -> None:
        seen: set[str] = set()
        for index, identifier in enumerate(values):
            if identifier in seen:
                raise ValueError(f"{path}[{index}]: duplicate reference {identifier!r}")
            if identifier not in target_ids:
                raise ValueError(f"{path}[{index}]: unknown reference {identifier!r}")
            seen.add(identifier)

    @classmethod
    def _reject_evaluation_keys(cls, value: JsonValue, path: str) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                nested_path = f"{path}[{key!r}]"
                if key in (
                    "expected_action", "recommended_action", "reference_rationale", "rubric_version",
                ):
                    raise ValueError(
                        f"{nested_path}: evaluation-only key {key!r} is not allowed"
                    )
                cls._reject_evaluation_keys(nested, nested_path)
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                cls._reject_evaluation_keys(nested, f"{path}[{index}]")
