"""Typed contracts for synthetic AML investigation records."""

from datetime import date
from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


# Shared field types
Money = Annotated[
    Decimal,
    Field(ge=0, allow_inf_nan=False, decimal_places=2),
]

Currency = Annotated[
    str,
    Field(pattern=r"^[A-Z]{3}$"),
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