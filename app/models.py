from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field, PlainSerializer


Money = Annotated[
    Decimal,
    PlainSerializer(lambda amount: format(amount, ".2f"), return_type=str, when_used="json"),
]


class AccountType(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class AccountSubtype(StrEnum):
    OPERATING_REVENUE = "operating_revenue"
    CONTRA_REVENUE = "contra_revenue"
    COGS = "cogs"
    OPERATING_EXPENSE = "operating_expense"
    OTHER_INCOME = "other_income"
    BALANCE_SHEET = "balance_sheet"


class EntryStatus(StrEnum):
    POSTED = "posted"
    DRAFT = "draft"
    VOID = "void"


class Account(BaseModel):
    number: str
    name: str
    type: AccountType
    subtype: AccountSubtype
    is_active: bool


class JournalLine(BaseModel):
    account: str
    debit: Decimal = Field(ge=0, allow_inf_nan=False)
    credit: Decimal = Field(ge=0, allow_inf_nan=False)


class JournalEntry(BaseModel):
    id: str
    date: date
    status: EntryStatus
    memo: str
    lines: list[JournalLine]


class Ledger(BaseModel):
    company: str
    currency: str
    accounts: list[Account]
    journal_entries: list[JournalEntry]


class StatementAccount(BaseModel):
    number: str
    name: str
    amount: Money = Decimal("0.00")


class StatementSection(BaseModel):
    accounts: list[StatementAccount] = Field(default_factory=list)
    total: Money = Decimal("0.00")


class IncomeStatement(BaseModel):
    company: str
    currency: str
    start: date
    end: date
    revenue: StatementSection
    cost_of_goods_sold: StatementSection
    gross_profit: Money
    operating_expenses: StatementSection
    operating_income: Money
    other_income: StatementSection
    net_income: Money
