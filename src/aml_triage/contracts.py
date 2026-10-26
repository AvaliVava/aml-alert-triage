"""Typed contracts for synthetic AML investigation records."""

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


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
